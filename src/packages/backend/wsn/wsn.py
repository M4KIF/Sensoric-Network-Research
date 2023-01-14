
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
import math
import random
import shapely



#####################
# Object definition #
#####################


# Particle class for the PSO algorithm
class Particle():


    # Constructor with a few parameters that enable quick initialisation of the particle
    def __init__(self, position=shapely.Point(0,0), velocity=float(0.0), linked_to=None):

        # Setting the postion a initial value, defaults to (0,0)
        self.mv_Position = position

        # Setting the velocity an initial value, defaults to 0
        self.mv_Velocity = velocity

        #  the refference to the node that the particle is linked with
        self.mv_LinkedTo = linked_to

        # Setting the pBest initial value of None
        self.mv_pBest = None

        # Setting the personal fitness value to 0
        self.mv_pFitness = 0

        # Setting the global fitness value to 0
        self.mv_gFitness = 0

    
    #############################
    # Member methods definition #
    #############################


    # Sets the current particle positon after updating the value in the algorithm
    def set_position(self, position):
        self.mv_Position = position

    
    # Sets the current particle velocity after updating the value in the algorithm
    def set_velocity(self, velocity):
        self.mv_Velocity = velocity


    # Sets the best particle positon after deciding in the algorithm
    def set_pbest(self, best_positon):
        self.mv_pBest = best_positon


    # Sets the personal fitness value
    def set_pfitness(self, fitness):
        self.mv_pFitness = fitness


    # Sets the global fitness value
    def set_gfitness(self, fitness):
        self.mv_gFitness = fitness

    
    # Gets the position
    def get_position(self):
        return self.mv_Position


    # Gets the velocity
    def get_velocity(self):
        return self.mv_Velocity


    # Gets the pBest
    def get_pbest(self):
        return self.mv_pBest


    # Gets the personal fitness value
    def get_pfitness(self):
        return self.mv_pFitness


    # Gets the global fitness value
        return self.mv_gFitness


