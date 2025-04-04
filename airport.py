import simpy
from .flight import Flight
from .processes import CheckIn, Security, PassportControl, Boarding

class Airport:
    def __init__(self, env, num_security, num_checkin, num_passport, num_gates, num_runways):
        self.env = env
        self.check_in_process = CheckIn(env, num_checkin)
        self.security_process = Security(env, num_security)
        self.runways = num_runways
        self.passport_control_process = PassportControl(env, num_passport)
        self.boarding_process = Boarding(env, num_gates)
        self.flights = []

    def schedule_flight(self, flight: Flight):
        """Adds a flight to the airport's schedule flight.

        Args:
            flight (Flight): Flight object to be scheduled.
        """
        
        self.flights.append(flight)

    def process_flight(self, flight: Flight):
        """Executes the full passenger processing workflow for a flight, which includes:
            1. Check-in
            2. Security 
            3. Passport control (if international)
            4. Boarding

        Args:
            flight (Flight): Flight object to be processed.

        Yields:
            simpy.events.process: Simulation events for each process.
        """
        yield self.env.process(self.check_in_process.process(flight))
        yield self.env.process(self.security_process.process(flight))
        yield self.env.process(self.passport_control_process.process(flight))
        yield self.env.process(self.boarding_process.process(flight))