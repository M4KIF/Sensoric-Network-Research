

########################################################
# Object that responsible for keeping the energy usage #
# in hand. Calculates the energy usage in particular   #
# scenarios and substract the amount used from         #
# the battery cell                                     #
########################################################



###########
# Imports #
###########


# Contains the battery object
from .battery import Battery

# For the energy consumption formulas
from math import sqrt, pow


#####################
# Object definition #
#####################


class EMU(Battery):

    #########################
    # Objects and variables #
    #########################

    # Energy consumed per node sensor activation
    mv_SensingPowerConsumption = 0.0000005

    # Energy consumed per bit in Joules
    mv_AntennaPowerConsumption = 0.00000005

    # Energy consumed in Joules per bit per meter squared
    mv_AmplifierLowPowerConsumption = 0.00000000001

    # Energy consumed in Joules per bit per meter quadrupled
    mv_AmplifierHighPowerConsumption = 0.0000000000000013

    # Amplifier power mode switch threshold value[m]
    mv_AmplifierThreshold = None

    #######################
    # Methods definitions #
    #######################


    # Takes the battery capacity in mAH that the battery should be set with
    def __init__(self, capacity_j=1):

        # Initialising the battery class from which the EMU inherits
        super().__init__(capacity_j)

        # Calculating the amplifier threshold value
        self.mv_AmplifierThreshold = sqrt((self.mv_AmplifierLowPowerConsumption/self.mv_AmplifierHighPowerConsumption))


    ##############################
    # Member methods definitions #
    ##############################


    # Sets the sensing power consumption value
    def set_sensing_consumption(self, value=float):
        self.mv_SensingPowerConsumption = value


    # Sets the antenna power consumption value
    def set_antenna_consumption(self, value=float):
        self.mv_AntennaPowerConsumption = value


    # Sets the low power amplifier mode consumption value
    def set_low_power_amplifier_consumption(self, value=float):
        self.mv_AmplifierLowPowerConsumption = value


    # Sets the high power amplifier mode consumption value
    def set_high_power_amplifier_consumption(self, value=float):
        self.mv_AmplifierHighPowerConsumption = value


    # Returns the value of sensing power consumption
    def get_sensing_consumption(self):
        return self.mv_SensingPowerConsumption


    # Gets the antenna power consumption value
    def get_antenna_consumption(self):
        return self.mv_AntennaPowerConsumption


    # Gets the low power amplifier mode consumption value
    def get_low_power_amplifier_consumption(self):
        return self.mv_AmplifierLowPowerConsumption


    # Gets the high power amplifier mode consumption value
    def get_high_power_amplifier_consumption(self):
        return self.mv_AmplifierHighPowerConsumption


    # Gets the threshold distance after which the amplifier goes into high power
    def get_threshold_distance(self):
        return self.mv_AmplifierThreshold


    # Calculates the transmission energy depending on the packet size and distance traveled
    def calculate_transmission_consumption(self, packet_size=int, distance=float):

        # If the distance is smaller than 15 meters, then the amplifier goes into high power mode
        if distance < self.mv_AmplifierThreshold:

            # Returns a value calculated for the low power state
            return (packet_size*self.mv_AntennaPowerConsumption 
            + packet_size*self.mv_AmplifierLowPowerConsumption*pow(distance, 2))

        else:

            # Returns a value calculated for the high power state
            return (packet_size*self.mv_AntennaPowerConsumption 
            + packet_size*self.mv_AmplifierHighPowerConsumption*pow(distance, 4))


    # Calculates the receiver consumption depending on the data size that has been received
    def calculate_receiver_consumption(self, packet_size):
        return packet_size*self.mv_AntennaPowerConsumption