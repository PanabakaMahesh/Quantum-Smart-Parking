import pandas as pd
import random
import time
import threading

def run_city_simulation(csv_path):
    """
    ACTIVE MODE: Real-Time Dynamic City Simulator.
    This background thread shuffles BOTH availability AND distances 
    to simulate live, changing traffic conditions.
    """
    def simulate():
        print("[SYSTEM] Active City Simulation Started: Distances and Availability are updating live!")
        while True:
            # Wait for 5 seconds between changes
            time.sleep(5) 
            try:
                # 1. Read the current data
                df = pd.read_csv(csv_path)
                
                # 2. Pick a random slot to toggle availability (Green <--> Red)
                idx = random.randint(0, len(df)-1)
                old_status = df.at[idx, 'availability']
                new_status = 0 if old_status == 1 else 1
                df.at[idx, 'availability'] = new_status
                
                # 3. Shuffle the distances for ALL slots randomly (between 10m and 100m)
                # This makes the vehicles recalculate their routes dynamically!
                new_distances = random.sample(range(10, 101, 5), len(df))
                df['distance'] = new_distances
                
                # 4. Save everything back to the CSV
                df.to_csv(csv_path, index=False)
                
                # Print status to terminal so you can see it working
                print(f"\n[SIMULATOR UPDATE] Slot {df.at[idx, 'slot_id']} is now {'OCCUPIED' if new_status == 0 else 'FREE'}")
                print("📋 New Live Distances: " + ", ".join([f"{row['slot_id']}: {row['distance']}m" for _, row in df.iterrows()]))
                
            except Exception as e:
                print(f"[SIMULATOR ERROR] Could not update CSV: {e}")

    # Start this combined loop in a background thread
    threading.Thread(target=simulate, daemon=True).start()
