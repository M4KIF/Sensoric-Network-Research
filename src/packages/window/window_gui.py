
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


    def createAreaPlot(self, x, y, color):
        self.m_Plots.scatter(x, y, s=50, c=color, cmap="spring")


    def clearCanvas(self):
        # Checking if there are more than one plots on the canvas
        for plot in self.m_Figure.get_axes():
            plot.clear()

        # Clearing the figure of any plots
        self.m_Figure.clear()


    def clearAxes(self):
        for plot in self.m_Figure.get_axes():
            plot.clear()


    def updateAxes(self):
        self.draw()

# GUI class, implements the functionality from the backend 
class Window(QMainWindow):

    def __init__(self, *args, **kwargs):

        ###########################################
        # Objects initialisation, threading, etc. #
        ###########################################

        # Base class initialisation
        super(Window, self).__init__(*args, **kwargs)

        # App name
        self.m_AppName = "WSN-Research"

        # The backend, that the window will visualise
        self.backend = simulator.wsnSimulator()

        ######################################
        # Main Window layouts initialisation #
        ######################################

        # The outer window layout to which I will add the area plot and the settings panel
        self.mainLayout = QHBoxLayout()

        # The plot layout, to which I will add an matplotlib widget
        self.plotLayout = QGridLayout()
        self.area_widget = PlotCanvas(self, width=8,height=7,dpi=120)
        self.area_widget.addSinglePlot()
        self.draw_plot()
        self.plotLayout.addWidget(self.area_widget)

        # The settings panel layout
        self.settingsLayout = QVBoxLayout()
        self.settingsLayout.setSpacing(15)
        self.settingsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        ############################################
        # Algorithm settings panel layout creation #
        ############################################

        # Creating a algorithm selection section
        self.algorithm_layout = QFormLayout()

        # Defining the algorithm selection combobox and linking it to the function, which takes the index
        self.select_algorithm_combo = QComboBox()
        self.select_algorithm_combo.addItems(self.backend.m_Network.ml_Algorithms)
        self.select_algorithm_combo.setStatusTip("Sends the backend a message about which algorithm to use")
        self.select_algorithm_combo.activated.connect(self.set_algorithm)

        # Adding a row with and action
        self.algorithm_layout.addRow("Algorithm:", self.select_algorithm_combo)

        #######################################
        # Area settings panel layout creation #
        #######################################

        # Creating the area dimensions section
        self.area_dimensions_layout = QFormLayout()

        # Defining the height selection line edit
        self.select_height_box = QLineEdit()
        self.select_height_box.setStatusTip("Enables the edition of the area height parameter")
        self.select_height_box.setText(str(self.backend.m_Network.mv_Height))
        self.select_height_box.textEdited.connect(self.set_height)

        # Defining the width selection line edit
        self.select_width_box = QLineEdit()
        self.select_width_box.setStatusTip("Enables the edition of the area width parameter")
        self.select_width_box.setText(str(self.backend.m_Network.mv_Width))
        self.select_width_box.textEdited.connect(self.set_width)

        # Defining the area coverage line edit
        self.select_minimal_area_coverage_box = QLineEdit()
        self.select_minimal_area_coverage_box.setStatusTip("Enables the edition of the minimal area coverage parameter")
        self.select_minimal_area_coverage_box.setText(str(self.backend.m_Network.mv_MinimumCoverage))
        self.select_minimal_area_coverage_box.textEdited.connect(self.set_minimal_coverage)

        # Adding the boxes to the layout
        self.area_dimensions_layout.addRow("Area height:", self.select_height_box)
        self.area_dimensions_layout.addRow("Area width:", self.select_width_box)
        self.area_dimensions_layout.addRow("Minimal coverage:", self.select_minimal_area_coverage_box)

        #######################################
        # Node settings panel layout creation #
        #######################################

        # Node settings layout
        self.node_settings_layout = QFormLayout()

        # Defining the nodes amount line edit
        self.nodes_amount_box = QLineEdit()
        self.nodes_amount_box.setStatusTip("Enables the edition of the nodes amount in the networks")
        self.nodes_amount_box.setText(str(self.backend.m_Network.mv_NodeAmount))
        self.nodes_amount_box.textEdited.connect(self.set_nodes_amount)

        # Defining the node's battery capacity line edit
        self.nodes_battery_capacity_box = QLineEdit()
        self.nodes_battery_capacity_box.setStatusTip("Enables the edition of the nodes battery capacity")
        self.nodes_battery_capacity_box.setText(str(self.backend.m_Network.mv_BatteryCapacity))
        self.nodes_battery_capacity_box.textEdited.connect(self.set_nodes_battery_capacity)

        # Adding the node settings boxes to the layout
        self.node_settings_layout.addRow("Nodes Amount:", self.nodes_amount_box)
        self.node_settings_layout.addRow("Battery capacity:", self.nodes_battery_capacity_box)

        ######################################
        # Runtime info panel layout creation #
        ######################################

        # Runtime information
        self.runtime_info_layout = QFormLayout()

        # Will display the current coverage
        self.current_coverage_label = QLabel()
        self.current_coverage_label.setText(self.backend.m_Network.mv_CurrentCoverage)

        # Displays the naive alg. times label
        self.naive_label = QLabel()
        self.naive_label.setText("Naive algorithm times:")

        # Displays the naive average run times
        self.naive_average = QLabel()
        self.naive_average.setText("0.0")

        # Displays the naive last run time
        self.naive_last = QLabel()
        self.naive_last.setText("0.0")

        # Displays the optimised alg. times label
        self.optimised_label = QLabel()
        self.optimised_label.setText("Optimised algorithm times:")

        # Displays the optimised average run times
        self.optimised_average = QLabel()
        self.optimised_average.setText("0.0")

        # Displays the optimised last run time
        self.optimised_last = QLabel()
        self.optimised_last.setText("0.0")

        # Adding the labels to the layout
        self.runtime_info_layout.addWidget(self.naive_label)
        self.runtime_info_layout.addRow("Mean", self.naive_average)
        self.runtime_info_layout.addRow("Last", self.naive_last)
        self.runtime_info_layout.addWidget(self.optimised_label)
        self.runtime_info_layout.addRow("Mean", self.optimised_average)
        self.runtime_info_layout.addRow("Last", self.optimised_last)
        self.runtime_info_layout.addRow("Current coverage:", self.current_coverage_label)

        #######################################################
        # Adding created layouts to the outer settings layout #
        #######################################################

        # Adding the final "run" button to the layout
        self.run_simulation_button = QPushButton()
        self.run_simulation_button.clicked.connect(self.run_simulation)
        self.run_simulation_button.setText("Simulate!")
        
        self.settingsLayout.addLayout(self.algorithm_layout)
        self.settingsLayout.addLayout(self.area_dimensions_layout)
        self.settingsLayout.addLayout(self.node_settings_layout)
        self.settingsLayout.addLayout(self.runtime_info_layout)
        self.settingsLayout.addWidget(self.run_simulation_button)

        ##############################################
        # Adding sublayouts to the main/outer layout #
        ##############################################

        self.mainLayout.addLayout(self.plotLayout)
        self.mainLayout.addLayout(self.settingsLayout)

        ###########################################################
        # Setting the created layout as the main displayed widget #
        ###########################################################
        
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.mainLayout)

        # Setting as central
        self.setCentralWidget(self.main_widget)

        # Showing the layout on the screen
        self.show()





    def set_algorithm(self, index=int):
        self.backend.m_Network.set_algorithm(index)


    def set_height(self, height=str):

        if height != '':
            if int(height) > 0 and int(height) < 20000:

                self.backend.m_Network.set_height(int(height))

                self.select_height_box.setText(str(self.backend.m_Network.mv_Height))

                self.draw_plot()


    def set_width(self, width=str):

        if width!='':
            if int(width) > 0 and int(width) < 20000:

                self.backend.m_Network.set_width(int(width))

                self.select_width_box.setText(str(self.backend.m_Network.mv_Width))

                self.draw_plot()


    def set_minimal_coverage(self, coverage=str):

        if(int(coverage) > 0 and int(coverage) <= 100):
            self.backend.m_Network.set_minimum_coverage_value(int(coverage))

            self.select_minimal_area_coverage_box.setText(str(self.backend.m_Network.mv_MinimumCoverage))

        else:
            print("Here I must show and error with OK button")


    def set_nodes_amount(self, amount=str):

        if amount != '':
            if int(amount) > 0 and int(amount) < 2000:
        
                self.backend.m_Network.set_node_amount(int(amount))

                self.nodes_amount_box.setText(str(self.backend.m_Network.mv_NodeAmount))

                self.draw_plot()


    def set_nodes_battery_capacity(self, capacity=str):
        
        if capacity != '':
            if int(capacity) > 0 and int(capacity) < 5000:
                self.backend.m_Network.set_node_battery_capacity(int(capacity))

                self.nodes_battery_capacity_box.setText(str(self.backend.m_Network.mv_BatteryCapacity))


    def draw_plot(self):
        self.area_widget.clearAxes()

        temp = self.backend.m_Network.get_plot_data()

        self.area_widget.createAreaPlot(temp[0], temp[1], temp[2])

        self.area_widget.updateAxes()


    def run_simulation(self):
        self.draw_plot()
        self.backend.run_simulation()
        self.draw_plot()
        self.naive_last.setText(str(self.backend.mo_DataCollector.mv_NaiveLastTime))
        try:
            self.naive_average.setText(str(self.backend.mo_DataCollector.calculate_mean_from_naive_times()))
        except Exception as e:
            print(e[0])
        


