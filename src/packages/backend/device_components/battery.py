
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

    #############
    # Variables #
    #############

    # A value of charge that a fully chareged cell contains in mAH,
    # not using Wh for simplicity
    mv_DesignedCapacity = None

    # Updated constantly
    mv_CurrentCapacity = None

    ###########
    # Methods #
    ###########


    # Takes in the battery capacity as a default argument
    def __init__(self, capacity_mah=100):
        
        # Calling the capacity setter
        self.set_battery_capacity(capacity_mah)


    # A simple battery capacity setter
    def set_battery_capacity(self, capacity_mah=int):

        # Setting the cell capacity in mA
        self.mv_DesignedCapacity = capacity_mah * 3600


    # Battery capacity getter in mah
    def get_battery_designed_capacity(self):
        return self.mv_DesignedCapacity


    # Battery capacity getter in ma
    def get_battery_current_capacity(self):
        return self.mv_CurrentCapacity


    # Function that effectively discharges the cell
    def subtract_energy(self, amount):

        # Subtracting the energy used by the node, after calculating it in the energy management module
        self.mv_CurrentCapacity -= amount


    # Returns the percent of charge left
    def get_charge_left(self):
        
        # Calculates the percent value with a simple proportion
        return self.mv_CurrentCapacity * 100 / self.mv_DesignedCapacity


    