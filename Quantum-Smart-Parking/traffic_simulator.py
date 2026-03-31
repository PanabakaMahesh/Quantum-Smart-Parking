import threading

def run_city_simulation(csv_path):
    """
    PASSIVE MODE: Random external events are disabled.
    Only Quantum-guided vehicles will occupy slots.
    """
    def simulate():
        print("[SYSTEM] Pure Quantum Mode Active: External random traffic is DISABLED.")
        
    threading.Thread(target=simulate, daemon=True).start()