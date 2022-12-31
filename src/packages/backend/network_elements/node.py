
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
        "y": 0,
        "z": 0
    }

    # This node's id
    mv_ID = None

    # The sink node id, for validating if the data can be reached
    mv_SinkNodeID = None

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
        self.m_SOC = components.SOC(500)

        self.md_Location = localisation


    # Localizes the node in the environment, a simulation of an gps module
    def set_localization(self, localisation=dict):
        print()


    # Gets the dictionary with the localization
    def get_localization(self):
        print()


    # Calculates the distance to the given point in space, mainly in x and z axis
    def distance_from(self, localisation=dict):
        print()


    # Calculates the distance between a given node
    def calculate_distance(self, location):
        print()


    # Sends the battery low warning to all nodes that have been found
    def battery_low_warning(self):
        print()


    # Searches for the neighbours ( A simulation of neighbour seeking protocol used in internet network)
    # Simulated with the use of the main wsn map, that contains the 
    def find_neighbours(self, simulated_wsn_map=list):
        print()


    # Adds the neighbour to the list of neighbours after validation
    def add_neighbour(self):
        print()


    def collect_data(self):
        print()


    # Receives the data packet
    def receive_data(self):
        print()


    # Transmits the data packet
    def transmit_data(self):
        print()

    

