
#########################################################
# CPU object class that simulates the node doing        #
# calculations connected to the                         #
# functioning of the sensor network                     #
# Some values are changable, like data transmission and #
# receiving because different distances between nodes   #
# changes the time of transmission.                     #
# Some are considered to be constant values, like       #
# picking sensor data, or computing. Just so the object #
# isn't too complicated                                 #
#########################################################

# mo - member object
# ml - member list
# mv - member variable
# mb - member boolean

############
# Includes #
############

# Contains the scientific constatns
from scipy import constants as sc_const

# Contains the whole energy management module
from .energy_management import EMU

#####################
# Object definition #
#####################

class SOC():

    #########################
    # Objects and variables #
    #########################

    mo_EnergyManagement = None

    #######################
    # Methods definitions #
    #######################


    def __init__(self, battery_capacity=3000):

        # Initialising the energy management unit with given battery capacity, defaults to 3000 mAH
        self.mo_EnergyManagement = EMU(battery_capacity)


    # Simulating data transmission, the time is dependent on the distance between nodes
    def transmit_data(self, distance=float):

        # Sending the amout of time spend to the energy management unit
        self.mo_EnergyManagement.calculate_transmission_action_consumption(distance / sc_const.speed_of_light)


    # Simulating data reciving, as above, time dependent on the distance
    def receive_data(self, distance=float):

        # Sending the amout of time spend to the energy management unit
        self.mo_EnergyManagement.calculate_receive_action_consumption(distance / sc_const.speed_of_light)


    # Simulates the action of collecting the data from the sensors
    def collect_sensor_data(self):
        
        # The collection of data uses a constant amount of energy, that is equal to 1ns of calculations
        self.mo_EnergyManagement.calculate_sensor_action_consumption()


    # Simulates the computing in the WSN, computing the transmission action, receiving or collecting the data.
    def compute_data(self):

        # The collection of data uses a constant amount of energy, that is equal to 1ns of calculations
        self.mo_EnergyManagement.calculate_computing_action_consumption()


    # Checks the device battery level
    def get_battery_level(self):
        
        # Asks the energy management module for battery status
        return self.mo_EnergyManagement.calculate_percent_left()