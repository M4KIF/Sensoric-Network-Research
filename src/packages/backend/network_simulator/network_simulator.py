
#######################################
# Takes the sensoric network and data #
# collecting objects to create a      #
# simulation                          #
#######################################



############
# Includes #
############

# From there on, a simulation will be created in conjunction with data logging
from .. import sensoric_network as network
from .. import misc as data

# For enabling the multithreading in the main App by using signals
from PyQt5 import QtCore

#
# Object definition #
#

class NetworkSimulator():

    m_Network = network.SensoricNetwork(x_l=0, y_l=0, x_u=500, y_u=500)

    def __init__(self):
        self.m_Network.initiate_network(25, 500)
        self.m_Network.naive_algorithm()