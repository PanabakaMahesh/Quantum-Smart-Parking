import pandas as pd
import random
import time
import os

CSV_PATH = "data/parking_data.csv"

def simulate_distance_changes():
    print("="*50)
    print("   QUANTUM DYNAMIC DISTANCE SIMULATOR (4V x 5S)")
    print("="*50)

    if not os.path.exists(CSV_PATH):
        print("Error: CSV file not found.")
        return

    try:
        while True:
            df = pd.read_csv(CSV_PATH)

            # Randomly shuffle distances for the 5 slots
            new_distances = random.sample(range(10, 101, 5), len(df))
            df['distance'] = new_distances
            
            df.to_csv(CSV_PATH, index=False)
            
            print(f"\n[UPDATE] New Distances:")
            for _, row in df.iterrows():
                print(f"  {row['slot_id']}: {row['distance']}m")
            
            time.sleep(5) # Moves every 5 seconds
            
    except KeyboardInterrupt:
        print("\nSimulator stopped.")

if __name__ == "__main__":
    simulate_distance_changes()