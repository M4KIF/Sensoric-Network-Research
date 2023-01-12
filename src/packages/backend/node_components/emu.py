

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

# Contains the scientific constatns
from scipy import constants as sc_const

# For the energy consumption formulas
from math import sqrt, pow


#####################
# Object definition #
#####################


class EMU(Battery):

    #########################
    # Objects and variables #
    #########################

    #0.0000005
    mv_SensingPowerConsumption = 0.0000005

    # Energy consumed per bit in Joules
    #0.00000005
    mv_AntennaPowerConsumption = 0.00000005

    # Energy consumed in Joules per bit per meter squared
    #0.00000000001
    mv_AmplifierLowPowerConsumption = 0.00000000001

    # Energy consumed in Joules per bit per meter quadrupled
    #0.0000000000000013
    mv_AmplifierHighPowerConsumption = 0.0000000000000013

    #######################
    # Methods definitions #
    #######################


    # Takes the battery capacity in mAH that the battery should be set with
    def __init__(self, capacity_J=1):

        # Initialising the battery class from which the EMU inherits
        super().__init__(capacity_J)


    ##############################
    # Member methods definitions #
    ##############################


    # Returns the value of sensing power consumption
    def get_sensing_consumption(self):
        return self.mv_SensingPowerConsumption


    # Calculates the transmission energy depending on the packet size and distance traveled
    def calculate_transmission_consumption(self, packet_size=int, distance=int):

        # If the distance is smaller than 15 meters, then the amplifier goes into high power mode
        if distance < 15:

            # Returns a value calculated for the low power state
            return (packet_size*self.mv_AntennaPowerConsumption 
            + packet_size*self.mv_AmplifierLowPowerConsumption*sqrt(distance))

        else:

            # Returns a value calculated for the high power state
            return (packet_size*self.mv_AntennaPowerConsumption 
            + packet_size*self.mv_AmplifierHighPowerConsumption*pow(distance, 4))


    # Calculates the receiver consumption depending on the data size that has been received
    def calculate_receiver_consumption(self, packet_size):
        return packet_size*self.mv_AntennaPowerConsumption