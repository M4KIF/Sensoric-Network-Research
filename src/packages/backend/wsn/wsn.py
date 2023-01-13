
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
from .. import wsn_nodes as components
from numpy.random import uniform
import random
import shapely


#####################
# Object definition #
#####################


class SensoricNetwork():


    #######################
    # Methods definitions #
    #######################


    # A constructor. Takes the amount of nodes,
    # battery capacity, lower left and upper right point of the area covered by sensors as params
    def __init__(self, node_amount=int(10), battery_capacity=int(50), height=int(1000), width=int(1000),
    minimum_coverage=int(70)):

        ###########
        # Approaches choice variables #
        ###########

        # List containing the names of the implemented approaches to improving the lifetime of a WSN
        self.ml_Algorithms = ["naive", "Particle-Swarm-Optimisation"]

        # Runtime speed x times faster than real
        self.ml_RuntimeSpeed = ["100", "500", "1000", "10000"]

        #####################
        # Network variables #
        #####################

        # Setting a list of points temporarily, in order to create a polygon
        self.ml_AreaBounds = [shapely.Point(0, 0), shapely.Point(width, 0), shapely.Point(width, height), shapely.Point(0, height)]

        # Contains the area polygon
        self.mv_AreaPolygon = shapely.Polygon([[p.x, p.y] for p in self.ml_AreaBounds])

        # Contains the width of the area
        self.mv_Width = width

        # Contains the height of the area
        self.mv_Height = height

        # The amount of the nodes
        self.mv_NodeAmount = node_amount

        # Active nodes amount
        self.mv_ActiveNodes = 0

        # The minimum percentile value of the area that the WSN has to cover
        self.mv_MinimumCoverage = minimum_coverage

        # The current value that the network covers
        self.mv_CurrentCoverage = None

        # Cell capacity of the nodes
        self.mv_BatteryCapacity = battery_capacity

        ######################
        # Nodes, Groups etc. #
        ######################

        # Contains the base station
        self.mv_BaseStation = components.Node(battery_capacity, self.mv_AreaPolygon.point_on_surface().coords[:][0][0], 
        self.mv_AreaPolygon.point_on_surface().coords[:][0][1])

        # List of all of the sinks that are currently used in any of the solutions
        self.ml_SinkNodes = []

        # List of all of the standard nodes excluding the sink nodes
        self.ml_Nodes = []

        # Possibly used for algorithms using grouping as an optimisation
        self.ml_GroupsOfNodes = []

        #################
        # Miscellaneous #
        #################

        # Stores the "uptime" of the network
        self.mv_Lifetime = None

        # Currently used algorithm
        self.mv_CurrentAlgorithm = self.ml_Algorithms[0]

        self.ml_xAxisPlotData = []
        self.ml_yAxisPlotData = []
        self.ml_ColorPlotData = []

        ############
        # Booleans #
        ############

        # Activated after every call on "Collect data" on the nodes
        self.mb_DataCollectionRequestSent = False

        # Activated if all of the nodes properties are set
        self.mb_EssentialPropertiesSet = False

        # Activated if the nodes are initialised
        self.mb_NodesInitialised = False

        # Activated after the initialisation of the nodes, by that I mean:
        # location has been assigned and parameters like cell capacity are correct
        self.mb_NetworkReady = False

        # Activated if a valid lists of neighbours has been created for every node
        self.mb_NeighboursAssigned = False

        # Activated if a node raises an exception concerning the low battery level of a particular node
        self.mb_LayoutShuffleNeeded = False

        #
        self.mb_SizeChanged = False

        # 
        self.mb_BatteryCapacity = False

        #
        self.mb_CoverageUnderThreshold = False


    ##############################
    # Member methods definitions #
    ##############################


    def set_height(self, height=int):

        # Setting the height
        self.mv_Height = height

        # Deactivating the ready flag
        self.mb_NetworkReady = False
        self.mb_NodesInitialised = False

        # Recreating the Area bounds and the polygon
        self.ml_AreaBounds = [shapely.Point(0, 0), shapely.Point(self.mv_Width, 0), shapely.Point(self.mv_Width, height), shapely.Point(0, height)]
        self.mv_AreaPolygon = shapely.Polygon([[p.x, p.y] for p in self.ml_AreaBounds])

        # After changing the dimensions I have to reinitiate the network partly
        for node in self.ml_Nodes:
            node.clear()

        self.ml_SinkNodes.clear()
        self.ml_Nodes.clear()
        self.ml_GroupsOfNodes.clear()
        
        self.initiate_network()

    def set_width(self, width=int):

        # Setting the width
        self.mv_Width = width

        # Deactivating the ready flag
        self.mb_NetworkReady = False
        self.mb_NodesInitialised = False

        # Recreating the Area bounds and the polygon
        self.ml_AreaBounds = [shapely.Point(0, 0), shapely.Point(width, 0), shapely.Point(width, self.mv_Height), shapely.Point(0, self.mv_Height)]
        self.mv_AreaPolygon = shapely.Polygon([[p.x, p.y] for p in self.ml_AreaBounds])

        # After changing the dimensions I have to reinitiate the network partly
        for node in self.ml_Nodes:
            node.clear()

        self.ml_SinkNodes.clear()
        self.ml_Nodes.clear()
        self.ml_GroupsOfNodes.clear()
        
        self.initiate_network()


