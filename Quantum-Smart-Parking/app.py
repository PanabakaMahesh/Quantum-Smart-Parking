from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np
import os
import time
from quantum.quantum_allocator import quantum_allocate_batch
from traffic_simulator import run_city_simulation

app = Flask(__name__)

# --- CONFIGURATION ---
CSV_PATH = "data/parking_data.csv"
VEHICLES = 4 
# ---------------------

run_city_simulation(CSV_PATH)

def classical_greedy_allocate(df, num_vehicles):
    """
    Greedy Classical Solver: 
    Picks the closest available slot for each vehicle.
    Fast, but often misses the Global Minimum.
    """
    temp_df = df.copy()
    allocs = {}
    vehicles = [f"V{i+1}" for i in range(num_vehicles)]
    
    for v in vehicles:
        if temp_df.empty:
            break
        best_slot_idx = temp_df['distance'].idxmin()
        best_slot = temp_df.loc[best_slot_idx]
        allocs[v] = best_slot['slot_id']
        temp_df = temp_df.drop(best_slot_idx)
        
    return allocs

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data')
def get_data():
    df = pd.read_csv(CSV_PATH)
    
    # Measure Quantum Speed
    start_q = time.time()
    q_allocs = quantum_allocate_batch(CSV_PATH, VEHICLES)
    end_q = time.time()
    q_speed = (end_q - start_q) * 1000 # Convert to ms
    
    # Measure Classical Speed
    start_c = time.time()
    c_allocs = classical_greedy_allocate(df, VEHICLES)
    end_c = time.time()
    c_speed = (end_c - start_c) * 1000 # Convert to ms
    
    # Calculate Total Distances
    q_total = sum(df[df['slot_id'] == s]['distance'].values[0] for s in q_allocs.values())
    c_total = sum(df[df['slot_id'] == s]['distance'].values[0] for s in c_allocs.values())
    
    return jsonify({
        "slots": df.to_dict('records'),
        "quantum": q_allocs,
        "classical": c_allocs,
        "q_total": int(q_total),
        "c_total": int(c_total),
        "q_speed": round(q_speed, 2),
        "c_speed": round(c_speed, 2),
        "qubits": VEHICLES * len(df)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)