import simpy
from Airport.processes import CheckIn, Security, PassportControl, Boarding, Disembarking

class Passenger:
    def __init__(self, env, name, airport, flight_type, gate, arrival_time, capacity):
        self.env = env
        self.name = name
        self.airport = airport
        self.flight_type = flight_type
        self.gate = gate
        self.arrival_time = arrival_time

        # Initialize time attributes for analysis
        self.check_in_time = None
        self.security_time = None
        self.passport_time = None
        self.boarding_time = None
        self.disembark_time = None

        # Start the passenger process
        env.process(self.process_passenger(capacity))  

    def process_passenger(self, capacity):
        """Simulate the complete passenger journey through the airport.
        
        Process flow:
        1. Arrival at airport
        2. Check-in
        3. Security screening
        4. Passport control (international only)
        5. Boarding
        6. Disembarking

        Args:
            capacity (tuple): Airport resource capacities

        Yields:
            simpy.events.Process: Sequence of airport processes
        """
        yield self.env.timeout(self.arrival_time) 
        print(f'[t={self.env.now}] {self.name} arrives at the airport.')

        # Extract specific capacities from tuple
        check_in_capacity = capacity[0]
        security_capacity = capacity[1]
        passport_capacity = capacity[2] if len(capacity) > 2 else None  
        boarding_capacity = capacity[4]

        check_in_process = CheckIn(self.env, check_in_capacity)  
        yield self.env.process(check_in_process.process(self))

        security_process = Security(self.env, security_capacity)  
        yield self.env.process(security_process.process(self))

        if self.flight_type == "International" and passport_capacity is not None:
            passport_process = PassportControl(self.env, passport_capacity)  
            yield self.env.process(passport_process.process(self))  

        boarding_process = Boarding(self.env, boarding_capacity)  
        yield self.env.process(boarding_process.process(self, self.gate))

        disembarking_process = Disembarking(self.env, boarding_capacity)  
        yield self.env.process(disembarking_process.process(self))