class Flight:
    def __init__(self, flight_number, origin, destination, gate_number, passengers):
        self.flight_number = flight_number
        self.origin = origin
        self.destination = destination
        self.gate_number = gate_number
        self.passengers = passengers
        self.check_in_time = 0
        self.security_time = 0
        self.passport_time = 0
        self.boarding_time = 0

    def add_passenger(self, passenger):
        """Adds a passenger to this flight.

        Args:
            passenger (Passenger): The passenger object to add
        """
        self.passengers.append(passenger)

    def total_processing_time(self):
        """Calculate total processing time

        Returns:
            float: Total time of check-in, security, passport and boarding
        """
        return (self.check_in_time + self.security_time + 
                self.passport_time + self.boarding_time)