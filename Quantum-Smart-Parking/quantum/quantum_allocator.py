import pandas as pd
import numpy as np
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_algorithms import NumPyMinimumEigensolver
from scipy.optimize import linprog

# ==========================================
# MANUAL CONFIGURATION (UPDATED FOR 16GB)
# ==========================================
RAM_LIMIT_GB = 16
# ==========================================

def quantum_allocate_batch(csv_path, num_vehicles):
    data = pd.read_csv(csv_path)
    slots = data['slot_id'].tolist()
    vehicles = [f"V{i+1}" for i in range(num_vehicles)]
    num_vars = len(vehicles) * len(slots)
    
    # Logic: 2^n states * 16 bytes per complex number
    # 30 qubits = (2^30 * 16) / 1024^3 = 16 GB exactly.
    required_ram = (2**num_vars * 16) / (1024**3)
    
    print(f"[SYSTEM] Qubits: {num_vars} | RAM Needed: {required_ram:.2f} GB")

    # 1. Build the QUBO Problem
    qp = QuadraticProgram("SmartParking")
    for v in vehicles:
        for s in slots:
            qp.binary_var(name=f"x_{v}_{s}")

    costs = {}
    for v in vehicles:
        for _, row in data.iterrows():
            penalty = 0 if row['availability'] == 1 else 100000
            costs[f"x_{v}_{row['slot_id']}"] = row['distance'] + penalty
    qp.minimize(linear=costs)

    # Constraints
    for v in vehicles:
        qp.linear_constraint(linear={f"x_{v}_{s}": 1 for s in slots}, sense="==", rhs=1)
    for s in slots:
        qp.linear_constraint(linear={f"x_{v}_{s}": 1 for v in vehicles}, sense="<=", rhs=1)

    # 2. Solver Selection
    allocations = {}
    
    # With 16GB, we can try the exact solver for up to 30 qubits.
    # Note: If your OS is using too much RAM, this might still trigger the fallback.
    if required_ram <= RAM_LIMIT_GB:
        print("[SOLVER] Hardware Check Passed: Using Exact NumPyMinimumEigensolver")
        try:
            exact_solver = MinimumEigenOptimizer(NumPyMinimumEigensolver())
            result = exact_solver.solve(qp)
            for i, var in enumerate(qp.variables):
                if result.x[i] > 0.5:
                    parts = var.name.split('_')
                    allocations[parts[1]] = parts[2]
            return allocations
        except MemoryError:
            print("[WARNING] System RAM full. Switching to Hybrid Fallback.")

    # Memory Safe Hybrid Mode (Fallback)
    print("[SOLVER] Using Hybrid-Classical Optimizer")
    flat_costs = [row['distance'] + (0 if row['availability'] == 1 else 100000) 
                  for v in vehicles for _, row in data.iterrows()]

    res = linprog(flat_costs, 
                  A_eq=np.kron(np.eye(num_vehicles), np.ones((1, len(slots)))), 
                  b_eq=np.ones(num_vehicles), 
                  A_ub=np.kron(np.ones((1, num_vehicles)), np.eye(len(slots))), 
                  b_ub=np.ones(len(slots)), 
                  method='highs')

    if res.success:
        x_final = res.x.reshape((num_vehicles, len(slots)))
        for i, v_id in enumerate(vehicles):
            slot_idx = np.argmax(x_final[i])
            allocations[v_id] = slots[slot_idx]
            
    return allocations