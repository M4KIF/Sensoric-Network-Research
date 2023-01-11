
###################################
# Window GUI and application loop #
###################################



############
# Includes #
############

# Elements for running the simulation
from ..backend import wsn_simulator as simulator
#from backend import misc
#from backend import network_simulator

# Qt backend
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# Matplotlib
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

# Arrays
import numpy as np

# Default modules
import sys
import os
from copy import copy

class PlotCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=8, height=2, dpi=100):

        #################
        # Boolean flags #
        #################

        self.m_MultiplePlots = False
        self.m_StackedHorizontaly = False
        self.m_StackedVerticaly = False


        ###########################################
        # Variables containing the Canvas content #
        ###########################################

        self.m_GridSpace = None
        self.m_Plots = None
        self.m_Figure = Figure(figsize=(width, height), dpi=dpi)

        #########
        # Setup #
        #########

        # Calling the constructor of the base class
        super(PlotCanvas, self).__init__(self.m_Figure)

        # Changing the layout to tight
        self.m_Figure.tight_layout()


    def addSinglePlot(self):
        self.m_Plots = self.m_Figure.subplots()


    def addTwoHorizontalPlots(self):
        self.m_GridSpace = self.m_Figure.add_gridspec(2, hspace=0.2)
        self.m_Plots = self.m_GridSpace.subplots()
        self.m_Plots[0].set_xticklabels([])
        self.m_Plots[0].set_xticks([])
        self.m_MultiplePlots = True
        self.m_StackedVerticaly = True


    def addTwoVerticalPlots(self):
        self.m_GridSpace = self.m_Figure.add_gridspec(1, 2, wspace=0.1)
        self.m_Plots = self.m_GridSpace.subplots(sharex=True)
        self.m_Plots[1].set_yticklabels([])
        self.m_Plots[1].set_yticks([])
        self.m_Plots[0].set_xticks([])
        self.m_MultiplePlots = True
        self.m_StackedHorizontaly = True


    def createFrequencyResponsePlot(self, data):
        self.m_Plots.plot(data[1], data[0])


    def createSpectrogramPlot(self, data):
        if not (self.m_MultiplePlots == True and self.m_StackedVerticaly == True):
            self.m_Plots.pcolormesh(self.backend.getFirstChannelTimeSegments(), self.backend.getFirstChannelFrequencySamples(), self.backend.getFirstChannelSpectrogramData(), cmap="plasma")
        else:
            self.m_Plots[0].pcolormesh(data[0][1], data[0][0], data[0][2], cmap="plasma")
            self.m_Plots[1].pcolormesh(data[1][1], data[1][0], data[1][2], cmap="plasma")


    def createSpectralDistributionPlot(self, data):
        print('')


    def clearCanvas(self):
        # Checking if there are more than one plots on the canvas
        for plot in self.m_Figure.get_axes():
            plot.clear()

        # Clearing the figure of any plots
        self.m_Figure.clear()

        # Changing the multiplots flag
        self.m_MultiplePlots = False
        self.m_StackedHorizontaly = False
        self.m_StackedVerticaly = False


    def clearAxes(self):
        for plot in self.m_Figure.get_axes():
            plot.clear()


    def updateAxes(self):
        self.draw()

# GUI class, implements the functionality from the backend 
class Window(QMainWindow):

    def __init__(self, *args, **kwargs):

        # Base class initialisation
        super(Window, self).__init__(*args, **kwargs)

        # App name
        self.m_AppName = "WSN-Research"

        self.backend = simulator.wsnSimulator()

        #
        self.baseLayout = QHBoxLayout()

        self.settingsLayout = QGridLayout()

        self.areaLayout = QGridLayout()

        self.algorithms_label = QLabel()
        self.algorithms_label.setText("Algorithms Available")
        self.settingsLayout.addWidget(self.algorithms_label, 0, 0, 1, 1)

        self.algorithms_combo = QComboBox()
        self.algorithms_combo.addItems(self.backend.m_Network.ml_Algorithms)
        self.settingsLayout.addWidget(self.algorithms_combo, 1, 0, 2, 1, Qt.AlignmentFlag.AlignTop)

        self.height_label = QLabel()
        self.height_label.setText("Height:")
        self.settingsLayout.addWidget(self.height_label, 2, 0, 3, 1, Qt.AlignmentFlag.AlignTop)

        self.height_edit = QLineEdit()
        self.height_edit.setText(str(self.backend.m_Network.ml_AreaPoints[2].coords[0][1]))
        self.settingsLayout.addWidget(self.height_edit, 3, 0, 4, 1, Qt.AlignmentFlag.AlignTop)

        self.width_label = QLabel()
        self.width_label.setText("Height:")
        self.settingsLayout.addWidget(self.width_label, 4, 0, 5, 1, Qt.AlignmentFlag.AlignTop)

        self.width_edit = QLineEdit()
        self.width_edit.setText(str(self.backend.m_Network.ml_AreaPoints[2].coords[0][0]))
        self.settingsLayout.addWidget(self.width_edit, 5, 0, 6, 1, Qt.AlignmentFlag.AlignTop)
        
        self.nodes_amount_label = QLabel()
        self.nodes_amount_label.setText("The amount of nodes used")
        self.settingsLayout.addWidget(self.nodes_amount_label, 6, 0, 7, 1, Qt.AlignmentFlag.AlignTop)

        self.nodes_amount_edit = QLineEdit()
        self.settingsLayout.addWidget(self.nodes_amount_edit, 7, 0, 8, 1, Qt.AlignmentFlag.AlignTop)

        self.battery_capacity_label = QLabel()
        self.battery_capacity_label.setText("The battery capacity")
        self.settingsLayout.addWidget(self.battery_capacity_label, 8, 0, 9, 1, Qt.AlignmentFlag.AlignTop)

        self.battery_capacity = QLineEdit()
        self.settingsLayout.addWidget(self.battery_capacity, 9, 0, 10, 1, Qt.AlignmentFlag.AlignTop)

        self.run_simulation_button = QPushButton()
        self.run_simulation_button.clicked.connect(self.backend.m_Network.run_simulation)
        self.run_simulation_button.setText("Simulate!")
        self.settingsLayout.addWidget(self.run_simulation_button, 10, 0, 11, 1, Qt.AlignmentFlag.AlignCenter)

        battery_capacity_change_action = QAction()

        self.area_widget = PlotCanvas(self, width=10,height=7,dpi=120)

        self.areaLayout.addWidget(self.area_widget)

        self.baseLayout.addLayout(self.areaLayout)
        self.baseLayout.addLayout(self.settingsLayout)

        self.main_widget = QWidget()

        self.main_widget.setLayout(self.baseLayout)
        self.setCentralWidget(self.main_widget)

        self.show()

