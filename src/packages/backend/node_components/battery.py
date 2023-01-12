
###############################################
# Battery object, implemented in every node,  #
# initialised via taking in the capacity in   #
# mAH for easy reference on which capacity is #
# large and which is small. Then it converts  #
# it to the amount of charge stored in mA for #
# easy power usage simulation                 #
###############################################


# mo - member object
# ml - member list
# md - member dictionary
# mt - member tuple
# mv - member variable
# mb - member boolean


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


    # Battery capacity getter in mah
    def get_battery_designed_capacity(self):

        return self.mv_DesignedCapacity


    # Battery capacity getter in ma
    def get_battery_current_capacity(self):

        return self.mv_CurrentCapacity


    # Function that effectively discharges the cell
    def subtract_energy(self, amount=int):

        # Subtracting the energy used by the node, after calculating it in the energy management module
        self.mv_CurrentCapacity -= amount


    # Returns the percent of charge left
    def get_charge_percentage_left(self):
        
        # Calculates the percent value with a simple proportion
        return self.mv_CurrentCapacity * 100 / self.mv_DesignedCapacity


    