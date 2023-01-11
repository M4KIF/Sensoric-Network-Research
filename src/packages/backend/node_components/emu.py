
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

    # In mA, I should add the transmission power options to the energy consumption,
    # as with the distance of the transmission the power requirements change in 
    # steps, co a 100m transmission can draw even more than 2 times less power than fe. 200m transmission

    # multiplied by 1000 to make things quicker
    md_TrasmissionPowerLevels = {
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
    mv_SensorsActionConsumption = 100

    # Energy that either sensing data/receiving/transmitting/
    # neighbour_locating calculations take
    mv_ComputingActionConsumption = 100

    # Sleep energy Consumption
    mv_SleepConsumption = 0.05

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


    def ack_transmission_consumption(self, power_level=str):
        return self.md_TrasmissionPowerLevels[power_level]


    # Calculates the signal propagation time
    def calculate_signal_propagation_delay(self, distance=float):

        return distance / sc_const.speed_of_light


    def calculate_data_aggregation(self,distance=int,data_size=int,transmission_rate=int):
        # Substracting from the battery
        self.mo_Battery.subtract_energy(2 * self.ack_transmission_consumption("1")*368/transmission_rate)

        self.mo_Battery.subtract_energy(self.md_TrasmissionPowerLevels["1"] * data_size/transmission_rate)

    # Calculates the energy consumed while transmitting data
    def calculate_transmission_action_consumption(self, distance=int, data_size=int, transmission_rate=int):
        
        # Adding the propagation delay to the time

        # Substracting from the battery
        if distance < 50:
            self.mo_Battery.subtract_energy(4 * self.ack_transmission_consumption("1")*368/transmission_rate)

            self.mo_Battery.subtract_energy(self.md_TrasmissionPowerLevels["1"] * data_size/transmission_rate)
        elif distance > 50 and distance < 200:
            self.mo_Battery.subtract_energy(4 * self.ack_transmission_consumption("15")*368/transmission_rate)

            self.mo_Battery.subtract_energy(self.md_TrasmissionPowerLevels["15"] * data_size/transmission_rate)
        elif distance > 200:
            self.mo_Battery.subtract_energy(4 * self.ack_transmission_consumption("31")*368/transmission_rate)

            self.mo_Battery.subtract_energy(self.md_TrasmissionPowerLevels["31"] * data_size/transmission_rate)


    # Calculates the energy consumed while receiving data
    def calculate_receive_action_consumption(self, distance=float, data_size=int, transmission_rate=int):

        # Adding the propagation delay to the time
        
        #
        self.mo_Battery.subtract_energy(4 * self.ack_transmission_consumption("15")*368/transmission_rate)

        # Substracting from the battery
        self.mo_Battery.subtract_energy(self.mv_ReceiverActionConsumption * data_size/transmission_rate)


    # Calculates the energy consumed while the node's sensor was collecting the data
    def calculate_sensor_action_consumption(self):
        
        # Substracting from the battery
        self.mo_Battery.subtract_energy(self.mv_SensorsActionConsumption)


    # Calculates the energy consumed while doing calculations 
    def calculate_computing_action_consumption(self):
        
        # Substracting from the battery
        self.mo_Battery.subtract_energy(self.mv_ComputingActionConsumption)


    # Simulates the device staying inactive
    def sleep(self, time):

        # Substracting the energy from the battery
        self.mo_Battery.subtract_energy(self.mv_SleepConsumption * time)


    # Calculates the percentage of the battery left based on the data from the battery
    def get_charge_percentage_left(self):
        
        # Getting the information from the Battery
        return self.mo_Battery.get_charge_percentage_left()