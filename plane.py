class Plane:
    def __init__(self, flight_number, plane_type, passengers=None, flight_type=None, gate=None, boarding_start=None):
        self.flight_number = flight_number
        self.plane_type = plane_type
        self.passengers = passengers if passengers else []
        self.flight_type = flight_type
        self.gate = gate
        self.boarding_start = boarding_start
        self.status = "On the ground"


    def __str__(self):
        """Returns a string of the plane status.
        
        Returns:
            str: string of plane with current status
        """
        return f"Plane {self.plane_type} for flight {self.flight_number} is {self.status}."

    def update_status(self, new_status):
        """Update the plane's status.
        
        Args:
            new_status (str): New status to set
            
        Raises:
            ValueError: If invalid status is provided
        """
        valid_statuses = ["On the ground", "Boarding", "In flight", "Landed", "Maintenance"]
        if new_status in valid_statuses:
            self.status = new_status
        else:
            raise ValueError(f"Invalid status: {new_status}. Must be one of: {valid_statuses}")

    def start_boarding(self):
        # Change status to indicate boarding has started.
        self.update_status("Boarding")

    def finish_boarding(self):
        # Change status to indicate boarding completed and plane is departing.
        self.update_status("In flight")

    def land(self):
        # Change status to indicate the plane has landed.
        self.update_status("Landed")

    def maintenance(self):
        # Change status to indicate plane is under maintenance.
        self.update_status("Maintenance")