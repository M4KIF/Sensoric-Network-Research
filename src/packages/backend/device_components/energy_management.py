
###################################################
# Object responsible for keeping the energy usage #
# in hand. Takes in parameters and simulates the  #
# functioning of an wsn node                      #
###################################################

# mo - member object
# ml - member list
# md - member dictionary
# mt - member tuple
# mv - member variable
# mb - member boolean

###########
# Imports #
###########

# Contains the battery object
from .battery import Battery

# And the values that can be consumed in one time segment
from .energy_usage_values import *

#####################
# Object definition #
#####################


class EMU():

    #########################
    # Objects and variables #
    #########################

    mo_Battery = None

    #######################
    # Methods definitions #
    #######################

    def __init__(self, capacity=3000):

        # Initialising the battery with a choosen value in mAH
        self.mo_Battery = Battery(capacity)


    ########################################################################################################
    # The energy consumtion per single time unit is constant and defined in the file "energy_usage_values" #
    ########################################################################################################


    # Calculates the energy consumed while transmitting data
    def calculate_transmission_action_consumption(self, time=float):
        
        self.mo_Battery.subtract_energy(transmiter_action * time)


    # Calculates the energy consumed while receiving data
    def calculate_receive_action_consumption(self, time=float):
        
        self.mo_Battery.subtract_energy(receiver_action * time)


    # Calculates the energy consumed while the node's sensor was collecting the data
    def calculate_sensor_action_consumption(self):
        
        self.mo_Battery.subtract_energy(sensors_action * 0.01)


    # Calculates the energy consumed while doing calculations 
    def calculate_computing_action_consumption(self):
        
        self.mo_Battery.subtract_energy(computing_action * 0.2)


    # Calculates the percentage of the battery left based on the data from the battery
    def calculate_percent_left(self, time=float):
        
        # Calculating the percentage left out of a single proportion
        return 100 * self.mo_Battery.get_battery_current_capacity_ma() / self.mo_Battery.get_battery_max_capacity_ma()