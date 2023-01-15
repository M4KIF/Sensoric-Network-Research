


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

# For setting the nodes in places
from numpy.random import uniform

# For the calculations
import math

# Mainly for setting randomised values in pso formulas
import random

# Geographical functionality
import shapely

# Threading support
from PyQt5.QtCore import pyqtSignal, QObject, QMutex


#####################
# Object definition #
#####################


# Particle class for the PSO algorithm
class Particle():


    # Constructor with a few parameters that enable quick initialisation of the particle
    def __init__(self, position=shapely.Point(0,0), velocity=float(0.0), pfitness=None, pbest=None):

        # Setting the postion a initial value, defaults to (0,0)
        self.mv_Position = position

        # Setting the x velocity an initial value, defaults to 0
        self.mv_xVelocity = velocity

        # Setting the z velocity an initial value, defaults to 0
        self.mv_zVelocity = velocity

        # Setting the pBest initial value of None
        self.mv_pBest = pbest

        # Setting the gBest initial value to None
        self.mv_gBest = None

        # Setting the personal fitness value to 0
        self.mv_pFitness = pfitness

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
class SensoricNetwork(QObject):


    #####################
    # Threading support #
    #####################

    # Mutex object for securing the memory changes
    mutex = QMutex()

    # Setters signals
    signal_set_height = pyqtSignal(int)

    signal_set_width = pyqtSignal(int)

    signal_set_area_dimensions = pyqtSignal([int, int])

    signal_set_node_amount = pyqtSignal(int)

    signal_set_node_battery_capacity = pyqtSignal(int)

    signal_set_minimum_coverage_value = pyqtSignal(int)

    signal_set_algorithm = pyqtSignal(int)

    # Getter signals
    signal_get_height = pyqtSignal()

    signal_get_width = pyqtSignal()

    signal_get_node_amount = pyqtSignal()

    signal_get_node_battery_capacity = pyqtSignal()

    signal_get_minimum_coverage_value = pyqtSignal()

    signal_get_current_algorithm = pyqtSignal()

    signal_get_rounds = pyqtSignal()

    signal_get_algorithms_list = pyqtSignal()

    signal_get_plot_data = pyqtSignal()

    # Data sending signals
    signal_send_rounds = pyqtSignal(list)

    signal_send_height = pyqtSignal(int)

    signal_send_width = pyqtSignal(int)

    signal_send_node_amount = pyqtSignal(int)

    signal_send_node_capacity = pyqtSignal(int)

    signal_send_minimum_coverage = pyqtSignal(int)

    signal_send_algorithms_list = pyqtSignal(list)

    signal_send_current_algorithm = pyqtSignal(int)

    signal_send_plot_data = pyqtSignal(list)

    # Other methods
    signal_run_pso_simulation = pyqtSignal()

    signal_run_naive_simulation = pyqtSignal()



    #######################
    # Methods definitions #
    #######################


    # A constructor. Takes the amount of nodes,
    # battery capacity, lower left and upper right point of the area covered by sensors as params
    def __init__(self, node_amount=int(10), battery_capacity=int(50), height=int(1000), width=int(1000),
    minimum_coverage=int(70)):


        #######################################
        # Connecting signals to the functions #
        #######################################



        ###############################
        # Approaches choice variables #
        ###############################

        # List containing the names of the implemented approaches to improving the lifetime of a WSN
        self.ml_Algorithms = ["naive", "pso"]

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
        self.ml_Clusters = []

        # 
        self.ml_NodeToBaseNode = []

        # 
        self.ml_ClusterHeads = set()

        ######################
        # Simulation results #
        ######################

        # Marks the round in which first node dies
        self.mv_FND = 0

        # Marks the round in which half of the node is dead
        self.mv_HND = 0

        # Marks the round in which the last node dies,
        # after which the coverage drops below threshold
        self.mv_LND = 0

        #################
        # Miscellaneous #
        #################

        # Max iterations of the PSO algorithm, should be 2500
        self.mv_MaxIteration = 2000

        # Currently used algorithm
        self.mv_CurrentAlgorithm = self.ml_Algorithms[0]

        # Stores the plot data
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
        self.mb_Ready = False

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

        #
        self.mb_FirstNodeDied = False
        self.mb_HalfNodesDies = False
        self.mb_LastNodeDied = False


    ##############################
    # Member methods definitions #
    ##############################


    #####################
    # Setters / Getters #
    #####################


    # Sets the height of the networks area
    def set_height(self, height=int):

        # Setting the height
        self.mv_Height = height

        # Deactivating the ready flag
        self.mb_Ready = False
        self.mb_NodesInitialised = False

        # Recreating the Area bounds and the polygon
        self.ml_AreaBounds = [shapely.Point(0, 0), shapely.Point(self.mv_Width, 0), shapely.Point(self.mv_Width, height), shapely.Point(0, height)]
        self.mv_AreaPolygon = shapely.Polygon([[p.x, p.y] for p in self.ml_AreaBounds])

        # After changing the dimensions I have to reinitiate the network partly
        for node in self.ml_Nodes:
            node.clear()

        self.ml_SinkNodes.clear()
        self.ml_Nodes.clear()
        self.ml_Clusters.clear()
        
        self.initiate_network()


    # Sets the width of the networks area
    def set_width(self, width=int):

        # Setting the width
        self.mv_Width = width

        # Deactivating the ready flag
        self.mb_Ready = False
        self.mb_NodesInitialised = False

        # Recreating the Area bounds and the polygon
        self.ml_AreaBounds = [shapely.Point(0, 0), shapely.Point(width, 0), shapely.Point(width, self.mv_Height), shapely.Point(0, self.mv_Height)]
        self.mv_AreaPolygon = shapely.Polygon([[p.x, p.y] for p in self.ml_AreaBounds])

        # After changing the dimensions I have to reinitiate the network partly
        for node in self.ml_Nodes:
            node.clear()

        self.ml_SinkNodes.clear()
        self.ml_Nodes.clear()
        self.ml_Clusters.clear()
        
        self.initiate_network()


    # Changes both the height and the width of the area
    def set_area_dimensions(self, height=int, width=int):

        # Setting the height
        self.mv_Width = width

        # Setting the height
        self.mv_Height = height    

        # Deactivating the ready flag
        self.mb_Ready = False
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
        self.ml_Clusters.clear()
        
        self.initiate_network()


    # Sets the nodes amount
    def set_node_amount(self, amount):
        self.mv_NodeAmount = amount

        # Deactivating the ready flag
        self.mb_Ready = False
        self.mb_NodesInitialised = False

        # After changing the dimensions I have to reinitiate the network partly
        for node in self.ml_Nodes:
            node.clear()

        self.ml_SinkNodes.clear()
        self.ml_Nodes.clear()
        self.ml_Clusters.clear()
        
        self.initiate_network()


    # Sets the battery capacity in mAH
    def set_node_battery_capacity(self, capacity):
        self.mv_BatteryCapacity = capacity

        for node in self.ml_Nodes:
            node.set_battery_capacity(self.mv_BatteryCapacity)


    # Changes the minimum coverage value
    def set_minimum_coverage_value(self, percent_of_area=int):
        self.mv_MinimumCoverage=percent_of_area


    # Sets the current algorithm
    def set_algorithm(self, index=int):
        self.mv_CurrentAlgorithm = self.ml_Algorithms[index]


    # Setting a sink node
    def set_sink_node(self, node_number=int):
        sink = id(self.ml_Nodes[node_number])

        self.ml_SinkNodes.append(sink)

        for node in self.ml_Nodes:
            node.set_sink_node(self.ml_Nodes[node_number])


    #
    def get_height(self):
        return self.mv_Height


    #
    def get_width(self):
        return self.mv_Width


    #
    def get_node_amount(self):
        return self.mv_NodeAmount


    #
    def get_node_battery_capacity(self):
        return self.mv_BatteryCapacity


    def get_minimum_coverage_value(self):
        return self.mv_MinimumCoverage


    def get_current_algorithm(self):
        return self.mv_CurrentAlgorithm


    # Returns the value of rounds that a simulation has passed
    def get_rounds(self):
        # 0 - first node died
        # 1 - half nodes died
        # 2 - last node died
        return [self.mv_FND, self.mv_HND, self.mv_LND]


    #
    def get_algorithms_list(self):
        return self.ml_Algorithms


    #
    def get_plot_data(self):
        return [self.ml_xAxisPlotData, self.ml_yAxisPlotData, self.ml_ColorPlotData]


    #########################
    # Network setup methods #
    #########################


    # Initialises the network with stored parameters, random = uniform distribution for nodes placement
    def initiate_network(self):

        # Creating the sensors
        for i in range(self.mv_NodeAmount):

            # Creating a node with given battery capacity and random points taken from the area that shall be covered
            self.ml_Nodes.append(components.Node(self.mv_BatteryCapacity, uniform(0.0, self.mv_Width), uniform(0.0, self.mv_Height)))

        # Creating the base station
        self.mv_BaseStation=components.Node(
            self.mv_BatteryCapacity, self.mv_AreaPolygon.point_on_surface().coords[:][0][0], 
            self.mv_AreaPolygon.point_on_surface().coords[:][0][1]
            )

        # Activating the correct flag on the node
        self.mv_BaseStation.activate_base_station_flag()

        # Setting the base station across the nodes
        for node in self.ml_Nodes:
            node.set_base_station(self.mv_BaseStation)

        # Activating the flag indicating that the network is ready for a simulation
        self.mb_Ready = True

        self.calculate_plot_data()


    # Calculates the current coverage of the network
    def calculate_coverage(self):

        # It is a value of active nodes to total amount of nodes
        return (self.mv_ActiveNodes * 100) / self.mv_NodeAmount


    ###################################
    # Naive routing sollution methods #
    ###################################


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
            temp = node.get_sensing_range_area()

            for another_node in self.ml_Nodes:
                if id(node) != id(another_node) or node != sink:
                    
                    if (shapely.contains_xy(temp, another_node.get_localization().coords[:])):
                        # Adding a nodes that are relatively close 
                        node.add_to_neighbours_list(another_node)

            print(node.get_neighbours_amount())

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

        if not self.mb_Ready:
            self.initiate_network()

        #####################################
        # Nodes setup, searching for a sink #
        #####################################

        for node in self.ml_Nodes:
            node.activate()
            self.mv_ActiveNodes+=1

        self.mv_LND = 0

        while self.calculate_coverage() > self.mv_MinimumCoverage:

            for node in self.ml_Nodes:
                if node.is_active():
                    node.transmit_data(shapely.distance(node.get_localization(), self.mv_BaseStation.get_localization()))

            for node in self.ml_Nodes:
                if node.get_battery_level() < 2 and node.is_active():
                    node.deactivate()
                    self.mv_ActiveNodes-=1

                    if self.mb_FirstNodeDied and self.mv_ActiveNodes == (self.mv_NodeAmount-1):
                        self.mv_FND = self.mv_LND
                        self.mb_FirstNodeDied = True
                    
                    if (self.mb_HalfNodesDies and
                    (self.mv_ActiveNodes == self.mv_NodeAmount - int((self.mv_MinimumCoverage/100)*self.mv_NodeAmount))):
                        self.mv_HND = self.mv_LND
                        self.mb_HalfNodesDies = True

            self.mv_LND += 1

        print(self.mv_LND)
        self.mb_LastNodeDied = True

            
    ###############################################
    # Particle Swarm Optimisation routing methods #
    ###############################################

    
    #
    def calculate_optimal_clasters_amount(self, radius_start, radius_max, area, dist_max, h_value):
        a = area
        R = radius_start
        d_m = dist_max
        r = 0
        c = 0

        while a > 0:
            a-=math.pi*(math.pow((2*R+r), 2) - pow(r, 2))
            c+=((math.pi*pow(((2 * R)+ r),2))-(math.pi*pow(r, 2)))/(math.pi*pow(R, 2))
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

                            if shapely.intersects(intersection, node.get_localization()):
                                particles_in_intersections.add(id(node))

        # Returning the value
        return len(particles_in_intersections)/len(particles)


    # Calculates and updates the x and z velocity of the particle
    def update_velocity(self, particle, iteration):

        # Constants
        w_max = 0.9
        w_min = 0.4

        # The pBest acceleration bias
        c1 = 1
        # The gBest acceleration bias
        c2 = 2

        # Random values from (0,1)
        r1 = random.random()
        r2 = random.random()

        # The values cant be equal to 0
        while r1==0:
            r1 = random.random()

        while r2==0:
            r2 = random.random()

        # Calculating the inertia value
        w = w_max - (w_max-w_min)/self.mv_MaxIteration * iteration

        velocity_x = (
                w * particle.get_x_velocity() +
                c1 * r1 * (particle.get_pbest().get_position().coords[:][0][0] - particle.get_x_velocity()) +
                c2 * r2 * (particle.get_gbest().get_position().coords[:][0][0] - particle.get_x_velocity())
            )

        velocity_z = (
                w * particle.get_z_velocity() +
                c1 * r1 * (particle.get_pbest().get_position().coords[:][0][1] - particle.get_z_velocity()) +
                c2 * r2 * (particle.get_gbest().get_position().coords[:][0][1] - particle.get_z_velocity())
            )

        particle.set_x_velocity(velocity_x)

        particle.set_z_velocity(velocity_z)


    # 
    def update_position(self, particle):  

        # If the particle will get out of bounds through the left area border after addition of the acceleration value
        # and the acceleration sign is negative, multiply by -1 
        if (particle.get_x_position() + particle.get_x_velocity()) < 0:
            if particle.get_x_velocity() < 0:
                particle.set_x_velocity(-1*particle.get_x_velocity())

        # If the particle will get out of bounds through the right area border after addition of the acceleration value
        # and the acceleration sign is positive, multiply by -1 
        if (particle.get_x_position() + particle.get_x_velocity()) > self.mv_Width:
            if particle.get_x_velocity() > 0:
                particle.set_x_velocity(-1*particle.get_x_velocity())

        # If the particle will get out of bounds through the bottom area border after addition of the acceleration value
        # and the acceleration sign is positive, multiply by -1 
        if (particle.get_z_position() + particle.get_z_velocity()) < 0:
            if particle.get_z_velocity() < 0:
                particle.set_z_velocity(-1*particle.get_z_velocity())

        # If the particle will get out of bounds through the top area border after addition of the acceleration value
        # and the acceleration sign is positive, multiply by -1 
        if (particle.get_z_position() + particle.get_z_velocity()) > self.mv_Height:
            if particle.get_z_velocity() > 0:
                particle.set_z_velocity(-1*particle.get_z_velocity())
        
        # Setting the position after correction
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
            # Returning the value without the 
            return (alpha * (self.amount_of_nodes_in_area(area)/self.mv_NodeAmount)+ (1 - alpha)/(0.0001/self.mv_NodeAmount))
        else:
            # Returning the value
            return (alpha * (self.amount_of_nodes_in_area(area)/self.mv_NodeAmount) 
            + (1 - alpha)/(iou))


    #
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
                    nodes_in_range.append(node)

        # Calculating minimum distance from the CH candidates to the BN

        minimum_distance = 100000

        for n in nodes_in_range:
            temp = shapely.distance(self.mv_BaseStation.get_localization(), n.get_localization())
            if temp < minimum_distance:
                minimum_distance = temp
                
        weight = (weight_1 * (node.get_battery_level() / 100) + 
            weight_2 * (len(nodes_in_range)/self.mv_NodeAmount) +
            weight_3 * (minimum_distance/shapely.distance(node.get_localization(), self.mv_BaseStation.get_localization())))

        return weight


    # Calculates the weight of the next hop candidate
    def hop_weight(self, node, candidate_node):
        u1=0.35
        u2=0.45
        u3=0.2

        d0 = self.mv_BaseStation.get_amplifier_threshold_distance()

        dj = shapely.distance(node.get_localization(), candidate_node.get_localization())

        Ej = candidate_node.get_battery_level()

        dv = (
            math.fabs(((self.mv_BaseStation.get_localization().coords[:][0][1] - 
            node.get_localization().coords[:][0][1])*candidate_node.get_localization().coords[:][0][0]) +
            ((node.get_localization().coords[:][0][0]-self.mv_BaseStation.get_localization().coords[:][0][0])*
            candidate_node.get_localization().coords[:][0][1])+
            (self.mv_BaseStation.get_localization().coords[:][0][0] * node.get_localization().coords[:][0][1])-
            (self.mv_BaseStation.get_localization().coords[:][0][1]*node.get_localization().coords[:][0][0]))/math.sqrt(
                pow((self.mv_BaseStation.get_localization().coords[:][0][1] - node.get_localization().coords[:][0][1]),2) +
                pow((node.get_localization().coords[:][0][0] - self.mv_BaseStation.get_localization().coords[:][0][0]), 2)
            )

        )

        return u1*(dv/d0) + u2 * (dj/d0) + u3 * (100/Ej)


    # The setup phase of the PSO algorithm
    def pso_setup(self):
        ###############
        # Setup phase #
        ###############

        self.mv_ActiveNodes = 0

        self.ml_ClusterHeads.clear()
        self.ml_NodeToBaseNode.clear()
        for cluster in self.ml_Clusters:
            cluster.clear()
        self.ml_Clusters.clear()

        # Stores the iterations value
        total_iterations = 0

        # Calculating the max distance from the base node to a node
        dis_max = max([shapely.distance(node.get_localization(), self.mv_BaseStation.get_localization()) for node in self.ml_Nodes if node.get_battery_level() > 2])

        # Calculating the maximum radius of a cluster candidate area
        radius_max = self.mv_BaseStation.get_amplifier_threshold_distance()/2

        # Calculating the minimum radius of a cluster cadidate area
        radius_min = math.sqrt(self.mv_AreaPolygon.area/(math.pi*self.mv_NodeAmount))

        # Calculating the ideal value of circular areas for this network
        C = self.calculate_optimal_clasters_amount(radius_start=radius_min, radius_max=radius_max, dist_max=dis_max, area=self.mv_AreaPolygon.area, h_value=1)

        # List of all particles
        particles = []

        # Creating the particles with inital positions taken from node's positions
        for node in self.ml_Nodes:
            
            # Clearing important flags
            node.deactivate()
            node.clear_path()

            # Appending the particles list
            particles.append(Particle(position=node.get_localization(), velocity=0))

        # Initialising the radius, pfitness and pbest values inside the particles
        for particle in particles:
            # Calculating the distance from the particle to the base node
            dis = shapely.distance(particle.get_position(), self.mv_BaseStation.get_localization())

            # Calculating and setting the particle radius
            particle.set_radius((dis/dis_max * (radius_max - radius_min) + radius_min))

            particle.set_pfitness(self.fitness(particle))

            # Using a shortcut, setting the pbest as particle, and not a point, for easier calculations
            particle.set_pbest(particle)

        # Searching for an appropriate gbest init value
        gbest = None
        value = 0
        for particle in particles:
            temp = self.Fitness(particle, particles)
            if temp > value:
                value = temp
                gbest = particle

        # Setting the gbest across particles
        for particle in particles:
            particle.set_gbest(gbest)

        # List containing all of the added gbest values. Enables the searching of appropriate ch nodes later
        gbest_values = []

        # Repeating the pso algorithm for a set amount of iterations
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
                value = (dis/dis_max * (radius_max - radius_min) + radius_min)

                if value < radius_max:
                    particles[j].set_radius(value)
                else:
                    particles[j].set_radius(radius_max)
                
                # Calculating fitness values
                fitness_particle = self.fitness(particles[j])
                fitness_population = self.Fitness(particles[j], particles)

                # If the particle doesn't have any neighbours it is automatically added to the best particles list
                if fitness_particle < self.fitness(particles[j].get_pbest()):
                    particles[j].set_pbest(particles[j])
                if fitness_population < self.Fitness(gbest, particles):
                    gbest = particles[j]
                    gbest_values.append(gbest)

                    for particle in particles:
                        particle.set_gbest(gbest)

            # List for storing the candidates for ch areas after discarding some weak options
            ch_area_candidates = []

            # Discarding values that don't meet the criteria
            for particle in gbest_values:
            
                # If the ratio of intersected nodes to all nodes is to0 high, discards the candidate
                if self.IoU(particle, particles) < 0.70:
                    ch_area_candidates.append(particle)

            # Searching for the CH nodes in the CH candidate areas
            for particle in ch_area_candidates:

                # Calculating the polygon of the candidate area
                area = particle.get_position().buffer(particle.get_radius())

                # List of from which there will be a CH choosen
                nodes = []

                # Checking for nodes that are inside of the candidate area
                for node in self.ml_Nodes:
                
                    # If the node is withing the area, it is added to the list
                    if shapely.contains(area, node.get_localization()) and not node.is_battery_low() and not node.is_active():
                        nodes.append(node)

                # Tuple that will help find the final CH node from the candidates found above
                ch = (None, 100000)

                # Comparing the weights of every individual nodes in the candidate's list
                for node in nodes:
                    if not node.is_battery_low() and not node.is_active():
                
                        # Calculating and storing the weight value
                        temp = self.Weight(node)

                        # Checking if it is bigger than the other
                        if temp < ch[1]:
                    
                            # If yes, the tuple takes this candidate's values
                            ch = (node, temp)
            
                # Adding found nodes to the set
                if ch[0] != None:
                    self.ml_ClusterHeads.add(ch[0])

            if len(self.ml_ClusterHeads) >= math.ceil(C):
                break

            total_iterations+=1

        ###############################
        # Assigning nodes to clusters #
        ###############################

        # Adding the cluster heads to the clusters lists
        for ch in self.ml_ClusterHeads:
            
            if not ch.is_battery_low() and not ch.is_active():
                # Activating the boolean inside every CH for easy recognition
                ch.activate()
                self.mv_ActiveNodes+=1
                ch.activate_cluster_head_flag()

                self.ml_Clusters.append([ch])

        # Checking which nodes are closer than d0 to the base station
        for node in self.ml_Nodes:
            if not node.is_battery_low() and not node.is_active():
            
                if shapely.distance(node.get_localization(), self.mv_BaseStation.get_localization()) < self.mv_BaseStation.get_amplifier_threshold_distance():
                    self.ml_NodeToBaseNode.append(node)
                    self.mv_ActiveNodes+=1
                    node.activate()

        # Adding nodes to the clusters
        for node in self.ml_Nodes:
            if not node.is_battery_low() and not node.is_active():
                # Tuple made out of energy value and cluster index
                temp = (100000, None)
            
                for j in range(len(self.ml_Clusters)):

                    # Calculating the distance between the node and the cluster head
                    if id(node) != id(self.ml_Clusters[j][0]):
                        distance = shapely.distance(node.get_localization(), self.ml_Clusters[j][0].get_localization())

                        power_draw = self.mv_BaseStation.calculate_transmission_consumption(distance=distance, packet_size=self.mv_BaseStation.get_data_packet_size())

                        if temp[0] - power_draw > 0:
                            updated = (power_draw, j)
                            temp = updated

                if temp[1] != None:
                    node.activate()
                    self.mv_ActiveNodes+=1
                    self.ml_Clusters[temp[1]].append(node)


    # The setup + steady phase of pso
    def pso_algorithm(self):

        if not self.mb_Ready:
            self.initiate_network()

        self.pso_setup()

        ################
        # Steady state #
        ################

        self.mv_LND = 0
        head_died = False
        print("Begining the pso simulation!")

        while self.calculate_coverage() > self.mv_MinimumCoverage:

            if len(self.ml_ClusterHeads) == 0:
                break
            
            reshuffle = False
            
            # If there is any need - creating the multihop route for the cluster heads over other cluster heads
            for head in self.ml_ClusterHeads:

                if not head.is_battery_low():
                
                    head.clear_path()

                    # Checking if a node needs multihop
                    if shapely.distance(head.get_localization(), self.mv_BaseStation.get_localization()) > self.mv_BaseStation.get_amplifier_threshold_distance():
                        hops_left = []

                        for ch in self.ml_ClusterHeads:
                            hops_left.append(ch)
                    
                        hops_left.append(self.mv_BaseStation)
                        hops_left.remove(head)

                        while not head.is_path_estabilished():
                            next_hop_tuple = (None, None)
                            for hop in hops_left:
                                value = self.hop_weight(head, hop)

                                # If the temporal tuple is empty
                                if next_hop_tuple[1] == None:
                                    temp = (hop, value)
                                    next_hop_tuple = temp

                                if value < next_hop_tuple[1]:
                                    temp = (hop, value)
                                    next_hop_tuple = temp
                        
                            head.add_to_path(next_hop_tuple[0])
                            if id(next_hop_tuple[0]) == id(self.mv_BaseStation):
                                break
                            hops_left.remove(next_hop_tuple[0])

                        # Adding to the paths estabilished index
                        head.activate_multihop_flag()
                    else:
                        head.add_to_path(self.mv_BaseStation)
                else:
                    reshuffle = True

            if(reshuffle):
                self.pso_setup()
                reshuffle = False
                continue

            #############################
            # Proceeding with the round #
            #############################

            # The direct communicating nodes go first
            for node in self.ml_NodeToBaseNode:
                node.transmit_data(shapely.distance(node.get_localization(), self.mv_BaseStation.get_localization()))

            # First, the clusters collect the data
            for i in range(len(self.ml_Clusters)):

                if self.ml_Clusters[i][0].is_active():
                    for j in range(len(self.ml_Clusters[i])):

                        if id(self.ml_Clusters[i][0]) != id(self.ml_Clusters[i][j]):
                            self.ml_Clusters[i][j].transmit_data(shapely.distance(self.ml_Clusters[i][0].get_localization(), self.ml_Clusters[i][j].get_localization()))
                else:
                    for k in range(len(self.ml_Clusters[i])):
                        if self.ml_Clusters[i][k].is_active():
                            self.ml_Clusters[i][k].deactivate()
                            self.mv_ActiveNodes-=1

                            # Checking for the algorithm statistics
                            if self.mb_FirstNodeDied and self.mv_ActiveNodes == (self.mv_NodeAmount-1):
                                self.mv_FND = self.mv_LND
                                self.mb_FirstNodeDied = True
                    
                            if (self.mb_HalfNodesDies and
                            (self.mv_ActiveNodes == self.mv_NodeAmount - int((self.mv_MinimumCoverage/100)*self.mv_NodeAmount))):
                                self.mv_HND = self.mv_LND
                                self.mb_HalfNodesDies = True

            # Then the clusters send the data to the base node via their calculated path
            for ch in self.ml_Clusters:

                path = ch[0].get_path()

                # Pretending that the
                if len(path) > 1:
                    # Pretending that I am sending data_packets from the ch to the first hop
                    ch[0].aggregate_and_send_data(distance=shapely.distance(ch[0].get_localization(), path[0].get_localization()), amount_of_data_packets=len(ch))

                    # Then the data is sent through other hops
                    for i in range(len(path)-1):
                        path[i].aggregate_and_send_data(distance=shapely.distance(ch[0].get_localization(), path[i+1].get_localization()), amount_of_data_packets=len(ch))
                elif len(path) == 1:
                    # Pretending that I am sending data_packets from the ch to the first hop
                    ch[0].aggregate_and_send_data(distance=shapely.distance(ch[0].get_localization(), path[0].get_localization()), amount_of_data_packets=len(ch))
                
            for node in self.ml_Nodes:
                    
                if node.get_battery_level() < 1 and not node.is_battery_low():
                    node.activate_battery_low_flag()
                    self.mv_ActiveNodes-=1

                    # Checking for the algorithm statistics
                    if self.mb_FirstNodeDied and self.mv_ActiveNodes == (self.mv_NodeAmount-1):
                        self.mv_FND = self.mv_LND
                        self.mb_FirstNodeDied = True
                    
                    if (self.mb_HalfNodesDies and
                    (self.mv_ActiveNodes == self.mv_NodeAmount - int((self.mv_MinimumCoverage/100)*self.mv_NodeAmount))):
                        self.mv_HND = self.mv_LND
                        self.mb_HalfNodesDies = True

            print(self.mv_ActiveNodes)
            self.mv_LND += 1

        ########################################

        self.mb_LastNodeDied = True
        print(self.mv_LND)
    

    ####################
    # Plotting methods #
    ####################


    def calculate_plot_data(self):

        if self.mb_Ready:

            # Clearing the old data
            self.ml_xAxisPlotData.clear()
            self.ml_yAxisPlotData.clear()
            self.ml_ColorPlotData.clear()

            # Appending the coordinates and the colours of the nodes to the lists
            for node in self.ml_Nodes:
                self.ml_xAxisPlotData.append(node.get_localization().coords[:][0][0])
                self.ml_yAxisPlotData.append(node.get_localization().coords[:][0][1])
                self.ml_ColorPlotData.append(node.mv_Color)

            # Adding the base station to the list
            self.ml_xAxisPlotData.append(self.mv_BaseStation.get_localization().coords[:][0][0])
            self.ml_yAxisPlotData.append(self.mv_BaseStation.get_localization().coords[:][0][1])
            self.ml_ColorPlotData.append(self.mv_BaseStation.mv_Color)


    def cleanup_after_simulation(self):

        # Cleaning the statistcs
        self.mb_LastNodeDied = False
        self.mb_HalfNodesDies = False
        self.mb_FirstNodeDied = False

        # Clearing every node that has been used out of data
        for node in self.ml_Nodes:
            node.clear()
            node.set_battery_capacity(self.mv_BatteryCapacity)
            node.deactivate()

        # Setting active nodes count to 0
        self.mv_ActiveNodes = 0

        # Clearing all of the lists and variables of data
        self.ml_ClusterHeads.clear()
        self.ml_Clusters.clear()
        self.ml_SinkNodes.clear()
        self.ml_Nodes.clear()

        if self.mv_BaseStation != None:
            self.mv_BaseStation.clear()

        # Setting base station to none
        self.mv_BaseStation = None

        self.mb_Ready = False