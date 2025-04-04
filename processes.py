import simpy
import random

class CheckIn:
    def __init__(self, env, capacity):
        self
        self.env = env
        self.resource = simpy.Resource(env, capacity=capacity)

    def process(self, passenger):
        """Simulate passenger check-in process.
        
        Args:
            passenger (Passenger): Passenger object to process
            
        Yields:
            simpy.events.process: Check-in process events
        """
        with self.resource.request() as request:
            yield request
            check_in_time = random.randint(2, 8) 
            yield self.env.timeout(check_in_time)
            passenger.check_in_time = check_in_time 
            print(f'[t={self.env.now}] {passenger.name} has completed check-in in {check_in_time} minutes.')

class Security:
    def __init__(self, env, capacity):
        """Initialize security check
        
        Args:
            env (simpy.Environment): Simulation environment
            capacity (int): Number of security counters available
        """
        self.env = env
        self.resource = simpy.Resource(env, capacity=capacity)

    def process(self, passenger):
        """Process passenger through security check.
        
        Args:
            passenger (Passenger): Passenger object to process
            
        Yields:
            simpy.events.Process: Security process events
        """
        with self.resource.request() as request:
            yield request
            security_time = random.randint(2, 5)  
            yield self.env.timeout(security_time)
            passenger.security_time = security_time 
            print(f'[t={self.env.now}] {passenger.name} has passed security check in {security_time} minutes.')

class PassportControl:
    def __init__(self, env, capacity):
        """Initialize passport control
        
        Args:
            env (simpy.Environment): Simulation environment
            capacity (int): Number of passport control counters available
        """
        self.env = env
        self.resource = simpy.Resource(env, capacity=capacity)

    def process(self, passenger):
        """Process passenger through passport control.
        
        Args:
            passenger (Passenger): Passenger object to process
            
        Yields:
            simpy.events.Process: Passport control process events
        """
        with self.resource.request() as request:
            yield request
            passport_time = random.randint(1, 3)  
            yield self.env.timeout(passport_time)
            passenger.passport_time = passport_time  
            print(f'[t={self.env.now}] {passenger.name} has passed passport control in {passport_time} minutes.')

class Boarding:
    def __init__(self, env, capacity):
        """Initialize boarding gates.
        
        Args:
            env (simpy.Environment): Simulation environment
            capacity (int): Number of available boarding gates
        """
        self.env = env
        self.resource = simpy.Resource(env, capacity=capacity)

    def process(self, passenger, gate):
        """Process passenger boarding.
        
        Args:
            passenger (Passenger): Passenger object to board
            gate (str): Gate number/identifier
            
        Yields:
            simpy.events.Process: Boarding process events
        """
        with self.resource.request() as request:
            yield request
            boarding_time = random.randint(5, 15)  
            yield self.env.timeout(boarding_time)
            passenger.boarding_time = boarding_time 
            print(f'[t={self.env.now}] {passenger.name} has boarded the plane at gate {gate} in {boarding_time} minutes.')

class Disembarking:
    def __init__(self, env, capacity):
        """Initialize disembarkation resources.
        
        Args:
            env (simpy.Environment): Simulation environment
            capacity (int): Number of parallel disembarkation points
        """
        self.env = env
        self.resource = simpy.Resource(env, capacity=capacity)

    def process(self, passenger):
        """Process passenger disembarkation.
        
        Args:
            passenger (Passenger): Passenger object to disembark
            
        Yields:
            simpy.events.Process: Disembarkation process events
        """
        with self.resource.request() as request:
            yield request
            disembark_time = random.randint(1, 5)  
            yield self.env.timeout(disembark_time)
            passenger.disembark_time = disembark_time  
            print(f'[t={self.env.now}] {passenger.name} has disembarked in {disembark_time} minutes.')