
#############################################
# Battery object, that will be implemented  #
# inside the WSN node, and the base station #
#############################################



#####################
# Object definition #
#####################


class Battery():

    #############
    # Variables #
    #############


    # A value of charge that a fully chareged cell contains in mAH,
    # not using Wh because the voltage in WSN nodes is constant per 
    # device elements
    typical_capacity = 2000

    # Updated constantly
    current_capacity = None


    ###########
    # Methods #
    ###########


    def __init__(self):
        self.current_capacity = self.typical_capacity


    def subtract_energy(self, amount=float, time=float):

        # Subtracting the energy used by multiplying the amperage by time spent
        self.current_capacity -= amount * time


    