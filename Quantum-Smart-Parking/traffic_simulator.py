import pandas as pd
import random
import time
import threading

def run_city_simulation(csv_path):
    """
    ACTIVE MODE: Random external events are ENABLED.
    Simulates a living city where slots turn Red/Green automatically.
    """
    def simulate():
        print("[SYSTEM] Active City Simulation Started: External traffic is ENABLED.")
        while True:
            # Wait for 5 seconds between changes
            time.sleep(5) 
            try:
                # 1. Read the current data
                df = pd.read_csv(csv_path)
                
                # 2. Pick a random slot (S1 to S5)
                idx = random.randint(0, len(df)-1)
                
                # 3. Toggle availability: If 1 (Green), make it 0 (Red), and vice-versa
                old_status = df.at[idx, 'availability']
                new_status = 0 if old_status == 1 else 1
                df.at[idx, 'availability'] = new_status
                
                # 4. Save back to CSV so the Quantum Allocator sees the change
                df.to_csv(csv_path, index=False)
                
                status_text = "OCCUPIED (Red)" if new_status == 0 else "FREE (Green)"
                print(f"[SIMULATOR] Slot {df.at[idx, 'slot_id']} status changed to {status_text}")
                
            except Exception as e:
                print(f"[SIMULATOR ERROR] Could not update CSV: {e}")

    # Start the simulation loop in a background thread
    threading.Thread(target=simulate, daemon=True).start()