# The main sensoric network object with all of the network's funcitonality
class SensoricNetwork():


    #######################
    # Methods definitions #
    #######################


    # A constructor. Takes the amount of nodes,
    # battery capacity, lower left and upper right point of the area covered by sensors as params
    def __init__(self, node_amount=int(10), battery_capacity=int(50), height=int(1000), width=int(1000),
    minimum_coverage=int(70)):

        ###############################
        # Approaches choice variables #
        ###############################

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

        # Not neccesary
        #self.ml_Nodes.append(self.mv_BaseStation)

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

    
    def calculate_optimal_clasters_amount(self, radius_start, radius_max, area, dist_max, h_value):
        a = area
        R = radius_start
        d_m = dist_max
        r = 0
        c = 0

        while a > 0:
            a-=math.pi*(math.pow((2*R+r), 2) - pow(r, 2))
            c+=(math.pi*pow((2*R+ r),2)-math.pi*pow(r, 2))/math.pi*pow(R, 2)
            r+=2*R
            R = (r*(radius_max-radius_start)+radius_start*dist_max)/(dist_max-radius_max+radius_start)

        c*=h_value

        return c


    # Calculate nodes contained inside the CH candidate circle area
    def amount_of_nodes_intersecting(self, particle, radius):

        # The polygon which I will check
        area = particle.linked_to.get_localization().buffer(radius)

        # The amount of particles contained
        amount_contained = 0

        # Calculating the number of nodes that are contained withing the area of the CH candidate
        for node in self.ml_Nodes:
            if area.intersects(node.get_localization()):
                amount_contained+=1

        return amount_contained


    # Calculates the amount of nodes that intersect and compares over universal set(total nodes amount)
    def check_circle_area_intersections(self, particle, radius, particle_radius_list):

        # The polygon that I will check for nodes in intersection between a second circle
        area = particle.linked_to.get_localization().buffer(radius)
        particles_in_intersection = set()
        i = 0

        for node in self.ml_Nodes:

            temp = node.buffer(particle_radius_list[i])

            if shapely.intersects(area, temp):
                inter = shapely.intersection(area, temp)
                
                for comp_node in self.ml_Nodes:
                    if shapely.intersects_xy(inter, comp_node.get_localization()):
                        particles_in_intersection+=id(comp_node)


            i+=1

        # Returning the value
        return len(particles_in_intersection)


    def velocity(self):
        print()



    def position(self):
        print()



    # Calculates the fitness parameter without IoT
    def fitness(self, particle, radius):

        # The area which I will check
        area = particle.linked_to.get_localization().buffer(radius)

        # The amount of particles contained
        amount_contained = self.amount_of_nodes_intersecting(particle, radius)

        # Calculating the ideal amount of particles possible for this network
        amount_max_possible = area.area * (self.mv_NodeAmount / self.mv_AreaPolygon.area)             

        # Calculating the fitness value
        fitness_value = math.abs(amount_contained - amount_max_possible)

        # Returning the calculated value
        return fitness_value


    # Calculates the fitness parameter with IoT
    def Fitness(self, particle, radius):
        
        # Assuming that alpha = 0.9
        alpha = 0.9

        # Returning the value
        return (alpha * (self.amount_of_nodes_intersecting(particle, radius)/self.mv_NodeAmount) 
        + (1 - alpha)/(self.check_circle_area_intersections(particle, radius)/self.mv_NodeAmount))

    def Weight(self, particle, radius):

        #
        weight_1 = 0.8
        weight_2 = 0.05
        weight_3 = 0.15

        # Calculating nodes in communication range
        area = particle.linked_to.get_localization().buffer(particle.linked_to.get_communication_range())

        nodes_in_range = 0

        for node in self.ml_Nodes:
            
            if shapely.intersects_xy(area, node.get_locatlization()):
                nodes_in_range+=1

        # Calculating minimum distance from the CH candidates in the circle area
        area = particle.linked_to.get_localization().buffer(radius)

        minimum_distance = 100000

        for node in self.ml_Nodes:
            if shapely.intersects_xy(area, node.get_localization()):
                temp = shapely.distance(node.get_localization(), self.mv_BaseStation.get_localization())

                if temp < minimum_distance:
                    minimum_distance=temp
                

        weight = (weight_1 * (particle.get_battery_level() * 100) + 
            weight_2 * (nodes_in_range/self.mv_NodeAmount) +
            weight_3 * (minimum_distance/shapely.distance(particle.get_localization(), self.mv_BaseStation.get_localization())))




    # The PSO algorithm that implements the Fitness functions etc.
    def pso_algorithm(self):

        ###############
        # Setup phase #
        ###############

        # Particles list
        particles = []

        # Initialising the particles
        for node in self.ml_Nodes:
            particles.append(Particle(node.get_localization(),0.0, node))

        # The maximum radius of the cluster
        radius_max = self.mv_BaseStation.get_amplifier_threshold_distance()/2

        # The minimum radius of the cluster
        radius_min = math.sqrt(self.mv_AreaPolygon.area/math.pi*self.mv_NodeAmount)

        # A list that contains the distances between a node and a basenode
        distance_from_bn = [node.get_localization().distance(self.mv_BaseStation) for node in self.ml_Nodes]

        # Finding the maximum distance between possible CH and BN
        dis_max = max(distance_from_bn)

        # Calculating the optimal amount of circular clasters for this network, keeping in mind that H = 1
        C = self.calculate_optimal_clasters_amount(radius_start=radius_min, radius_max=radius_max
        , area=self.mv_AreaPolygon.area, dist_max=dis_max, h_value=1)

        # The list of optimal radius values per particle(node)
        particle_radius = [(dis/dis_max * (radius_max - radius_min) + radius_min) for dis in distance_from_bn]

        personal_best = []

        # Calculating the optimal circular area for each CH candidate
        for i in range(len(self.ml_Nodes)):
            personal_best.append(self.fitness(self.particles[i], particle_radius[i]))

        global_best = personal_best.copy()

        for i in range(2500):
            for j in range(len(particles)):
                


        ######################
        # Steady-state phase #
        ######################



        ######################

    
    def calculate_plot_data(self):

        self.ml_xAxisPlotData = []
        self.ml_yAxisPlotData = []
        self.ml_ColorPlotData = []

        for node in self.ml_Nodes:
            self.ml_xAxisPlotData.append(node.get_localization().coords[:][0][0])
            self.ml_yAxisPlotData.append(node.get_localization().coords[:][0][1])
            self.ml_ColorPlotData.append(node.mv_Color)

        # Adding the base station to the list
        self.ml_xAxisPlotData.append(self.mv_BaseStation.get_localization().coords[:][0][0])
        self.ml_yAxisPlotData.append(self.mv_BaseStation.coords[:][0][1])
        self.ml_ColorPlotData.append(self.mv_BaseStation.mv_Color)
    

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


