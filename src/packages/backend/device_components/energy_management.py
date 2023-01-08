
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

#####################
# Object definition #
#####################


class EMU():

    #########################################
    # Mean energy usage figures based on    #
    # an article titled "Power consumption  #
    # measurements of WSN based on Arduino" #
    # by U T Salim et al 2021 IOP Conf.     #
    # Ser.: Mater. Sci. Eng. 1152 012022    #
    # All values divided by 5V to roughly   #
    # achieve the mA energy consumption     #
    #########################################

    # Energy that transmitting the data take
    mv_TransmiterActionConsumption = 650 / 5

    # Energy that data receiving take
    mv_ReceiverActionConsumption = 500 / 5

    # Energy that the sensors take while collecting data
    mv_SensorsActionConsumption = 350 / 5

    # Energy that either sensing data/receiving/transmitting/
    # neighbour_locating calculations take
    mv_ComputingActionConsumption = 250 / 5

    # Sleep energy Consumption
    mv_SleepConsumption = 0.0005

    #########################
    # Objects and variables #
    #########################

    mo_Battery = None

    #######################
    # Methods definitions #
    #######################


    # Takes the battery capacity in mAH that the battery should be set with
    def __init__(self, capacity_mah=100):

        # Initialising the battery with a choosen value
        self.mo_Battery = Battery(capacity_mah)


    # Calculates the energy consumed while transmitting data
    def calculate_transmission_action_consumption(self, time=float):
        
        # Substracting from the battery
        self.mo_Battery.subtract_energy(self.mv_TransmiterActionConsumption * time)


    # Calculates the energy consumed while receiving data
    def calculate_receive_action_consumption(self, time=float):
        
        # Substracting from the battery
        self.mo_Battery.subtract_energy(self.mv_ReceiverActionConsumption * time)


    # Calculates the energy consumed while the node's sensor was collecting the data
    def calculate_sensor_action_consumption(self):
        
        # Substracting from the battery
        self.mo_Battery.subtract_energy(self.mv_SensorsActionConsumption * 0.05)


    # Calculates the energy consumed while doing calculations 
    def calculate_computing_action_consumption(self):
        
        # Substracting from the battery
        self.mo_Battery.subtract_energy(self.mv_ComputingActionConsumption * 0.2)


    # Simulates the device staying inactive
    def sleep(self, time):

        # Substracting the energy from the battery
        self.mo_Battery.subtract_energy(self.mv_SleepConsumption * time)


    # Calculates the percentage of the battery left based on the data from the battery
    def get_charge_left(self):
        
        # Getting the information from the Battery
        return self.mo_Battery.get_charge_left()