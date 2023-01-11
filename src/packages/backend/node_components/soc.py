
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
# md - member dictionary
# mt - member tuple
# mv - member variable
# mb - member boolean

############
# Includes #
############

# Contains the whole energy management module
from .emu import EMU

# For sleep time calculations
import time

#####################
# Object definition #
#####################

class SOC():

    #########################
    # Objects and variables #
    #########################

    mo_EnergyManagement = None

    mv_LastTimeActive = None

    #######################
    # Methods definitions #
    #######################


    # Takes the battery capacity in mAH as a parameter
    def __init__(self, battery_capacity_mah=100):

        # Initialising the energy management unit with given battery capacity, defaults to 100 mAH
        self.mo_EnergyManagement = EMU(battery_capacity_mah)

        # Setting the latest activity to mimmick switching the device on
        self.mv_LastTimeActive = time.time()


    # Simulating data transmission, the time is dependent on the distance between nodes
    def transmit_data(self, distance=int):

        # Takes the current time
        current_time = time.time()

        # Substracts the amount of energy that the device used while staying inactive
        self.mo_EnergyManagement.sleep(current_time - self.mv_LastTimeActive)

        # Updates the last active variable
        self.mv_LastTimeActive = current_time

        # Sending the amout of time spend to the energy management unit, assuming that the data packets are very small
        self.mo_EnergyManagement.calculate_transmission_action_consumption(distance, 256000, 800000)


    # Simulating data reciving, as above, time dependent on the distance
    def receive_data(self, distance=int):

        # Takes the current time
        current_time = time.time()

        # Substracts the amount of energy that the device used while staying inactive
        self.mo_EnergyManagement.sleep(current_time - self.mv_LastTimeActive)

        # Updates the last active variable
        self.mv_LastTimeActive = current_time

        # Sending the amout of time spend to the energy management unit, assuming that the data packets are very small
        self.mo_EnergyManagement.calculate_receive_action_consumption(distance, 256000, 800000)


    def aggregate_data(self, distance=int):

        # Takes the current time
        current_time = time.time()

        # Substracts the amount of energy that the device used while staying inactive
        self.mo_EnergyManagement.sleep(current_time - self.mv_LastTimeActive)

        # Updates the last active variable
        self.mv_LastTimeActive = current_time

        # Sending the amout of time spend to the energy management unit, assuming that the data packets are very small
        self.mo_EnergyManagement.calculate_data_aggregation(distance, 256000, 800000)



    # Simulates the action of collecting the data from the sensors
    def collect_sensor_data(self):

        # Takes the current time
        current_time = time.time()

        # Substracts the amount of energy that the device used while staying inactive
        self.mo_EnergyManagement.sleep(current_time - self.mv_LastTimeActive)

        # Updates the last active variable
        self.mv_LastTimeActive = current_time
        
        # The collection of data uses a constant amount of energy, that is equal to 1ns of calculations
        self.mo_EnergyManagement.calculate_sensor_action_consumption()


    # Simulates the computing in the WSN, computing the transmission action, receiving or collecting the data.
    def compute_data(self):

        # Takes the current time
        current_time = time.time()

        # Substracts the amount of energy that the device used while staying inactive
        self.mo_EnergyManagement.sleep(current_time - self.mv_LastTimeActive)

        # Updates the last active variable
        self.mv_LastTimeActive = current_time

        # The collection of data uses a constant amount of energy, that is equal to 1ns of calculations
        self.mo_EnergyManagement.calculate_computing_action_consumption()


    def sleep(self, time=float):

        self.mo_EnergyManagement.sleep(time)


    # Checks the device battery level
    def get_battery_level(self):
        
        # Asks the energy management module for battery status
        return self.mo_EnergyManagement.get_charge_percentage_left()