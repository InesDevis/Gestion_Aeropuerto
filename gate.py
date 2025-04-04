class Gate:
    def __init__(self, gate_number):
        self.gate_number = gate_number 

    def __str__(self):
        """Returns a string of the gate.

        Returns:
            str: string in the format "Gate {number}" 
        """
        return f"Gate {self.gate_number}"