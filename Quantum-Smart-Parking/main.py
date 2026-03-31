import os
import time
from traffic_simulator import run_city_simulation
from quantum.quantum_allocator import quantum_allocate_batch
from visualization.parking_visualizer import visualize_parking_animated

# ==========================================
# MANUAL CONFIGURATION
# ==========================================
CSV_PATH = "data/parking_data.csv"
VEHICLES = 4      # Number of Quantum Vehicles (V1, V2, V3...)
REFRESH_RATE = 1  # How fast the UI checks for changes
# ==========================================

def start():
    print("="*60)
    print("    QUANTUM SMART PARKING SYSTEM: LIVE MODE")
    print("="*60)
    
    if not os.path.exists(CSV_PATH):
        print("CRITICAL ERROR: CSV not found!")
        return

    run_city_simulation(CSV_PATH)
    
    try:
        while True:
            # Solve using Quantum Logic
            allocs = quantum_allocate_batch(CSV_PATH, VEHICLES)
            
            # Update the Figure 1 Panel automatically
            visualize_parking_animated(CSV_PATH, allocs)
            
            time.sleep(REFRESH_RATE)
    except KeyboardInterrupt:
        print("\nShutting down...")

if __name__ == "__main__":
    start()