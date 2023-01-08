
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
import shapely
from .. import device_components as dc

#####################
# Object definition #
#####################

class Node():

    ###########
    # Objects #
    ###########

    # Initialising the SOC functionality and setting the battery capacity
    mo_SOC = dc.SOC()

    #############
    # Variables #
    #############

    # Conatains the list of nodes that are within range, using python's id()
    ml_AdjacentNodes = []

    # Sink node
    mv_SinkNode = None

    # A dictionary that contains the location of the sensor in 2 dimensions
    mv_Location = shapely.Point(0,0)

    # Contains the range of a node in meters, defaults to 150m
    mv_Range = 150

    # Contains the area that the node can access
    mv_RangeArea = mv_Location.buffer(mv_Range)

    # This node's id
    mv_ID = None

    # The sink node id, for validating if the data can be reached
    mv_SinkID = None

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

    def __init__(self, battery_capacity=int(100), x=int(0), y=int(0), node_id=int):

        # Sets the location of the node
        self.mv_Location = shapely.Point(x, y)

        # Sets current node id
        self.mv_ID = node_id

        print(self.mv_Location.coords[:])

        # The default "low battery" warning threshold
        self.mv_BatteryLowThreshold = 20


    # Localizes the node in the environment, a simulation of an gps module
    def set_localization(self, x=int, y=int):
        
        # Setting the device localisation
        self.md_Location = shapely.Point(x, y)


    # Sets the id of a sink node
    def set_sink_node(self, sink=None):
        self.mv_SinkID = id(sink)

        if self.mv_SinkID == self.mv_ID:
            self.mb_IsSink = True


    # Sends the battery low warning to all nodes that have been found
    def activate_battery_low_flag(self):
        self.mb_BatteryLow = True


    def get_battery_low_flag(self):
        return self.mb_BatteryLow


    # Gets the dictionary with the localization
    def get_localization(self):
        
        return self.mv_Location

    
    def get_range(self):
        return self.mv_Range


    def get_range_area(self):
        return self.mv_RangeArea


    def get_battery_level(self):
        
        # Getting the cell's current capacity
        level = self.mo_SOC.get_battery_level()

        # Checking if it is above the threshold
        if level <= self.mv_BatteryLowThreshold and not self.mb_BatteryLow:
            self.activate_battery_low_flag()

            raise Exception("Battery level low")

        return level


    # Calculates the distance to the given point in space, mainly in x and z axis
    def distance_from(self, point=shapely.Point()):
        
        # Calculating the distance from a point
        return shapely.distance(self.mv_Location, point)


    # Searches for the neighbours ( A simulation of neighbour seeking protocol used in internet network)
    # Simulated with the use of the main wsn map, that contains the 
    def find_neighbours(self, nodes_list=list):
        
        for node in nodes_list:
            
            if self.distance_from(node.get_localisation()) < self.mv_Range:
                self.add_neighbour(id(node))


    # Adds the neighbour to the list of neighbours after validation
    def add_neighbour(self, neighbour_id=int):
        
        self.ml_AdjacentNodes.append(neighbour_id)


    # Simulates data collection
    def collect_data(self):

        # Sends the signal to SOC to take care of data collection and energy management
        self.mo_SOC.collect_sensor_data()


    # Receives the data packet
    def receive_data(self):

        # Sends the signal to SOC that It has to receive the data wirelesly
        # of course, energy management is obvious
        self.mo_SOC.receive_data()


    # Transmits the data packet
    def transmit_data(self):

        # Informs the SOC that It has to follow through the transmission procedures
        self.mo_SOC.transmit_data()

    

