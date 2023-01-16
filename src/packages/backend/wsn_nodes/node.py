

############################################################
# Basic WSN element: a node, that is essentialy            #
# a small computer with sensors.It's job is to collect and #
# pass/transmit the data to the base(sink) node,           #
# from which it will be taken to the research centre       #
############################################################



############
# Includes #
############


# Geographical Points, areas and other usefull calculations
import shapely

# The module containing energy consumption and calculation related components
from ..node_components import SOC

# Used mainly for the sleep
import time


#####################
# Object definition #
#####################


class Node():


    ###################################
    # Base object methods definitions #
    ###################################


    # Initialises the node with needed data, ie. its battery capacity, location, and possibly id
    def __init__(self, battery_capacity=int(100), x=int(0), y=int(0)):

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

        # Contains the sensing range of a node in meters, defaults to 2 meters
        self.mv_SensingRange = 5

        # Contains the area that the node can access
        self.mv_SensingArea = self.mv_Location.buffer(self.mv_SensingRange)

        # Contains the communication range value
        self.mv_CommunicationRange = 25

        ###########################
        # Other nodes information #
        ###########################

        # Conatains the list of nodes that are within range
        self.ml_AdjacentNodes = []

        # Base station
        self.mv_BaseStation = None

        # Sink node
        self.mv_SinkNode = None

        # Basic path to sink node
        self.ml_Path = set()

        ###########################
        # Node settings variables #
        ###########################

        # The threshold at which node indicates low battery level warning
        self.mv_BatteryLowThreshold = 2

        #################
        # Miscellaneous #
        #################

        # For the plotting of the color
        self.mv_Color = 80

        ############
        # Booleans #
        ############

        # Activated when the multi hop route to the base station has been estabilished
        self.mb_PathEstabilished = False

        # Activated if it needs multi hop communication
        self.mb_MultiHop = False

        # Activated only if this node is a Base Node
        self.mb_BaseStation = False

        # Activated only if this node is a sink
        self.mb_ClusterHead = False

        # Activated only if this node is an aggregating node
        self.mb_Aggregating = False

        # Activated only if this node is the sensing node
        self.mb_Sensing = False

        # Set only if the battery level reaches 20%, so as the network can try and deal with this situation
        self.mb_LowBattery = False

        #
        self.mb_Active = False


    # Clears up after the node just to be sure
    def __del__(self):
        
        self.clear()


    # Clears all of the copy containing lists
    def clear(self):
        # Cleaning the nodes stored in the other nodes list
        self.ml_AdjacentNodes.clear()
        self.ml_Path.clear()
        self.deactivate_base_station_flag()
        self.deactivate_multihop_flag()
        self.deactivate_path_estabilished_flag()
        self.deactivate_cluster_head_flag()

    def clear_flags(self):
        self.deactivate_base_station_flag()
        self.deactivate_multihop_flag()
        self.deactivate_path_estabilished_flag()
        self.deactivate_cluster_head_flag()

    def clear_path(self):
        self.ml_Path.clear()
        self.deactivate_path_estabilished_flag()

    #########################
    # Boolean flags methods #
    #########################


    # Activates the node status flag
    def activate(self):
        self.mb_Active = True

    
    # Deactivates the node status flag
    def deactivate(self):
        # Deactivates the main flag
        self.mb_Active = False

        # Clears all of the flags
        self.clear_flags()


    # Checks the node status flag
    def is_active(self):
        return self.mb_Active


    # Activates the base station flag
    def activate_base_station_flag(self):
        self.mb_BaseStation = True
        self.mv_Color = 0


    # Deactivates the base station flag
    def deactivate_base_station_flag(self):
        self.mb_BaseStation = False
        self.mv_Color = 80


    # Returns the value of the base station flag
    def is_base_station(self):
        return self.mb_BaseStation


    # Activates the cluster head flag
    def activate_cluster_head_flag(self):
        self.mb_ClusterHead = True
        self.mv_Color = 40


    # Deactivates the cluster head flag
    def deactivate_cluster_head_flag(self):
        self.mb_ClusterHead = False
        self.mv_Color = 80


    # Returns the cluster head flag value
    def is_cluster_head(self):
        return self.mb_ClusterHead


    # Activates the multihop flag
    def activate_multihop_flag(self):
        self.mb_MultiHop = True


    # Deactivates the multihop flag
    def deactivate_multihop_flag(self):
        self.mb_MultiHop = False


    # Returns the multihop flag value
    def is_multihop(self):
        return self.mb_MultiHop


    # Activates the path estabilished flag when there is a path to sink/base estabilished
    def activate_path_estabilished_flag(self):
        self.mb_PathEstabilished = True


    # Deactivates the path estabilished flag
    def deactivate_path_estabilished_flag(self):
        self.mb_PathEstabilished = False


    # Returns the flag value
    def is_path_estabilished(self):
        return self.mb_PathEstabilished


    def activate_battery_low_flag(self):
        self.mb_LowBattery = True


    def deactivate_battery_low_flag(self):
        self.mb_LowBattery = False


    def is_battery_low(self):
        return self.mb_LowBattery


    #####################
    # Setters / Getters #
    #####################


    # Sets the base station of the network
    def set_base_station(self, base_station):
        self.mv_BaseStation = base_station


    # Sets the battery size
    def set_battery_capacity(self, capacity):
        # A little shortcut
        self.mo_SOC.set_battery_capacity(capacity)


    # Sets the node colour
    def set_colour(self, colour):
        self.mv_Color = colour


    # Localizes the node in the environment, a simulation of an gps module
    def set_localization(self, x=int, y=int):
        
        # Setting the device localisation
        self.mv_Location = shapely.Point(x, y)

        self.mv_SensingArea = self.mv_Location.buffer(self.mv_SensingRange)


    # Gets the amplifier power mode distance threshold
    def get_amplifier_threshold_distance(self):
        return self.mo_SOC.get_amplifier_threshold_distance()

    
    # Gets a single data packet size
    def get_data_packet_size(self):
        return self.mo_SOC.get_data_packet_size()

    
    # Gets a single status message size
    def get_status_message_size(self):
        return self.mo_SOC.get_status_message_size()

    
    # Gets the communication range of the node
    def get_communication_range(self):
        return self.mv_CommunicationRange


    # Gets a list with hops leading to the sink/base
    def get_path(self):
        temp = []
        for hop in self.ml_Path:
            temp.append(hop)
        return temp


    # Gets the Point with the localization
    def get_localization(self):
        
        return self.mv_Location

    
    # Gets the sensing range of the node
    def get_sensing_range(self):
        return self.mv_SensingRange

    
    # Gets the area of range
    def get_sensing_range_area(self):
        return self.mv_SensingArea


    # Gets the current battery level of this device 
    def get_battery_level(self):
        
        # Getting the cell's current capacity
        level = self.mo_SOC.get_charge_percentage_left()

        # Activating the battery critical flag if bellow 2%
        if level < 2:
            self.activate_battery_low_flag()

        return level

    
    # Gets the number of neighbours that this node has
    def get_neighbours_amount(self):
        return len(self.ml_AdjacentNodes)


    #######################
    # Calculating methods #
    #######################


    # Returns the sensing power consumption unit value
    def calculate_sensing_consumption(self):
        return self.mo_SOC.get_sensing_consumption()


    # Returns the antenna power consumption unit value
    def calculate_antenna_consumption(self):
        return self.mo_SOC.get_antenna_consumption()

    
    # Returns the transmission consumption for given parameters
    def calculate_transmission_consumption(self, distance, packet_size):
        return self.mo_SOC.calculate_transmission_consumption(distance=distance, packet_size=packet_size)


    # Returns the receiver consumption for given parameters
    def calculate_receiver_consumtion(self, packet_size):
        return self.mo_SOC.calculate_receiver_consumption(packet_size=packet_size)


    #################
    # Miscellaneous #
    #################


    # Sets the id of a sink node
    def add_sink_node(self, sink=None):
        self.ml_SinkNode = sink


    # Adds a node which has to be visited in order to reach the Sink
    def add_to_path(self, node):
        if id(node) == id(self.mv_BaseStation):
            self.activate_path_estabilished_flag()
        self.ml_Path.add(node)


    # Adding a node to the neighbours list
    def add_to_neighbours_list(self, node):
        self.ml_AdjacentNodes.append(node)


    # Calculates the distance to the given point in space, mainly in x and z axis
    def distance_from(self, point=shapely.Point()):
        
        # Calculating the distance from a point
        return shapely.distance(self.mv_Location, point)


    # Searches for the neighbours ( A simulation of neighbour seeking protocol used in internet network)
    # Simulated with the use of the main wsn map, that contains the 
    def find_neighbours(self, nodes_list=list):
        
        for node in nodes_list:
            
            if self.distance_from(node.get_localisation()) < self.mv_SensingRange:
                self.add_neighbour(id(node))


    # Adds the neighbour to the list of neighbours after validation
    def add_neighbour(self, neighbour_id=int):
        
        self.ml_AdjacentNodes.append(neighbour_id)
    

    #####################
    # Data transmission #
    #####################


    # Simulates data collection
    def collect_data(self):
        
        # Sends the signal to SOC to take care of data collection and energy management
        self.mo_SOC.sense_data()


    # Receives the data packet
    def receive_data(self):

        self.mo_SOC.receive_data()


    def aggregate_and_send_data(self, distance=float, amount_of_data_packets=int):
        self.mo_SOC.aggregate_and_send_data(distance, amount_of_data_packets)


    # Transmits the data packet
    def transmit_data(self, distance=float):

        # Informs the SOC that It has to follow through the transmission procedures
        self.mo_SOC.send_data(distance)


    def transmit_status(self, distance=float):
        self.mo_SOC.send_status(distance)

    
    def aggregate_data(self, distance=float):

        self.mo_SOC.aggregate_data(distance)