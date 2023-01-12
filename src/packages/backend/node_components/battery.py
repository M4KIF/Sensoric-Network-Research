

################################################
# Battery object, implemented later in every   #
# node object. Contains a charge in J, for     #
# the ease of use. Only operation availabe is  #
# substracting from the charge, until it empty #
################################################



#####################
# Object definition #
#####################


class Battery():


    # Takes in the battery capacity as a default argument
    def __init__(self, capacity_J=1):
        
        #############
        # Variables #
        #############

        # A value of charge stored in Joules
        self.mv_DesignedCapacity = capacity_J

        # Updated constantly
        self.mv_CurrentCapacity = self.mv_DesignedCapacity


    ##############################
    # Member methods definitions #
    ##############################


    # A simple battery capacity setter
    def set_battery_capacity(self, capacity_J):

        # Setting the cell capacity in mA
        self.mv_DesignedCapacity = capacity_J

        # Setting current battery capacity as the designed capacity
        self.mv_CurrentCapacity = self.mv_DesignedCapacity


    # Designed battery charge getter
    def get_battery_designed_capacity(self):

        return self.mv_DesignedCapacity


    # Current battery charge getter
    def get_battery_current_capacity(self):

        return self.mv_CurrentCapacity


    # Discharges the cell until empty
    def subtract_energy(self, amount=int):

        # Subtracting the energy, it tries to substract from empty, throws an exception
        if self.mv_CurrentCapacity != 0:
            self.mv_CurrentCapacity -= amount
        else:
            raise Exception("Battery empty")


    # Returns the percent of charge left
    def get_charge_percentage_left(self):
        
        # Calculates the percent value with a simple proportion
        return self.mv_CurrentCapacity * 100 / self.mv_DesignedCapacity


    