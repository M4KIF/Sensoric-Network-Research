
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

# Contains the scientific constatns
from scipy import constants as sc_const

from math import sqrt, pow


#####################
# Object definition #
#####################


class EMU(Battery):

    #########################################
    # Mean energy usage figures based on    #
    # an article titled "Power consumption  #
    # measurements of WSN based on Arduino" #
    # by U T Salim et al 2021 IOP Conf.     #
    # Ser.: Mater. Sci. Eng. 1152 012022    #
    # All values divided by 5V to roughly   #
    # achieve the mA energy consumption     #
    #########################################

    # In mA, I should add the transmission power options to the energy consumption,
    # as with the distance of the transmission the power requirements change in 
    # steps, co a 100m transmission can draw even more than 2 times less power than fe. 200m transmission

    # multiplied by 1000 to make things quicker
    md_TransmissionPowerConsumption = {
        "1":4000,
        "3":6000,
        "7":8000,
        "11":10000,
        "15":12000,
        "19":15000,
        "23":18000,
        "27":24000,
        "31":30000
    }

    # Energy that transmitting the data take
    mv_TransmiterActionConsumption = 200

    # Energy that data receiving take
    mv_ReceiverActionConsumption = 200

    # Energy that the sensors take while collecting data
    mv_SamplingConsumption = 100

    # Energy that either sensing data/receiving/transmitting/
    # neighbour_locating calculations take
    mv_ComputingActionConsumption = 100

    # calculate_sleep_consumption energy Consumption
    mv_SleepConsumption = 0.05

    # ACK packet size in bits
    mv_AcknowledgePacketSize = 368

    # The size of a data packet
    mv_DataPacketSize = 256000

    # Transmission speed in bits/s
    mv_TransmissionRate = 800000

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


    def get_sensing_consumption(self):
        return self.mv_SensingPowerConsumption


    def calculate_transmission_consumption(self, packet_size=int, distance=int):

        if distance < 25:
            return (packet_size*self.mv_AntennaPowerConsumption 
            + packet_size*self.mv_AmplifierLowPowerConsumption*sqrt(distance))
        else:
            return (packet_size*self.mv_AntennaPowerConsumption 
            + packet_size*self.mv_AmplifierHighPowerConsumption*pow(distance, 4))


    def calculate_receiver_consumption(self, packet_size):
        return packet_size*self.mv_AntennaPowerConsumption


    ##############
    # Depracated #
    ##############


    # Calculates the signal propagation time
    def calculate_signal_propagation_delay(self, distance=float):

        return distance / sc_const.speed_of_light


    def calculate_ack_consumption(self, power_level=str):
        return (self.mv_AcknowledgePacketSize/self.mv_TransmissionRate * self.md_TransmissionPowerConsumption[power_level])


    def calculate_aggregation_consumption(self,distance=int):
        
        # Calculating the power consumption value
        value = 2 * self.calculate_ack_consumption("1")*368/self.mv_TransmissionRate
        value+=self.md_TransmissionPowerConsumption["1"] * self.mv_DataPacketSize/self.mv_TransmissionRate
        
        return value


    # Calculates the energy consumed while transmitting data
    def calculate_transmiting_consumption(self, distance=int):
        
        # Adding the propagation delay to the time
        value = 0

        # Substracting from the battery
        if distance < 50:
            
            # Adding ack sending consumption
            value+= 4 * self.calculate_ack_consumption("1")*368/self.mv_TransmissionRate
            # Adding transmission power consumption
            value+= self.md_TransmissionPowerConsumption["1"] * self.mv_DataPacketSize/self.mv_TransmissionRate

        elif distance > 50 and distance < 200:
            
             # Adding ack sending consumption
            value+= 4 * self.calculate_ack_consumption("15")*368/self.mv_TransmissionRate
            # Adding transmission power consumption
            value+= self.md_TransmissionPowerConsumption["15"] * self.mv_DataPacketSize/self.mv_TransmissionRate

        elif distance > 200:

             # Adding ack sending consumption
            value+= 4 * self.calculate_ack_consumption("31")*368/self.mv_TransmissionRate
            # Adding transmission power consumption
            value+= self.md_TransmissionPowerConsumption["31"] * self.mv_DataPacketSize/self.mv_TransmissionRate

        return value


    # Calculates the energy consumed while receiving data
    def calculate_receiving_consumption(self, distance=float):

        # Adding the propagation delay to the time
        value = 4 * self.calculate_ack_consumption("15")*368/self.mv_TransmissionRate
        value += self.mv_ReceiverActionConsumption * self.mv_DataPacketSize/self.mv_TransmissionRate

        return value


    # Calculates the energy consumed while the node's sensor was collecting the data
    def calculate_sampling_consumption(self):

        return self.mv_SamplingConsumption


    # Calculates the energy consumed while doing calculations 
    def calculate_computing_consumption(self):

        return self.mv_ComputingConsumption


    # Simulates the device staying inactive
    def calculate_sleep_consumption(self, time):

        # Substracting the energy from the battery
        return self.mv_SleepConsumption * time