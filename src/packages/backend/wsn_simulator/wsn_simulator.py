


#########################################
# Takes the sensoric network and data   #
# collecting objects to create a        #
# simulation environment.               #
# Also works as some sort of an         #
# interface class for the above objects #
# to help implement multithreading      #
#########################################



############
# Includes #
############


# The WSN object
from .. import wsn as network

# The Data Collection object
from .. import misc as data

# For enabling the multithreading in the main App by using signals
from PyQt5.QtCore import pyqtSignal, QObject, QMutex


#####################
# Object definition #
#####################


class wsnSimulator(QObject):

    def __init__(self):
        super().__init__()

        self.m_Network = network.SensoricNetwork(node_amount=50, battery_capacity=1, width=100, height=100,)

        self.m_Network.initiate_network()

        self.mo_DataCollector = data.DataCollector()


    def initialise_network(self):
        self.m_Network.initiate_network()

    
    # Running the simulation, distinguishing which to run via index of the algorithms list
    def run_simulation(self):
        if self.m_Network.mv_CurrentAlgorithm == self.m_Network.ml_Algorithms[0]:
            self.mo_DataCollector.start_timer()
            self.m_Network.naive_algorithm_new()
            self.mo_DataCollector.end_timer()
            self.mo_DataCollector.save_result_as_naive()
        else:
            self.mo_DataCollector.start_timer()
            self.m_Network.pso_algorithm()
            self.mo_DataCollector.end_timer()
            self.mo_DataCollector.save_result_as_optimised()
        
        return True