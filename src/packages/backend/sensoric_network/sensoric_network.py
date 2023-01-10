
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


    #######################
    # Methods definitions #
    #######################


    # A constructor. Takes the amount of nodes,
    # battery capacity, lower left and upper right point of the area covered by sensors as params
    def __init__(self, node_amount=int(10), battery_capacity=int(500),
    x_l=int(0), y_l=int(0), x_u=int(1000), y_u=int(1000), minimum_coverage=int(70)):

        ###########
        # Approaches choice variables #
        ###########

        # List containing the possible solutions to the problem of maximisation of the lifetime expectancy
        self.ml_SolutionType = ["Centralised", "Decentralised"]

        # Proposed algorithms for the centralised approach, dispatched by this object
        # assuming that it is a gateway of the whole WSN. This object is then responsible for 
        # simulating the data collection functionality and all of the management
        self.ml_CentralisedAlgorithms = ["naive"]

        # Proposed algorithms for the decentralised approach, which will be dispatched mainly
        # by the nodes themselves. This object will only send signals about the data collection,
        # the rest should be carried out by the nodes with the help of the neighbour list
        # The data transmission will recursive with limited amount of hops to transfer the data to the sink
        self.ml_DecentralisedAlgorithms = []


        # List containing the names of the implemented approaches to improving the lifetime of a WSN
        self.ml_Algorithms = ["naive", "Particle-Swarm-Optimisation"]

        #####################
        # Network variables #
        #####################

        # Setting a list of points temporarily, in order to create a polygon
        self.ml_AreaPoints = [shapely.Point(x_l, y_l), shapely.Point(x_u, y_l), shapely.Point(x_u, y_u), shapely.Point(x_l, y_u)]

        # Contains the area polygon
        self.mv_Area = shapely.Polygon([[p.x, p.y] for p in self.ml_AreaPoints])

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

        ############
        # Booleans #
        ############

        # Activated after every call on "Collect data" on the nodes
        self.mb_DataCollectionRequestSent = False

        # Activated after the initialisation of the nodes, by that I mean:
        # location has been assigned and parameters like cell capacity are correct
        self.mb_NodesInitialised = False

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


    # Sets the nodes amount
    def set_node_amount(self, amount):
        self.mv_NodeAmount = amount


    # Sets the battery capacity in mAH
    def set_node_battery_capacity(self, capacity):
        self.mv_BatteryCapacity = capacity


    def set_height(self, h=int):
        print()
        #points = [self.ml_AreaPoints[0], self.ml_AreaPoints[1], shapely.]


    # Changes the area of the network
    def set_area(self, x_l=int, y_l=int, x_u=int, y_u=int):

        # Setting a list of points temporarily, in order to create a polygon
        self.ml_AreaPoints = [shapely.Point(x_l, y_l), shapely.Point(x_u, y_l), shapely.Point(x_u, y_u), shapely.Point(x_l, y_u)]

        # Creating a polygon out of the points from above
        self.mv_Area = shapely.Polygon([[p.x, p.y] for p in self.ml_AreaPoints])


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

        self.mb_NodesInitialised = True


    def calculate_coverage(self):
        
        # Making a copy of the area
        area = shapely.Polygon(self.mv_Area)
        #print(f"Copied polygon area ", area.area)
        #print(f"Original polygon area ", self.mv_Area.area)

        # If the nodes have been initialised
        if self.mb_NodesInitialised:
            
            # Substracting their areas from the area of interest
            for node in self.ml_Nodes:
                
                if node.is_active():
                    area = area.difference(node.get_range_area())

            #print(f"Copied polygon area after substracting", area.area)


            # After the differences have been calculated, calculating the coverage percentage
            print(100 - area.area * 100 / self.mv_Area.area)
            return 100 - area.area * 100 / self.mv_Area.area





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
        possible_sink_location = self.mv_Area.point_on_surface().buffer(200)

        # Current lowest distance from the middle point
        lowest_distance = None
        sink = None

        # Searching for the best sink location in the area near the middle
        for node in self.ml_Nodes:
            # If the node is inside the possible sink span
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
                    node.transmit_data(10000*int(shapely.distance(node.get_localization(), node.ml_Path[0].get_localization())))
                    if len(node.ml_Path) > 1:
                        for element in node.ml_Path:
                            if element.is_active():
                                if id(element) != id(sink):
                                    element.aggregate_data(10000*int(shapely.distance(node.get_localization(), element.get_localization())))
                                else:
                                    element.receive_data(10000*int(shapely.distance(node.get_localization(), element.get_localization())))
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




    def run_simulation(self):

        print("Not yet")

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


    


