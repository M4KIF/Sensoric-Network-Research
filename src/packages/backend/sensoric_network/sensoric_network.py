
##########################################
# Fully equipped sensoric network object #
##########################################



############
# Includes #
############

# For enabling the network functions
from .. import network_elements


class SensoricNetwork():

    ###########
    # Objects #
    ###########

    #############
    # Variables #
    #############   

    # List containing the possible solutions to the problem of maximisation of the lifetime expectancy
    ml_SolutionType = ["Centralised", "Decentralised"]

    # Proposed algorithms for the centralised approach, dispatched by this object
    # assuming that it is a gateway of the whole WSN. This object is then responsible for 
    # simulating the data collection functionality and all of the management
    ml_CentralisedAlgorithms = []

    # Proposed algorithms for the decentralised approach, which will be dispatched mainly
    # by the nodes themselves. This object will only send signals about the data collection,
    # the rest should be carried out by the nodes with the help of the neighbour list
    # The data transmission will recursive with limited amount of hops to transfer the data to the sink
    ml_DecentralisedAlgorithms = []

    # List of all of the sinks that are currently used in any of the solutions
    ml_SinkNodes = []

    # List of all of the standard nodes excluding the sink nodes
    ml_Nodes = []

    # Possibly used for algorithms using grouping as an optimisation
    ml_GroupsOfNodes = []

    # The points that are indicating the area that the WSN shall cover
    ml_Area = [{"x":0,"z":0}, {"x":0,"z":0}]

    # The minimum percentile value of the area that the WSN has to cover
    mv_MinimumCoverage = None

    # The current value that the network covers
    mv_CurrentCoverage = None

    # Stores the "uptime" of the network
    mv_Lifetime = None

    # The amount of the nodes
    mv_Size = None

    # Cell capacity of the nodes
    mv_BatteryCapacity = None

    ############
    # Booleans #
    ############

    # Activated after every call on "Collect data" on the nodes
    mb_DataCollectionRequestSent = False

    # Activated after the initialisation of the nodes, by that I mean:
    # location has been assigned and parameters like cell capacity are correct
    mb_NodesInitialised = False

    # Activated if a valid lists of neighbours has been created for every node
    mb_NeighboursAssigned = False

    # Activated if a node raises an exception concerning the low battery level of a particular node
    mb_LayoutShuffleNeeded = False

    #
    mb_SizeChanged = False

    # 
    mb_BatteryCapacity = False

    #
    mb_CoverageUnderThreshold = False

    #######################
    # Methods definitions #
    #######################


    # Default constructor
    def __init__(self):
        print()


    #
    def set_size(self, size):
        print()

    def set_node_battery_capacity(self, capacity):
        print()

    def set_area(self, area):
        print()


    # Sets the network up with the given amount of nodes, 
    # that are spread over a certain and defined area and each one
    # with a battery cell of which the size is specified
    def initiate_network(self, size=int, node_cell_capacity=int, area=dict):
        self.set_size(size)
        self.set_node_battery_capacity(node_cell_capacity)
        self.set_area(area)


    # Randomises every nodes location over the specified area
    def assign_nodes_location(self):
        print()


    # Assigns the neighbours to all of the nodes
    def assign_neighbours(self):
        print()

    def setup_network(self):
        print()

