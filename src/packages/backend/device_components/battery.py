
#############################################
# Battery object, that will be implemented  #
# inside the WSN node, and the base station #
#############################################

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
    mv_MaxCapacityMah = None
    mv_MaxCapacityMa = None

    # Updated constantly
    mv_CurrentCapacity = None


    ###########
    # Methods #
    ###########


    def __init__(self, capacity=2000):
        
        # Calling the default capacity setter
        self.set_battery_capacity(capacity)

        # Updating the current capacity to the max value
        self.mv_CurrentCapacity = self.mv_MaxCapacityMa


    # A simple battery capacity setter
    def set_battery_capacity(self, capacity=int):
        self.mv_MaxCapacityMah = capacity

        # The amount of mA that the cell can supply in its lifetime
        self.mv_MaxCapacityMa = self.mv_MaxCapacityMah * 3600


    # Battery capacity getter in mah
    def get_battery_mv_MaxCapacityMah(self):
        return self.mv_MaxCapacityMah


    # Battery capacity getter in ma
    def get_battery_mv_MaxCapacityMa(self):
        return self.mv_MaxCapacityMa


    # Battery capacity getter in ma
    def get_battery_mv_CurrentCapacity_ma(self):
        return self.mv_CurrentCapacity


    # Function that effectively discharges the cell
    def subtract_energy(self, amount):

        # Subtracting the energy used by the node, after calculating it in the energy management module
        self.mv_CurrentCapacity -= amount


    