#    Changes the area of the network
    def set_area_dimensions(self, height=int, width=int):

        # Setting the height
        self.mv_Width = width

        # Setting the height
        self.mv_Height = height    

        # Deactivating the ready flag
        self.mb_NetworkReady = False
        self.mb_NodesInitialised = False

        # Setting a list of points temporarily, in order to create a polygon
        self.ml_AreaBounds = [shapely.Point(0, 0), shapely.Point(width, 0), shapely.Point(width, height), shapely.Point(0, height)]

        # Creating a polygon out of the points from above
        self.mv_AreaPolygon = shapely.Polygon([[p.x, p.y] for p in self.ml_AreaBounds])

        # After changing the dimensions I have to reinitiate the network partly
        for node in self.ml_Nodes:
            node.clear()

        self.ml_SinkNodes.clear()
        self.ml_Nodes.clear()
        self.ml_GroupsOfNodes.clear()
        
        self.initiate_network()


    # Sets the nodes amount
    def set_node_amount(self, amount):
        self.mv_NodeAmount = amount

        # Deactivating the ready flag
        self.mb_NetworkReady = False
        self.mb_NodesInitialised = False

        # After changing the dimensions I have to reinitiate the network partly
        for node in self.ml_Nodes:
            node.clear()

        self.ml_SinkNodes.clear()
        self.ml_Nodes.clear()
        self.ml_GroupsOfNodes.clear()
        
        self.initiate_network()


    # Sets the battery capacity in mAH
    def set_node_battery_capacity(self, capacity):
        self.mv_BatteryCapacity = capacity

        for node in self.ml_Nodes:
            node.set_battery_capacity(self.mv_BatteryCapacity)


    # Changes the minimum coverage value
    def set_minimum_coverage_value(self, percent_of_area=int):
        self.mv_MinimumCoverage=percent_of_area


    def set_algorithm(self, index=int):
        self.mv_CurrentAlgorithm = self.ml_Algorithms[index]


    # Setting a sink node
    def set_sink_node(self, node_number=int):
        sink = id(self.ml_Nodes[node_number])

        self.ml_SinkNodes.append(sink)

        for node in self.ml_Nodes:
            node.set_sink_node(self.ml_Nodes[node_number])


    def can_initiate(self):
        print() 


    # Sets the network up with the given amount of nodes, 
    # that are spread over a certain and defined area and each one
    # with a battery cell of which the size is specified
    def initiate_network(self):

        # Creating the sensors
        for i in range(self.mv_NodeAmount):

            # Appending the list with sensors which have a battery of choosen size       

            # Extracting the bounds of the area polygon
            area_bounds = self.mv_AreaPolygon.bounds

            # Creating a node with given battery capacity and random points taken from the area that shall be covered
            self.ml_Nodes.append(components.Node(self.mv_BatteryCapacity, uniform(0.0, self.mv_Width), uniform(0.0, self.mv_Height)))

        self.mb_NetworkReady = True
        self.mb_NodesInitialised = True

        self.mv_BaseStation=components.Node(self.mv_BatteryCapacity, self.mv_AreaPolygon.point_on_surface().coords[:][0][0], 
        self.mv_AreaPolygon.point_on_surface().coords[:][0][1])
        self.mv_BaseStation.activate_base_station_flag()

        self.ml_Nodes.append(self.mv_BaseStation)

        self.calculate_plot_data()


    def calculate_coverage(self):
        
        # Making a copy of the area
        area = shapely.Polygon(self.mv_AreaPolygon)
        #print(f"Copied polygon area ", area.area)
        #print(f"Original polygon area ", self.mv_AreaPolygon.area)

        # If the nodes have been initialised
        if self.mb_NetworkReady:
            
            # Substracting their areas from the area of interest
            for node in self.ml_Nodes:
                
                if node.is_active():
                    area = area.difference(node.get_range_area())

            #print(f"Copied polygon area after substracting", area.area)


            # After the differences have been calculated, calculating the coverage percentage
            print(100 - area.area * 100 / self.mv_AreaPolygon.area)
            return 100 - area.area * 100 / self.mv_AreaPolygon.area





    def search_sink_recursive(self, node=None, path_list=None):

        for node in self.ml_Nodes:

            sink_found = False
            error_occured = False

            path = node.ml_Path
            adj = node.ml_AdjacentNodes

            while not sink_found and not error_occured:

                if len(adj) == 0:
                    error_occured = True
                    break

                distance = None
                best_node = None

                for n in adj:
                    if id(n) == id(node.ml_SinkNodes[0]):
                        path_list.append(n)
                        sink_found = True
                        break

                    temp = shapely.distance(node.ml_SinkNodes[0].get_localization(), n.get_localization())

                    if distance == None:
                        distance = temp

                    elif temp < distance:
                        best_node = n
                        distance = temp

                node.ml_Path.append(best_node)

                adj = best_node.ml_AdjacentNodes



        # Proceeds if the needed variables aren't empty
        if node != None or path_list != None:

            if node.ml_AdjacentNodes != 0:
                # 
                distance = None
                best_node = None

                for n in node.ml_AdjacentNodes:
                    if id(n) == id(node.ml_SinkNodes[0]):
                        path_list.append(n)
                        return

                    print("Sinkju")
                    print(len(node.ml_SinkNodes))
                    temp = shapely.distance(node.ml_SinkNodes[0].get_localization(), n.get_localization())

                    if distance == None:
                        distance = temp

                    elif temp < distance:
                        best_node = n
                        distance = temp

                if best_node != None:
                    path_list.append(best_node)

                    self.search_sink_recursive(best_node, path_list)


    def path_to_sink(self, node, sink, ):
        stack, path = [node], []


    def dfs(self, visited, node, sink):  #function for dfs 
        if id(node) == id(sink):
            visited.add(node)
            raise Exception("sink found")

        if node not in visited:
            visited.add(node)
            for neighbour in node.ml_AdjacentNodes:
                self.dfs(visited, neighbour, sink)  




    def naive_algorithm(self):

        #####################################
        # Nodes setup, searching for a sink #
        #####################################

        # Activating all of the nodes
        for node in self.ml_Nodes:
            node.activate()
            self.mv_ActiveNodes+=1

        # Contains a circle in which a sink has to be found
        possible_sink_location = self.mv_AreaPolygon.point_on_surface().buffer(50)

        # Current lowest distance from the middle point
        lowest_distance = None
        sink = None

        # Searching for the best sink location in the area near the middle
        for node in self.ml_Nodes:
            # If the node is inside the possible sink span
            if shapely.contains_xy(possible_sink_location, node.get_localization().coords[:]):

                # Calculating the distance between middle of the area and a node
                temp = shapely.distance(self.mv_AreaPolygon.point_on_surface(), node.get_localization())

                if lowest_distance == None:
                    lowest_distance = temp
                    sink = node
                else:
                    
                    if temp < lowest_distance:
                        lowest_distance = temp
                        sink = node

        # Adding sink nodes
        for node in self.ml_Nodes:

            # Setting the sink node in the other nodes
            node.add_sink_node(sink)

            if id(node) == id(sink):
                print("Tak bylo")
                node.mb_Sink = True

        # Adding the closest neighbours to the node within 100m
        for node in self.ml_Nodes:
            temp = node.get_range_area()

            for another_node in self.ml_Nodes:
                if id(node) != id(another_node) or node != sink:
                    
                    if (shapely.contains_xy(temp, another_node.get_localization().coords[:])):
                        # Adding a nodes that are relatively close 
                        node.add_to_neighbours_list(another_node)

            print(node.get_neighbours_amount())
        
        # Searching for a individual path to a sink for each node
        #for node in self.ml_Nodes:
            
        #self.search_sink_recursive(node, node.ml_Path)

        visited = set()

        for node in self.ml_Nodes:
            visited.clear()
            try:
                self.dfs(visited, node, sink)
            except:
                print("Path to the sink found!")
                for v in visited:
                    node.add_to_path(v)
                print(len(node.ml_Path))

        # Calculating coverage for the test
        # Can assume that the coverage is the overall percent of the network as is, while discarding the area approach
        # crappy apporach
        # and can calculate the coverage by using shapely.difference(Area, sensor range) and substracting all of the sensors
        # area from the overall network area, then calculating the percentile coverage.

        while self.calculate_coverage() > self.mv_MinimumCoverage:

            transfer_done = False
            print(self.mv_ActiveNodes)

            for node in self.ml_Nodes:
                if node.is_active() and len(node.ml_Path) > 0:
                    node.transmit_data(int(shapely.distance(node.get_localization(), node.ml_Path[0].get_localization())))
                    self.calculate_plot_data()
                    if len(node.ml_Path) > 1:
                        for element in node.ml_Path:
                            if element.is_active():
                                if id(element) != id(sink):
                                    element.aggregate_data(int(shapely.distance(node.get_localization(), element.get_localization())))
                                    self.calculate_plot_data()
                                else:
                                    element.receive_data()
                                    self.calculate_plot_data()
                                transfer_done = True
                            else:
                                node.deactivate()
                else:
                    continue

            if not transfer_done:
                print("Out!")
                break

            for node in self.ml_Nodes:
                if node.get_battery_level() < 5 and node.is_active():
                    self.mv_ActiveNodes-=1
                    node.deactivate()

            if self.mv_ActiveNodes == 0:
                print("Out?")
                break

    
    # Iterative naive algorithm
    def naive_algorithm_new(self):

        #####################################
        # Nodes setup, searching for a sink #
        #####################################

        for node in self.ml_Nodes:
            if not node.is_base_station():
                node.set_base_station(self.mv_BaseStation)
                node.activate()
                self.mv_ActiveNodes+=1

        # Sending hello message to the base station
        for node in self.ml_Nodes:
            if node.is_active():
                node.transmit_status(int(shapely.distance(node.get_localization(), self.mv_BaseStation.get_localization())))

        while self.calculate_coverage() > self.mv_MinimumCoverage:

            print(self.mv_ActiveNodes)

            for node in self.ml_Nodes:
                if node.is_active():
                    node.transmit_data(int(shapely.distance(node.get_localization(), self.mv_BaseStation.get_localization())))

            for node in self.ml_Nodes:
                if node.get_battery_level() < 5 and node.is_active():
                    node.deactivate()
                    self.mv_ActiveNodes-=1

            if self.mv_ActiveNodes == 0:
                break
            
    #############################################
    # Here is the biggest thing of this program #
    #############################################

    # The PSO algorithm that implements the Fitness functions etc.
    def pso_algorithm(self):

        print()

    
    def calculate_plot_data(self):

        self.ml_xAxisPlotData = []
        self.ml_yAxisPlotData = []
        self.ml_ColorPlotData = []

        for node in self.ml_Nodes:
            self.ml_xAxisPlotData.append(node.get_localization().coords[:][0][0])
            self.ml_yAxisPlotData.append(node.get_localization().coords[:][0][1])
            self.ml_ColorPlotData.append(node.mv_Color)
    

    def get_plot_data(self):

        return [self.ml_xAxisPlotData, self.ml_yAxisPlotData, self.ml_ColorPlotData]


    def cleanup_after_simulation(self):
        for node in self.ml_Nodes:
            node.ml_AdjacentNodes.clear()
            node.ml_AggregatingNodes.clear()
            node.ml_SinkNodes.clear()
            node.ml_Path.clear()
            node.set_battery_capacity(self.mv_BatteryCapacity)
            node.deactivate()

        self.mv_ActiveNodes = 0

        self.ml_SinkNodes.clear()


