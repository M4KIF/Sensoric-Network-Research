
#######################################
# Takes the sensoric network and data #
# collecting objects to create a      #
# simulation                          #
#######################################



############
# Includes #
############

# From there on, a simulation will be created in conjunction with data logging
from .. import wsn as network
from .. import misc as data
import time

# For enabling the multithreading in the main App by using signals
from PyQt5 import QtCore

#
# Object definition #
#

class wsnSimulator():

    def __init__(self):
        self.m_Network = network.SensoricNetwork(x_l=0, y_l=0, x_u=1000, y_u=1000)

        self.m_Network.initiate_network(100, 650)

        time_before = time.time()
        self.m_Network.naive_algorithm()
        time_after = time.time()

        print(f"The runtime is {time_after - time_before}s")