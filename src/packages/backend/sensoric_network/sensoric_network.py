
############################################
# Sensoric network object, containing all  #
# nodes and informations needed for the    #
# network to work. It implements different #
# approaches to the WSN coverage problem,  #
# a naive one for comparsion and the       #
# Particle Swarm Optimisation techniques   #
############################################



############
# Includes #
############


# For enabling the network functions
from .. import network_elements as components
import random
import shapely


#####################
# Object definition #
#####################


class SensoricNetwork():

    ###########
    # Approaches choice variables #
    ###########

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


    # List containing the names of the implemented approaches to improving the lifetime of a WSN
    ml_Algorithms = ["naive", "Particle-Swarm-Optimisation"]

    #####################
    # Network variables #
    #####################

    # Contains the area polygon
    mv_Area = None

    # The amount of the nodes
    mv_NodeAmount = None

    # The minimum percentile value of the area that the WSN has to cover
    mv_MinimumCoverage = None

    # The current value that the network covers
    mv_CurrentCoverage = None

    # Cell capacity of the nodes
    mv_BatteryCapacity = None

    ######################
    # Nodes, Groups etc. #
    ######################

    # List of all of the sinks that are currently used in any of the solutions
    ml_SinkNodes = []

    # List of all of the standard nodes excluding the sink nodes
    ml_Nodes = []

    # Possibly used for algorithms using grouping as an optimisation
    ml_GroupsOfNodes = []

    #################
    # Miscellaneous #
    #################

    # Stores the "uptime" of the network
    mv_Lifetime = None

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
    def __init__(self, node_amount=int(10), battery_capacity=int(500),
    x_l=int(0), y_l=int(0), x_u=int(1000), y_u=int(1000), minimum_coverage=int(80)):

        # Setting a list of points temporarily, in order to create a polygon
        polygon_points_list = [shapely.Point(x_l, y_l), shapely.Point(x_u, y_l), shapely.Point(x_u, y_u), shapely.Point(x_l, y_u)]

        # Creating a polygon out of the points from above
        self.mv_Area = shapely.Polygon([[p.x, p.y] for p in polygon_points_list])

        # Setting the coverage value
        self.set_minimum_coverage_value(minimum_coverage)

        # Setting the nodes amount
        self.set_node_amount(node_amount)

        # Setting default battery capacity
        self.set_node_battery_capacity(battery_capacity)

        # Setting the default algorithm to be the centralised naive
        self.mv_CurrentAlgorithm = self.ml_Algorithms[0]


    # Sets the nodes amount
    def set_node_amount(self, amount):
        self.mv_NodeAmount = amount


    # Sets the battery capacity in mAH
    def set_node_battery_capacity(self, capacity):
        self.mv_BatteryCapacity = capacity


    # Changes the area of the network
    def set_area(self, x_l=int, y_l=int, x_u=int, y_u=int):

        # Setting a list of points temporarily, in order to create a polygon
        polygon_points_list = [shapely.Point(x_l, y_l), shapely.Point(x_u, y_l), shapely.Point(x_u, y_u), shapely.Point(x_l, y_u)]

        # Creating a polygon out of the points from above
        self.mv_Area = shapely.Polygon([[p.x, p.y] for p in polygon_points_list])


    # Changes the minimum coverage value
    def set_minimum_coverage_value(self, percent_of_area=int):
        self.mv_MinimumCoverage=percent_of_area


    # Setting a sink node
    def set_sink_node(self, node_number=int):
        sink = id(self.ml_Nodes[node_number])

        self.ml_SinkNodes.append(sink)

        for node in self.ml_Nodes:
            node.set_sink_node(self.ml_Nodes[node_number])


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

        #####################################
        # Nodes setup, searching for a sink #
        #####################################

        # Contains a circle in which a sink has to be found
        possible_sink_location = self.mv_Area.point_on_surface().buffer(250)

        # Current lowest distance from the middle point
        lowest_distance = None
        sink = None

        for node in self.ml_Nodes:
            if shapely.contains_xy(possible_sink_location, node.get_localization().coords[:]):

                # Calculating the distance between middle of the area and a node
                temp = shapely.distance(self.mv_Area.point_on_surface(), node.get_localization())

                if lowest_distance == None:
                    lowest_distance = temp
                    sink = node
                else:
                    
                    if temp < lowest_distance:
                        lowest_distance = temp
                        sink = node

        for node in self.ml_Nodes:

            # Setting the sink node in the other nodes
            node.add_sink_node(sink)

        # Searching a path to the sink node via shapely functions
        


    def run_simulation(self):

        # Running a loop until the coverage drops
        while self.mv_CurrentCoverage >= self.mv_MinimumCoverage:

            print(self.mv_CurrentCoverage)
            
            # Checking what kind of approach has to be used 
            if self.mv_CurrentSollution == self.ml_SolutionType[0]:

                # Deciding what kind of centralised algorithm will be used
                if self.mv_CurrentAlgorithm == self.ml_CentralisedAlgorithms[0]:
                    self.naive_algorithm()
            elif self.mv_CurrentSollution == self.ml_SolutionType[1]:

                # Deciding what kind of decentralised algorithm will be used
                print()


    


