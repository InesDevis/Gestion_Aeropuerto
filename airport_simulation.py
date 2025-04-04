import simpy
import random
import pandas as pd
from Airport.airport import Airport
from Airport.plane import Plane
from Passenger.passenger import Passenger

random.seed(42)

def create_passenger(env, airport, flight_type, gate, capacity, flight_name):
    # Function to create a new passenger
    passenger_id = f"ID{random.randint(100, 999)}"
    arrival_time = random.randint(0, 10)
    return Passenger(env, passenger_id, airport, flight_type, gate, arrival_time, capacity), passenger_id

def run_simulation(env, capacity):
    """Runs an airport simulation function of the workflow of passengers and flights.

    Args:
        env (simpy.Environment): used to manage the simulation.
        capacity (tuple): contains the airport resource capacities.

    Returns:
        list[]: a list which contains the data for a single passenger.
            - 'Passenger ID': ID for the passenger.
            - 'Flight ID': Associated flight number.
            - 'Plane Type': Aircraft model.
            - 'Flight Type': Domestic or international.
            - 'Gate': Assigned boarding gate.
            -  Durations for check-in, security, passport control (if international), boarding, and disembarking.
            - 'Total Processing Time': Sum of all processing durations.
            - 'Simulation Parameters': capacities.
    """
    
    airport = Airport(env, *capacity)
    num_flights = 5  
    flights = []
    data_save = []
    airlines = ["Iberia", "American Airlines", "Delta", "United Airlines", "Lufthansa"]
    available_gates = [f"Gate {chr(65 + i)}" for i in range(capacity[4])]

    # Create flights and passengers
    for _ in range(num_flights):
        flight_name = f"{random.choice(airlines)} {random.randint(1000, 9999)}"
        flight_type = random.choice(["Domestic", "International"])
        gate = random.choice(available_gates)
        plane_type = random.choice(["Boeing 737", "Airbus A320", "Boeing 787", "Airbus A380"])

        passengers = []
        for _ in range(20):
            passenger, passenger_id = create_passenger(env, airport, flight_type, gate, capacity, flight_name)
            passengers.append(passenger)

        plane = Plane(flight_name, plane_type, passengers, flight_type, gate, env.now)
        flights.append(plane)

    env.run(until=100)

    # Collect data after simulation finishes
    for plane in flights:
        for passenger in plane.passengers:
            data_save.append({
                'Passenger ID': passenger.name,
                'Flight ID': plane.flight_number,
                'Plane Type': plane.plane_type,
                'Flight Type': passenger.flight_type,
                'Gate': passenger.gate,
                'Check-in Duration': passenger.check_in_time,
                'Security Duration': passenger.security_time,
                'Passport Duration': passenger.passport_time if passenger.flight_type == "International" else None,
                'Boarding Duration': passenger.boarding_time,
                'Disembark Duration': passenger.disembark_time,
                'Total Processing Time': (passenger.check_in_time + passenger.security_time + 
                                        (passenger.passport_time if passenger.flight_type == "International" else 0) + 
                                        passenger.boarding_time + passenger.disembark_time),
                'Simulation Parameters': str(capacity)
            })

    return data_save