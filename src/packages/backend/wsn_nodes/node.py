
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

# Geographical Points, areas and other usefull calculations
import shapely

# The module containing energy consumption and calculation related components
from ..node_components import SOC

# Enables sleep time to pause "in_action" for a moment. 
# Helps with displaying the data on the plot with the active node highlighted
import time


#####################
# Object definition #
#####################

class Node():

    # Initialises the node with needed data, ie. its battery capacity, location, and possibly id
    def __init__(self, battery_capacity=int(100), x=int(0), y=int(0), node_id=int):

        ###########
        # Objects #
        ###########

        # Initialising the SOC functionality and setting the battery capacity
        self.mo_SOC = SOC(battery_capacity)

        #####################
        # Node Localisation #
        #####################

        # A point that contains the coordinates of this sensor node
        self.mv_Location = shapely.Point(x, y)

        # Contains the range of a node in meters, defaults to 250m
        self.mv_Range = 200

        # Contains the area that the node can access
        self.mv_Coverage = self.mv_Location.buffer(self.mv_Range)

        ###########################
        # Other nodes information #
        ###########################

        # Can contain tuples of information, node and needed hops

        # Conatains the list of nodes that are within range
        self.ml_AdjacentNodes = []

        # Contains the information about aggregating nodes
        self.ml_AggregatingNodes = []

        # Contains the information about sink nodes
        self.ml_SinkNodes = []

        # Basic path to sink node
        self.ml_Path = list()

        ###########################
        # Node settings variables #
        ###########################

        # The threshold at which node indicates low battery level warning
        self.mv_BatteryLowThreshold = None

        #################
        # Miscellaneous #
        #################

        # This node's id
        self.mv_ID = None

        # The sink node id
        self.mv_SinkID = None

        # For the plotting of the color
        self.mv_Color = 80

        ############
        # Booleans #
        ############

        # Activated only if this node is a sink
        self.mb_Sink = False

    #    Activated only if this node is an aggregating node
        self.mb_Aggregating = False

        # Activated only if this node is the sensing node
        self.mb_Sensing = False

        # Set only if the battery level reaches 20%, so as the network can try and deal with this situation
        self.mb_LowBattery = False

        #
        self.mb_Active = False

        # The default "low battery" warning threshold
        self.mv_BatteryLowThreshold = 20

    def __del__(self):
        
        self.clear()


    def clear(self):
        # Cleaning the nodes stored in the other nodes list
        self.ml_AdjacentNodes.clear()
        self.ml_AggregatingNodes.clear()
        self.ml_Path.clear()
        self.ml_SinkNodes.clear()


    #
    def activate(self):
        self.mb_Active = True


    def deactivate(self):
        self.mb_Active = False


    def is_active(self):
        return self.mb_Active


    # Sets the battery size
    def set_battery_capacity(self, capacity=int):
        # A little shortcut
        self.mo_SOC.mo_EnergyManagement.mo_Battery.set_battery_capacity(capacity)


    # Localizes the node in the environment, a simulation of an gps module
    def set_localization(self, x=int, y=int):
        
        # Setting the device localisation
        self.mv_Location = shapely.Point(x, y)

        self.mv_Coverage = self.mv_Location.buffer(self.mv_Range)


    # Sets the id of a sink node
    def add_sink_node(self, sink=None):
        self.ml_SinkNodes.append(sink)


    # Adds a node which has to be visited in order to reach the Sink
    def add_to_path(self, node):
        self.ml_Path.append(node)


    # Adding a node to the neighbours list
    def add_to_neighbours_list(self, node):
        self.ml_AdjacentNodes.append(node)


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
        return self.mv_Coverage


    def get_battery_level(self):
        
        # Getting the cell's current capacity
        level = self.mo_SOC.get_battery_level()

        # Checking if it is above the threshold
        if level <= self.mv_BatteryLowThreshold and not self.mb_LowBattery:
            self.activate_battery_low_flag()

        return level

    
    def get_neighbours_amount(self):
        return len(self.ml_AdjacentNodes)


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
        
        self.mv_Color = 50

        # Sends the signal to SOC to take care of data collection and energy management
        self.mo_SOC.collect_sensor_data()

        time.sleep(0.05)
        self.mv_Color = 20


    # Receives the data packet
    def receive_data(self, distance=int):

        self.mv_Color = 50

        # Sends the signal to SOC that It has to receive the data wirelesly
        # of course, energy management is obvious
        self.mo_SOC.receive_data(distance)

        time.sleep(0.05)
        self.mv_Color = 20


    # Transmits the data packet
    def transmit_data(self, distance=int):

        self.mv_Color = 50

        # Informs the SOC that It has to follow through the transmission procedures
        self.mo_SOC.transmit_data(distance)

        time.sleep(0.05)
        self.mv_Color = 20

    
    def aggregate_data(self, distance=int):

        self.mv_Color = 50

        self.mo_SOC.aggregate_data(distance)

        time.sleep(0.05)
        self.mv_Color = 20

    
