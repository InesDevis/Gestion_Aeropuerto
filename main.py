# PRACTICA: simulación de eventos discretos
# Gestión de aeropuerto
#
# María Moreno, Inés Devís y Adriana Díaz
# Inteligencia Artificial
# Ingeniería Informática y ADE
# CUNEF Universidad

import simpy
import pandas as pd
from tqdm.contrib.itertools import product
from tqdm import tqdm
import contextlib
import io

from Simulation.airport_simulation import run_simulation

def silent(func):
    def wrapper(*args, **kwargs):
        with contextlib.redirect_stdout(io.StringIO()):
            return func(*args, **kwargs)
    return wrapper

@silent
def run_silent_simulation(env, capacity):
    """Run simulation with cartesian product of the available capacities.
    
    Args:
        env (simpy.Environment): simulation environment
        capacity (tuple): contains the airport resource capacities.
        
    Returns:
        list: Simulation results data
    """
    return run_simulation(env, capacity)

if __name__ == '__main__':
    # Setting the capacities parameter's range 
    check_in_capacities = [1, 2, 3, 4]
    security_capacities = [1, 2, 3, 4]
    passport_capacities = [1, 2, 3, 4]
    runways_capacities = [1, 2, 3, 4]
    gates_capacities = [5, 10, 20, 25]
    
    all_data = []
    total_simulations = len(check_in_capacities) * len(security_capacities) * \
                       len(passport_capacities) * len(runways_capacities) * len(gates_capacities)

    # Main progress bar for simulations
    for capacity in tqdm(product(check_in_capacities, security_capacities, 
                               passport_capacities, runways_capacities, gates_capacities),
                        total=total_simulations):
        env = simpy.Environment()
        simulation_data = run_silent_simulation(env, capacity)
        all_data.extend(simulation_data)
        
        # Save accumulated results
        pd.DataFrame(all_data).to_csv('./passenger_flight_data.csv', index=False)

    print("\nAll simulations completed. Data saved to passenger_flight_data.csv")