
##########################################
# Fully equipped sensoric network object #
##########################################



############
# Includes #
############

# For enabling the network functions
from .. import network_elements as components
import random
import shapely


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
    ml_CentralisedAlgorithms = ["naive"]

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

    # Contains the area polygon
    mv_Area = None

    # The minimum percentile value of the area that the WSN has to cover
    mv_MinimumCoverage = None

    # The current value that the network covers
    mv_CurrentCoverage = None

    # Stores the "uptime" of the network
    mv_Lifetime = None

    # The amount of the nodes
    mv_NodeAmount = None

    # Cell capacity of the nodes
    mv_BatteryCapacity = None

    # Currently used sollution
    mv_CurrentSollution = None

    # Currently used algorithm
    mv_CurrentAlgorithm = None

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


    # A constructor. Takes the amount of nodes,
    # battery capacity, lower left and upper right point of the area covered by sensors as params
    def __init__(self, node_amount=int(10), battery_capacity=int(500), x_l=int(0), y_l=int(0), x_u=int(1000), y_u=int(1000), minimum_coverage=int(80)):

        # Setting a list of points temporarily, in order to create a polygon
        polygon_points_list = [shapely.Point(x_l, y_l), shapely.Point(x_u, y_l), shapely.Point(x_u, y_u), shapely.Point(x_l, y_u)]

        # Creating a polygon out of the points from above
        self.mv_Area = shapely.Polygon([[p.x, p.y] for p in polygon_points_list])

        # Setting the coverage value
        self.set_minimum_coverage_value(minimum_coverage)

        # Setting the currently used sollution
        self.mv_CurrentSollution = self.ml_SolutionType[0]

        # Setting the default algorithm to be the centralised naive
        self.mv_CurrentAlgorithm = self.ml_CentralisedAlgorithms[0]


    #
    def set_node_amount(self, amount):
        self.mv_NodeAmount = amount


    def set_node_battery_capacity(self, capacity):
        self.mv_BatteryCapacity = capacity


    def set_area(self, area=[{"x":0,"z":0}, {"x":0,"z":0}]):

        # Setting the points from lower left, to upper right
        for i in range(2):
            self.ml_Area[i]["x"] = area[i]["x"]
            self.ml_Area[i]["y"] = area[i]["y"]


    def set_minimum_coverage_value(self, percent_of_area=int):
        self.mv_MinimumCoverage=percent_of_area


    # Assigns the neighbours to all of the nodes
    def set_neighbours(self):
        print()


    # Setting a sink node
    def set_sink_node(self, node_number=int):
        sink = id(self.ml_Nodes[node_number])

        for node in self.ml_Nodes:
            node.set_sink_node_id(sink)


    # Sets the network up with the given amount of nodes, 
    # that are spread over a certain and defined area and each one
    # with a battery cell of which the size is specified
    def initiate_network(self, node_amount=int(10), node_cell_capacity=int):

        # Setting the size of the network - amount of sensors overall
        self.set_node_amount(node_amount)

        # Setting the battery capacity of each node
        self.set_node_battery_capacity(node_cell_capacity)

        # Creating the sensors
        for i in range(self.mv_NodeAmount):

            # Appending the list with sensors which have a battery of choosen size       

            # Extracting the bounds of the area polygon
            area_bounds = self.mv_Area.bounds

            # Creating a node with given battery capacity and random points taken from the area that shall be covered
            self.ml_Nodes.append(components.Node(self.mv_BatteryCapacity,
            random.randint(int(area_bounds[0]), int(area_bounds[2])),
            random.randint(int(area_bounds[1]), int(area_bounds[3]))))


    def calculate_coverage(self):
        print()


    def naive_algorithm(self):
        for node in self.ml_Nodes:
            node.collect_data()
            node.send_data()

            if id(node) == id(self.ml_Nodes[sink]):
                continue
            else:
                self.ml_Nodes[sink].receive_data()

            self.calculate_coverage()



    def run_simulation(self):
        print()


    


