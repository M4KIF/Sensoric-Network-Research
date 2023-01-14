
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

        # Setting the x velocity an initial value, defaults to 0
        self.mv_xVelocity = velocity

        # Setting the z velocity an initial value, defaults to 0
        self.mv_zVelocity = velocity

        #  the refference to the node that the particle is linked with
        self.mv_LinkedTo = linked_to

        # Setting the pBest initial value of None
        self.mv_pBest = None

        # Setting the gBest initial value to None
        self.mv_gBest = None

        # Setting the personal fitness value to 0
        self.mv_pFitness = 0

        # Setting the global fitness value to 0
        self.mv_gFitness = 0

        # Setting Candidate CH circular area radius
        self.mv_Radius = 0

    
    #############################
    # Member methods definition #
    #############################


    # Sets the current particle positon after updating the value in the algorithm
    def set_position(self, position):
        self.mv_Position = position

    
    # Sets the current particle x velocity after updating the value in the algorithm
    def set_x_velocity(self, velocity):
        self.mv_xVelocity = velocity


    # Sets the current particle z velocity after updating the value in the algorithm
    def set_z_velocity(self, velocity):
        self.mv_zVelocity = velocity


    # Sets the best particle positon after deciding in the algorithm
    def set_pbest(self, best_positon):
        self.mv_pBest = best_positon


    # Sets the global best position value
    def set_gbest(self, best_position):
        self.mv_gBest = best_position


    # Sets the personal fitness value
    def set_pfitness(self, fitness):
        self.mv_pFitness = fitness


    # Sets the global fitness value
    def set_gfitness(self, fitness):
        self.mv_gFitness = fitness


    # Sets the circular area radius value
    def set_radius(self, radius):
        self.mv_Radius = radius

    
    # Gets the position
    def get_position(self):
        return self.mv_Position


    def get_x_position(self):
        return self.mv_Position.coords[:][0][0]


    def get_z_position(self):
        return self.mv_Position.coords[:][0][1]


    # Gets the x velocity
    def get_x_velocity(self):
        return self.mv_xVelocity


    # Gets the z velocity
    def get_z_velocity(self):
        return self.mv_zVelocity


    # Gets the pBest
    def get_pbest(self):
        return self.mv_pBest


    # Gets the gBest
    def get_gbest(self):
        return self.mv_gBest


    # Gets the personal fitness value
    def get_pfitness(self):
        return self.mv_pFitness


    # Gets the global fitness value
    def get_gfitness(self):
        return self.mv_gFitness


    # Gets the radius value
    def get_radius(self):
        return self.mv_Radius


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

        # Max iterations of the PSO algorithm, should be 2500
        self.mv_MaxIteration = 10

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
    def amount_of_nodes_in_area(self, area):

        # The amount of particles contained
        amount_contained = 0

        # Calculating the number of nodes that are contained withing the area of the CH candidate
        for node in self.ml_Nodes:
            if shapely.intersects(area, node.get_localization()):
                amount_contained+=1

        return amount_contained


    # Calculates the amount of nodes that intersect and compares over universal set(total nodes amount)
    def IoU(self, particle_compared, particles):

        # The polygon that I will check for nodes in intersection between a second circle
        point = particle_compared.get_position()
        area = point.buffer(particle_compared.get_radius())

        # Contains all of the particles found in the intersections
        particles_in_intersections = set()

        for p in particles:
            if id(particle_compared) != id(p):
                temp = p.get_position().buffer(p.get_radius())

                if shapely.intersects(area, temp):
                    intersection = shapely.intersection(area, temp)

                    if not intersection.area == 0:

                        for node in self.ml_Nodes:

                            if shapely.contains(intersection, node.get_localization()):
                                particles_in_intersections.add(id(node))

        # Returning the value
        return len(particles_in_intersections)


    # Calculates and updates the x and z velocity of the particle
    def update_velocity(self, particle, iteration):

        # Constants
        w_max = 0.9
        w_min = 0.4

        # Acceleration coefficients
        c1 = 1
        c2 = 2

        # Calculating the w value
        w = w_max - (w_max-w_min)/self.mv_MaxIteration * iteration

        # X coordinate calculations, the velocity is understood as "meters" per iteration of the algorithm
        particle.set_x_velocity(
            w * particle.get_x_velocity() +
            c1 * random.randrange(0, 1) * (particle.get_pbest().get_position().coords[:][0][0] - particle.get_x_velocity()) +
            c2 * random.randrange(0, 1) * (particle.get_gbest().get_position().coords[:][0][0] - particle.get_x_velocity())
        )

        particle.set_z_velocity(
            w * particle.get_z_velocity() +
            c1 * random.randrange(0, 1) * (particle.get_pbest().get_position().coords[:][0][1] - particle.get_z_velocity()) +
            c2 * random.randrange(0, 1) * (particle.get_gbest().get_position().coords[:][0][1] - particle.get_z_velocity())
        )


    # 
    def update_position(self, particle):
        
        particle.set_position(
            shapely.Point(
                particle.get_x_position() + particle.get_x_velocity(),
                particle.get_z_position() + particle.get_z_velocity()
            )
        )



    # Calculates the fitness parameter without IoT
    def fitness(self, particle):

        # Area of the circular area
        point = particle.get_position()
        area = point.buffer(particle.get_radius())

        # The amount of particles contained
        amount_contained = self.amount_of_nodes_in_area(area)

        # Calculating the ideal amount of particles possible for this network
        amount_max_possible = area.area * (self.mv_NodeAmount / self.mv_AreaPolygon.area)             

        # Calculating the fitness value
        fitness_value = math.fabs(amount_contained - amount_max_possible)

        # Returning the calculated value
        return fitness_value


    # Calculates the fitness parameter with IoT
    def Fitness(self, particle, particles):

        point = particle.get_position()
        area = point.buffer(particle.get_radius())
        
        # Assuming that alpha = 0.9
        alpha = 0.9

        # IoU value
        iou = self.IoU(particle, particles)

        # Checking if calculating global Fitness is the right choice here
        if iou == 0:
            raise ValueError("IoU==0")

        # Returning the value
        return (alpha * (self.amount_of_nodes_in_area(area)/self.mv_NodeAmount) 
        + (1 - alpha)/(iou/self.mv_NodeAmount))

    def Weight(self, node):

        #
        weight_1 = 0.8
        weight_2 = 0.05
        weight_3 = 0.15

        # Searching for nodes in communication range
        area = node.get_localization().buffer(node.get_communication_range())

        nodes_in_range = []

        for n in self.ml_Nodes:
            
            if id(node)!=id(n):
                if shapely.intersects(area, n.get_localization()):
                    nodes_in_range.append(n)

        # Calculating minimum distance from the CH candidates to the BN

        minimum_distance = 100000

        for n in nodes_in_range:
            temp = shapely.distance(self.mv_BaseStation.get_localization(), n.get_localization())
            if temp < minimum_distance:
                minimum_distance = temp
                
        weight = (weight_1 * (node.get_battery_level() * 100) + 
            weight_2 * (nodes_in_range/self.mv_NodeAmount) +
            weight_3 * (minimum_distance/shapely.distance(node.get_localization(), self.mv_BaseStation.get_localization())))

        print(weight)
        return weight


    # The PSO algorithm that implements the Fitness functions etc.
    def pso_algorithm(self):

        ###############
        # Setup phase #
        ###############

        particles = []

        # Initialising the particles with Nodes positions
        for node in self.ml_Nodes:
            particles.append(Particle(position=node.get_localization(), velocity=10, linked_to=node))

        # Calculating the max distance from the base node
        dis_max = max([shapely.distance(node.get_localization(), self.mv_BaseStation.get_localization()) for node in self.ml_Nodes])

        # The maximum radius of the cluster
        radius_max = self.mv_BaseStation.get_amplifier_threshold_distance()/2

        # The minimum radius of the cluster
        radius_min = math.sqrt(self.mv_AreaPolygon.area/math.pi*self.mv_NodeAmount)

        # Initialising the radius inside the particle
        for particle in particles:
            # Calculating the distance from the particle to the base node
            dis = shapely.distance(particle.get_position(), self.mv_BaseStation.get_localization())

            # Calculating and setting the particle radius
            particle.set_radius((dis/dis_max * (radius_max - radius_min) + radius_min))

            particle.set_pfitness(self.fitness(particle))

            # Using a shortcut, setting the pbest as particle, and not a point, for easier calculations
            particle.set_pbest(particle)

        gbest = particles[0].get_pbest()

        # Setting the global best as the current p_best temporarily
        for particle in particles:
            particle.set_gbest(gbest)

        # List containing all of the historical gbest's
        gbest_values = []

        # Repeating the algorithm for a set amount of time
        for i in range(self.mv_MaxIteration):

            # Iterating through the particles
            for j in range(len(particles)):

                # Updating the velocity of the particle
                self.update_velocity(particles[j], i)

                # Updating the position of the particle based on the velocity
                self.update_position(particle=particles[j])

                # Calculating the distance from the particle to the base node
                dis = shapely.distance(particles[j].get_position(), self.mv_BaseStation.get_localization())

                # Calculating and setting the particle radius
                particles[j].set_radius((dis/dis_max * (radius_max - radius_min) + radius_min))

                # Calculating fitness values
                fitness_particle = self.fitness(particles[j])

                # If the particle doesn't have any neighbours it is automatically added to the best particles list
                # But its fitness cannot be added as the value is incorrect
                try:
                    fitness_population = self.Fitness(particles[j], particles)
                except ValueError as err:
                    if fitness_particle < self.fitness(particles[j].get_pbest()):
                        particles[j].set_pbest(particles[j])
                    
                    gbest_values.append(particles[j])
                    continue

                # Conditionals
                if fitness_particle < self.fitness(particles[j].get_pbest()):
                    particles[j].set_pbest(particles[j])
                try:
                    if fitness_population < self.Fitness(gbest, particles):
                        gbest = particles[j]
                        gbest_values.append(gbest)

                        for particle in particles:
                            particle.set_gbest(gbest)
                except ValueError as err:
                    continue

            print(particles[0].get_position())
        
        ch_nodes_candidates = []

        for particle in gbest_values:
            
            if self.IoU(particle, gbest_values) > 0.7:
                continue
            else:
                ch_nodes_candidates.append(particle)

        ch_nodes = []

        for particle in ch_nodes_candidates:

            # Calculating the polygon of the candidate area
            point = particle.get_position()
            area = point.buffer(particle.get_radius())

            nodes_to_check = []

            # Checking for nodes that are in the candidate area
            for node in self.ml_Nodes:

                if shapely.contains(area, node.get_localization()):
                    nodes_to_check.append(node)

            ch = (None, -1)

            # Checking the weights of the nodes
            for node in nodes_to_check:
                
                temp = self.Weight(node)

                if temp > ch[1]:
                    ch = (node, temp)
            
            ch_nodes.append(ch)

        for node in ch_nodes:
            print(id(node[1]))
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
        self.ml_yAxisPlotData.append(self.mv_BaseStation.get_localization().coords[:][0][1])
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


