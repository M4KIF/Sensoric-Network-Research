
#######################################
# Takes the sensoric network and data #
# collecting objects to create a      #
# simulation                          #
#######################################



############
# Includes #
############

# From there on, a simulation will be created in conjunction with data logging
from .. import sensoric_network
from .. import misc

# For enabling the multithreading in the main App by using signals
from PyQt5 import QtCore

#
# Object definition #
#

class NetworkSimulator():

    def __init__(self):
        print()