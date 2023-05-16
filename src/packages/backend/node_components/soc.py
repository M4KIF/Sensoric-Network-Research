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

#####################
# Object definition #
#####################


class SOC:
    # Takes the battery capacity in mAH as a parameter
    def __init__(self, battery_capacity_j=1):
        #########################
        # Objects and variables #
        #########################

        # Initialising the energy management unit with given battery capacity, defaults to 100 mAH
        self.mo_EnergyManagement = EMU(battery_capacity_j)

        # The size of hello/status message
        self.mv_StatusMessageSize = 200

        # The size of the data packet from the node
        self.mv_DataPacketSize = 4000

    #######################
    # Methods definitions #
    #######################

    # Battery size setter
    def set_battery_capacity(self, capacity):
        self.mo_EnergyManagement.set_battery_capacity(capacity)

    # Gets the device battery level
    def get_charge_percentage_left(self):
        # Asks the energy management module for battery status
        return self.mo_EnergyManagement.get_charge_percentage_left()

    # Gets the sensing power consumption
    def get_sensing_consumption(self):
        return self.mo_EnergyManagement.get_sensing_consumption()

    # Gets the antenna power consumption
    def get_antenna_consumption(self):
        return self.mo_EnergyManagement.get_antenna_consumption()

    # Gets the low power amplifier consumption
    def get_low_power_amplifier_consumption(self):
        return self.mo_EnergyManagement.get_low_power_amplifier_consumption()

    # Gets the high power amplifier consumption
    def get_high_power_amplifier_consumption(self):
        return self.mo_EnergyManagement.get_high_power_amplifier_consumption()

    # Gets the distance after which amplifier switches to a high power mode
    def get_amplifier_threshold_distance(self):
        return self.mo_EnergyManagement.get_threshold_distance()

    # Calculates the transmission energy depending on the packet size and distance traveled
    def calculate_transmission_consumption(self, packet_size=int, distance=int):
        return self.mo_EnergyManagement.calculate_transmission_consumption(
            packet_size=packet_size, distance=distance
        )

    # Calculates the receiver consumption depending on the data size that has been received
    def calculate_receiver_consumption(self, packet_size):
        return self.mo_EnergyManagement.calculate_receiver_consumption(
            packet_size=packet_size
        )

    # Gets the data packet size
    def get_data_packet_size(self):
        return self.mv_DataPacketSize

    # Gets the status message packet size
    def get_status_message_size(self):
        return self.mv_StatusMessageSize

    # Emulates the sending of the status message into the network
    def send_status(self, distance=float):
        self.mo_EnergyManagement.subtract_energy(
            self.mo_EnergyManagement.calculate_transmission_consumption(
                self.mv_StatusMessageSize, distance
            )
        )

    # Emulates the sending of the data into the network
    def send_data(self, distance=float):
        self.mo_EnergyManagement.subtract_energy(
            self.mo_EnergyManagement.calculate_transmission_consumption(
                self.mv_DataPacketSize, distance
            )
        )

    def aggregate_and_send_data(self, distance=float, amount_of_data_packets=int):
        self.mo_EnergyManagement.subtract_energy(
            self.mo_EnergyManagement.calculate_transmission_consumption(
                amount_of_data_packets * self.mv_DataPacketSize, distance
            )
        )

    # Emulates the receiving of the data from the network
    def receive_data(self):
        self.mo_EnergyManagement.subtract_energy(
            self.mo_EnergyManagement.calculate_receiver_consumption(
                self.mv_DataPacketSize
            )
        )

    # Emulates the receiving of a status from the network
    def receive_status(self):
        self.mo_EnergyManagement.subtract_energy(
            self.mo_EnergyManagement.calculate_receiver_consumption(
                self.mv_StatusMessageSize
            )
        )

    # Emulates the activation and data collection from the sensors
    def sense_data(self):
        self.mo_EnergyManagement.subtract_energy(
            self.mo_EnergyManagement.get_sensing_consumption()
        )
