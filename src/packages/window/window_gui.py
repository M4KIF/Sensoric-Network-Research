
###################################
# Window GUI and application loop #
###################################



############
# Includes #
############

# Elements for running the simulation
from ..backend import network_simulator as simulator
#from backend import misc
#from backend import network_simulator

# Qt backend
from PyQt5 import QtCore, QtWidgets, QtGui

# Arrays
import numpy as np

# Default modules
import sys
import os
from copy import copy

m_Hey = simulator.NetworkSimulator()

print(id(m_Hey))
print("Its here")

