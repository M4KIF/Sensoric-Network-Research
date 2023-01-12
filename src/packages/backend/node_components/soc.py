
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

    # New part
    
    # The size of hello/status message
    mv_StatusMessageSize = 200

    # The size of the data packet from the node
    mv_DataPacketSize = 4000

    #######################
    # Methods definitions #
    #######################


    # Takes the battery capacity in mAH as a parameter
    def __init__(self, battery_capacity_mah=100):

        # Initialising the energy management unit with given battery capacity, defaults to 100 mAH
        self.mo_EnergyManagement = EMU(battery_capacity_mah)

        # Setting the latest activity to mimmick switching the device on
        self.mv_LastTimeActive = time.time()


    # New stuff

    def set_battery_capacity(self, capacity):
        self.mo_EnergyManagement.set_battery_capacity(capacity)


    def send_status(self, distance=int):
        self.mo_EnergyManagement.subtract_energy(
            self.mo_EnergyManagement.calculate_transmission_consumption(self.mv_StatusMessageSize, distance)
        )


    def send_data(self, distance=int):
        self.mo_EnergyManagement.subtract_energy(
            self.mo_EnergyManagement.calculate_transmission_consumption(self.mv_DataPacketSize, distance)
        )


    def receive_data(self):
        self.mo_EnergyManagement.subtract_energy(
            self.mo_EnergyManagement.calculate_receiver_consumption(self.mv_DataPacketSize)
        )


    def receive_status(self):
        self.mo_EnergyManagement.subtract_energy(
            self.mo_EnergyManagement.calculate_receiver_consumption(self.mv_StatusMessageSize)
        )


    def sense_data(self):
        self.mo_EnergyManagement.subtract_energy(
            self.mo_EnergyManagement.get_sensing_consumption()
        )


    # Depracated


    def aggregate_data(self, distance=int):

        # Takes the current time
        current_time = time.time()

        # Substracts the amount of energy that the device used while staying inactive
        consumption = self.mo_EnergyManagement.calculate_sleep_consumption(current_time - self.mv_LastTimeActive)

        # Updates the last active variable
        self.mv_LastTimeActive = current_time

        # Calculating the data aggregation energy consumption
        if(consumption!=0):
            consumption += self.mo_EnergyManagement.calculate_aggregation_consumption(distance)
        else:
            consumption = self.mo_EnergyManagement.calculate_aggregation_consumption(distance)

        self.mo_EnergyManagement.subtract_energy(consumption)

    # Simulates the action of collecting the data from the sensors
    def sample(self):

        # Takes the current time
        current_time = time.time()

        # Substracts the amount of energy that the device used while staying inactive
        consumption = self.mo_EnergyManagement.calculate_sleep_consumption(current_time - self.mv_LastTimeActive)

        # Updates the last active variable
        self.mv_LastTimeActive = current_time
        
        # The collection of data uses a constant amount of energy, that is equal to 1ns of calculations
        if consumption != 0:
            consumption += self.mo_EnergyManagement.calculate_sampling_consumption()
        else:
            consumption = self.mo_EnergyManagement.calculate_sampling_consumption()

        self.mo_EnergyManagement.subtract_energy(consumption)


    # Simulates the computing in the WSN, computing the transmission action, receiving or collecting the data.
    def compute_data(self):

        # Takes the current time
        current_time = time.time()

        # Substracts the amount of energy that the device used while staying inactive
        consumption = self.mo_EnergyManagement.calculate_sleep_consumption(current_time - self.mv_LastTimeActive)

        # Updates the last active variable
        self.mv_LastTimeActive = current_time

        # The collection of data uses a constant amount of energy, that is equal to 1ns of calculations
        if consumption != 0:
            consumption += self.mo_EnergyManagement.calculate_computing_consumption()
        else:
            consumption = self.mo_EnergyManagement.calculate_computing_consumption()

        self.mo_EnergyManagement.subtract_energy(consumption)


    def sleep(self, time=float):

        self.mo_EnergyManagement.subtract_energy(self.mo_EnergyManagement.calculate_sleep_consumption(time))


    # Checks the device battery level
    def get_charge_percentage_left(self):
        
        # Asks the energy management module for battery status
        return self.mo_EnergyManagement.get_charge_percentage_left()