import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Interactive mode for live updates
plt.ion()
fig, ax = plt.subplots(figsize=(12, 6))

def visualize_parking_animated(csv_path, allocations):
    data = pd.read_csv(csv_path)
    ax.clear()
    
    ax.set_title("Quantum Smart Parking Dashboard", fontsize=16, fontweight='bold', pad=20)
    
    # Create list of slots currently occupied by Quantum vehicles
    occupied_by_quantum = list(allocations.values())
    
    for i, row in data.iterrows():
        s_id = row['slot_id']
        
        # COLOR LOGIC: 
        # Red if a Quantum car is parked there OR external occupancy.
        # Green if truly empty.
        if s_id in occupied_by_quantum or row['availability'] == 0:
            status_color = "#e74c3c" # Red
        else:
            status_color = "#2ecc71" # Green
        
        # Draw Slot
        rect = patches.Rectangle((i, 0.2), 0.8, 0.6, facecolor=status_color, 
                                 edgecolor="white", linewidth=2, alpha=0.9)
        ax.add_patch(rect)
        
        # Show Slot ID
        ax.text(i + 0.4, 0.35, s_id, ha='center', va='center', color='white', fontweight='bold', fontsize=12)
        
        # If a Quantum vehicle is in this slot, show the Vehicle ID (V1, V2, etc.)
        for v_id, assigned_s_id in allocations.items():
            if assigned_s_id == s_id:
                ax.text(i + 0.4, 0.65, v_id, ha='center', va='center', 
                        color='white', fontweight='bold', fontsize=14, 
                        bbox=dict(facecolor='none', edgecolor='white', boxstyle='round,pad=0.3'))

    # Legend
    green_patch = patches.Patch(color='#2ecc71', label='Free')
    red_patch = patches.Patch(color='#e74c3c', label='Occupied (Quantum Guided)')
    ax.legend(handles=[green_patch, red_patch], loc='lower center', 
              bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=False)

    ax.set_xlim(-1, len(data))
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    plt.draw()
    plt.pause(0.1)