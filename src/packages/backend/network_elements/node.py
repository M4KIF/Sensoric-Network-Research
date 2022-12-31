
############################################################
# Basic WSN element: a node, that is essentialy            #
# a small computer with sensors.It's job is to collect and #
# pass/transmit the data to the base(sink) node,           #
# from which it will be taken to the research centre       #
############################################################

# mo - member object
# ml - member list
# md - member dictionary
# mt - member tuple
# mv - member variable
# mb - member boolean

############
# Includes #
############

import math
from .. import device_components as components

#####################
# Object definition #
#####################

def Node():

    ###########
    # Objects #
    ###########

    # Contains the logic unit of the node
    mo_SOC = None

    #############
    # Variables #
    #############

    # Conatains the list of nodes that are close by and can be accessed
    ml_AdjacentNodesList = []

    # A list that contains the data collected from the sensor/s
    ml_Data = []

    # A dictionary that contains the location of the current sensor
    md_Location = {
        "x": 0,
        "z": 0
    }

    # This node's id
    mv_ID = None

    # The sink node id, for validating if the data can be reached
    mv_SinkNodeID = None

    # The threshold at which node indicates low battery level warning
    # used mainly for sink nodes, as they have to live a bit longer to
    # catch all the data from the other nodes
    mv_BatteryLowThreshold = None

    ############
    # Booleans #
    ############

    # Set only, if this exact node is pointed out as the sink node for the whole network or a certain group
    mb_IsSink = False

    # Set only if the battery level reaches 20%, so as the network can try and deal with this situation
    mb_BatteryLow = False

    #######################
    # Methods definitions #
    #######################

    def __init__(self, localisation=None):
        
        # Initialising the SOC functionality and setting the battery capacity
        self.mo_SOC = components.SOC(500)

        self.md_Location = localisation

        self.mv_BatteryLowThreshold = 20


    # Localizes the node in the environment, a simulation of an gps module
    def set_localization(self, localisation=dict):
        
        # Setting the device localisation
        self.md_Location = localisation


    # Sends the battery low warning to all nodes that have been found
    def activate_battery_low_flag(self):
        self.mb_BatteryLow = True


    def get_battery_low_flag(self):
        return self.mb_BatteryLow


    # Gets the dictionary with the localization
    def get_localization(self):
        
        return self.md_Location


    def get_battery_level(self):
        
        # Getting the cell's current capacity
        level = self.mo_SOC.get_battery_level()

        # Checking if it is above the threshold
        if level <= self.mv_BatteryLowThreshold and not self.mb_BatteryLow:
            self.activate_battery_low_flag()

            raise Exception("Battery level low")

        return level


    # Calculates the distance to the given point in space, mainly in x and z axis
    def distance_from(self, localisation=dict):
        
        # Calculating the distance from a point
        return math.dist([md_Location.get("x"), md_Location.get("z")], [localisation.get("x"), localisation.get("z")])


    # Searches for the neighbours ( A simulation of neighbour seeking protocol used in internet network)
    # Simulated with the use of the main wsn map, that contains the 
    def find_neighbours(self, simulated_wsn_map=list):
        
        for node in simulated_wsn_map:
            if self.distance_from(node.get_localisation()) < 1000:
                self.add_neighbour(node)


    # Adds the neighbour to the list of neighbours after validation
    def add_neighbour(self, node=Node()):
        
        self.ml_AdjacentNodesList.append(node)


    # Simulates data collection
    def collect_data(self):
        print()


    # Receives the data packet
    def receive_data(self):
        print()


    # Transmits the data packet
    def transmit_data(self):
        print()

    

