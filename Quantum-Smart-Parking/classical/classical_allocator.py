import pandas as pd

def classical_allocate_batch(csv_path, num_vehicles=5):
    # Load the latest data
    data = pd.read_csv(csv_path)
    
    # Filter only available slots and sort by distance (Greedy approach)
    available_slots = data[data['availability'] == 1].sort_values(by='distance').reset_index()
    
    allocations = {}
    vehicles = [f"V{i+1}" for i in range(num_vehicles)]
    
    for i, v in enumerate(vehicles):
        if i < len(available_slots):
            # Assign the i-th closest slot to the i-th vehicle
            allocations[v] = available_slots.loc[i, 'slot_id']
        else:
            # No slots left for this vehicle
            allocations[v] = "FULL"
            
    return allocations