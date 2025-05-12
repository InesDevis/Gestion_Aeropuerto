# pso_optimizer.py
#
# This file defines a PSO (Particle Swarm Optimization) strategy for improving airport performance.
# It searches for the optimal combination of airport resource capacities—such as check-in counters, security lanes,
# passport control booths, runways, and boarding gates—in order to minimize the average passenger processing time.
# The simulation runs silently for each configuration, and the PSO algorithm finds the best setup within the defined bounds.
# The result is returned as a DataFrame showing the best resource combination and the corresponding performance score.

import numpy as np
import pandas as pd
from pyswarm import pso
import simpy
import contextlib
import io
from simulation.airport_simulation import run_simulation

def silent(func):
    def wrapper(*args, **kwargs):
        with contextlib.redirect_stdout(io.StringIO()):
            return func(*args, **kwargs)
    return wrapper

@silent
def run_silent_simulation(env: simpy.Environment, capacity: tuple[int, int, int, int, int]) -> dict:
    """
    Run the airport simulation silently and return performance metrics.

    Args:
        env (simpy.Environment): simPy environment.
        capacity (tuple): resource capacities [check-in, security, passport, runways, gates].

    Returns:
        dict: dictionary with 'average_time'.
    """
    df = run_simulation(env, capacity)
    if df.empty:
        return {"average_time": float('inf')}
    avg_time = df["Total Processing Time"].mean()
    return {"average_time": avg_time}

def simulation_objective(x: np.ndarray) -> float:
    """
    Objective function used in PSO, wraps the silent simulation.

    Args:
        x (np.ndarray): Candidate capacities.

    Returns:
        float: Average processing time (to minimize).
    """
    capacities = tuple(int(round(i)) for i in x)
    env = simpy.Environment()
    result = run_silent_simulation(env, capacities)
    return result["average_time"]

def pso_opt() -> pd.DataFrame:
    """
    Run PSO to optimize airport resource.

    Returns:
        pd.DataFrame: DataFrame with best found solution and its fitness value.
    """
    lb = [1, 1, 1, 1, 5]   
    ub = [4, 4, 4, 4, 25]  

    # PSO parameters
    swarmsize = 30
    maxiter = 50
    w = 0.5
    c1 = 1.5
    c2 = 1.5

    # Run PSO
    best_solution, best_value = pso(
        simulation_objective,
        lb,
        ub,
        swarmsize=swarmsize,
        omega=w,
        phip=c1,
        phig=c2,
        maxiter=maxiter,
        debug=False
    )

    df_result = pd.DataFrame({
        "Best Solution": [best_solution],
        "Fitness Value (Avg. Time)": [best_value]
    })

    return df_result
