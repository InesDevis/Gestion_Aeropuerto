# fuzzy_logic.py
#
# This file defines a fuzzy logic system to estimate passenger satisfaction at an airport.
# The system considers two main inputs: the number of available check-in counters (capacity)
# and the average waiting time experienced by passengers.
# Based on these inputs, the system uses fuzzy logic rules to classify satisfaction into three levels:
# poor, average, or good.
# This allows us to evaluate airport performance in a more human-like and interpretive way,
# rather than using only strict numerical thresholds.
# It supports visualization and can return a final satisfaction score scaled as a percentage (0 to 100).

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import numpy as np


class AirportSatisfaction:
    def __init__(self) -> None:
        # Define the fuzzy variables
        self.checkin_capacity: ctrl.Antecedent = ctrl.Antecedent(np.arange(0, 11, 1), 'checkin_capacity')
        self.waiting_time: ctrl.Antecedent = ctrl.Antecedent(np.arange(0, 11, 1), 'waiting_time')
        self.passenger_satisfaction: ctrl.Consequent = ctrl.Consequent(np.arange(0, 11, 1), 'passenger_satisfaction')

        # Define fuzzy membership functions
        self.checkin_capacity.automf(3)
        self.waiting_time.automf(3)

        self.checkin_capacity['poor'] = fuzz.trimf(self.checkin_capacity.universe, [0, 0, 5])
        self.checkin_capacity['average'] = fuzz.trimf(self.checkin_capacity.universe, [0, 5, 10])
        self.checkin_capacity['good'] = fuzz.trimf(self.checkin_capacity.universe, [5, 10, 10])

        self.waiting_time['low'] = fuzz.trimf(self.waiting_time.universe, [0, 0, 5])
        self.waiting_time['medium'] = fuzz.trimf(self.waiting_time.universe, [0, 5, 10])
        self.waiting_time['high'] = fuzz.trimf(self.waiting_time.universe, [5, 10, 10])

        self.passenger_satisfaction['poor'] = fuzz.trimf(self.passenger_satisfaction.universe, [0, 0, 5])
        self.passenger_satisfaction['average'] = fuzz.trimf(self.passenger_satisfaction.universe, [0, 5, 10])
        self.passenger_satisfaction['good'] = fuzz.trimf(self.passenger_satisfaction.universe, [5, 10, 10])

        # Define fuzzy rules
        self.rule1 = ctrl.Rule(self.checkin_capacity['poor'] | self.waiting_time['high'], self.passenger_satisfaction['poor'])
        self.rule2 = ctrl.Rule(self.checkin_capacity['poor'] | self.waiting_time['medium'], self.passenger_satisfaction['average'])
        self.rule3 = ctrl.Rule(self.checkin_capacity['average'] | self.waiting_time['medium'], self.passenger_satisfaction['average'])
        self.rule4 = ctrl.Rule(self.checkin_capacity['good'] | self.waiting_time['low'], self.passenger_satisfaction['good'])
        self.rule5 = ctrl.Rule(self.checkin_capacity['average'] | self.waiting_time['low'], self.passenger_satisfaction['good'])
        
        self.system_ctrl: ctrl.ControlSystem = ctrl.ControlSystem([self.rule1, self.rule2, self.rule3, self.rule4, self.rule5])

    def evaluate_satisfaction(self, capacity: float, time: float) -> float:
        simulator: ctrl.ControlSystemSimulation = ctrl.ControlSystemSimulation(self.system_ctrl)
        simulator.input['checkin_capacity'] = capacity
        simulator.input['waiting_time'] = time
        simulator.compute()
        return simulator.output['passenger_satisfaction']*10

    def visualize(self, plot: bool = True) -> None:
        if plot:
            self.checkin_capacity.view()
            self.waiting_time.view()
            self.passenger_satisfaction.view()
            plt.savefig("Grafic.png")
            plt.show()