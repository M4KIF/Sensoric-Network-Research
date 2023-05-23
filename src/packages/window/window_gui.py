###################################
# Window GUI and application loop #
###################################


############
# Includes #
############


# Elements for running the simulation
from ..backend import wsn as network

#
from ..backend.misc import DataCollector

#
# Default imports
#

import time

from copy import copy

# Qt backend
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# Matplotlib
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure

# Arrays
import numpy as np


class Canvas(FigureCanvasQTAgg):
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
        super(Canvas, self).__init__(self.m_Figure)

        # Changing the layout to tight
        self.m_Figure.tight_layout()

    def addSinglePlot(self):
        self.m_Plots = self.m_Figure.subplots()

    def createAreaPlot(self, x, y, color):
        self.m_Plots.scatter(x, y, s=50, c=color, cmap="Set1")

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
    # Thread object for multithreading the backend
    m_BackendThread = QThread()

    def __init__(self, *args, **kwargs):
        ###########################################
        # Objects initialisation, threading, etc. #
        ###########################################

        # Base class initialisation
        super(Window, self).__init__(*args, **kwargs)

        # App name
        self.m_AppName = "WSN-Research"

        # Setting the window title to the above
        self.setWindowTitle(self.m_AppName)

        # Plot data
        self.m_PlotData = []

        # Repetition amount possible and current repeat value
        self.m_RepetitionValues = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        self.m_Repeat = int(self.m_RepetitionValues[0])

        # Round results
        self.m_NaiveRoundData = [0, 0, 0]
        self.m_psoRoundData = [0, 0, 0]

        # Coverage stats
        self.m_NaiveCoverageData = []
        self.m_PsoCoverageData = []

        # Current active nodes
        self.m_ActiveNodes = 0

        self.m_SimulationRoundFinished = False

        self.m_CurrentAlgorithm = str()

        self.m_NodeAmount = 0

        self.m_Height = 0

        self.m_Width = 0

        self.m_ToPlot = False

        self.m_ToCompareCoverage = False

        self.m_ToCompareRuntimeStats = False

        # Data collector and plotter object
        self.m_DataCollector = DataCollector()

        # The backend, that the window will visualise
        self.backend = network.SensoricNetwork(
            node_amount=50, battery_capacity=1, width=200, height=200
        )

        self.backend.moveToThread(self.m_BackendThread)

        ######################################
        # Main Window layouts initialisation #
        ######################################

        # The outer window layout to which I will add the area plot and the settings panel
        self.mainLayout = QHBoxLayout()

        # The plot layout, to which I will add an matplotlib widget
        self.plotLayout = QGridLayout()
        self.area_widget = Canvas(self, width=8, height=7, dpi=120)
        self.area_widget.addSinglePlot()
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
        self.backend.signal_get_algorithms_list.emit()
        self.select_algorithm_combo.setStatusTip(
            "Sends the backend a message about which algorithm to use"
        )
        self.select_algorithm_combo.activated.connect(self.set_algorithm)

        # Adding a row with and action
        self.algorithm_layout.addRow("Algorytm:", self.select_algorithm_combo)

        #######################################
        # Area settings panel layout creation #
        #######################################

        # Creating the area dimensions section
        self.area_dimensions_layout = QFormLayout()

        # Defining the height selection line edit
        self.select_height_box = QLineEdit()
        self.select_height_box.setStatusTip(
            "Enables the edition of the area height parameter"
        )
        self.select_height_box.textEdited.connect(self.set_height)

        # Defining the width selection line edit
        self.select_width_box = QLineEdit()
        self.select_width_box.setStatusTip(
            "Enables the edition of the area width parameter"
        )
        self.select_width_box.textEdited.connect(self.set_width)

        # Defining the area coverage line edit
        self.select_minimal_area_coverage_box = QLineEdit()
        self.select_minimal_area_coverage_box.setStatusTip(
            "Enables the edition of the minimal area coverage parameter"
        )
        self.select_minimal_area_coverage_box.textEdited.connect(
            self.set_minimal_coverage
        )

        # Adding the boxes to the layout
        self.area_dimensions_layout.addRow("Wysokość:", self.select_height_box)
        self.area_dimensions_layout.addRow("Szerokość:", self.select_width_box)
        self.area_dimensions_layout.addRow(
            "Minimalne pokrycie:", self.select_minimal_area_coverage_box
        )

        #######################################
        # Node settings panel layout creation #
        #######################################

        # Node settings layout
        self.node_settings_layout = QFormLayout()

        # Defining the nodes amount line edit
        self.nodes_amount_box = QLineEdit()
        self.nodes_amount_box.setStatusTip(
            "Enables the edition of the nodes amount in the networks"
        )
        self.nodes_amount_box.textEdited.connect(self.set_nodes_amount)

        # Defining the node's battery capacity line edit
        self.nodes_battery_capacity_box = QLineEdit()
        self.nodes_battery_capacity_box.setStatusTip(
            "Enables the edition of the nodes battery capacity"
        )
        self.nodes_battery_capacity_box.textEdited.connect(
            self.set_nodes_battery_capacity
        )

        # Adding the node settings boxes to the layout
        self.node_settings_layout.addRow("Ilość sensorów:", self.nodes_amount_box)
        self.node_settings_layout.addRow(
            "Pojemność baterii:", self.nodes_battery_capacity_box
        )

        # Repetition amount layout
        self.repetition_amount_layout = QFormLayout()
        self.repetition_amount_combo = QComboBox()
        self.repetition_amount_combo.addItems(self.m_RepetitionValues)
        self.repetition_amount_combo.activated.connect(self.set_repetition)
        self.repetition_amount_layout.addRow(
            "Ilość powtórzeń:", self.repetition_amount_combo
        )

        self.to_plot_combo = QCheckBox()
        self.to_plot_combo.toggled.connect(self.to_plot)
        self.repetition_amount_layout.addRow("Zapisz wykresy:", self.to_plot_combo)

        self.to_compare_coverage_checkbox = QCheckBox()
        self.to_compare_coverage_checkbox.toggled.connect(self.to_compare_coverage)
        self.repetition_amount_layout.addRow(
            "Porównaj wykresy pokrycia:", self.to_compare_coverage_checkbox
        )

        self.to_compare_runtime_stats_checkbox = QCheckBox()
        self.to_compare_runtime_stats_checkbox.toggled.connect(
            self.to_compare_runtime_stats
        )
        self.repetition_amount_layout.addRow(
            "Porównaj wykresy przebiegu:", self.to_compare_runtime_stats_checkbox
        )

        # Safety connects
        self.to_compare_coverage_checkbox.toggled.connect(
            self.select_algorithm_combo.setDisabled
        )
        self.to_compare_coverage_checkbox.toggled.connect(
            self.select_height_box.setDisabled
        )
        self.to_compare_coverage_checkbox.toggled.connect(
            self.select_width_box.setDisabled
        )
        self.to_compare_coverage_checkbox.toggled.connect(
            self.select_minimal_area_coverage_box.setDisabled
        )
        self.to_compare_coverage_checkbox.toggled.connect(
            self.nodes_amount_box.setDisabled
        )
        self.to_compare_coverage_checkbox.toggled.connect(
            self.nodes_battery_capacity_box.setDisabled
        )
        self.to_compare_coverage_checkbox.toggled.connect(
            self.repetition_amount_combo.setDisabled
        )
        self.to_compare_coverage_checkbox.toggled.connect(self.to_plot_combo.setChecked)

        self.to_compare_runtime_stats_checkbox.toggled.connect(
            self.select_algorithm_combo.setDisabled
        )
        self.to_compare_runtime_stats_checkbox.toggled.connect(
            self.select_height_box.setDisabled
        )
        self.to_compare_runtime_stats_checkbox.toggled.connect(
            self.select_width_box.setDisabled
        )
        self.to_compare_runtime_stats_checkbox.toggled.connect(
            self.select_minimal_area_coverage_box.setDisabled
        )
        self.to_compare_runtime_stats_checkbox.toggled.connect(
            self.nodes_amount_box.setDisabled
        )
        self.to_compare_runtime_stats_checkbox.toggled.connect(
            self.nodes_battery_capacity_box.setDisabled
        )
        self.to_compare_runtime_stats_checkbox.toggled.connect(
            self.repetition_amount_combo.setDisabled
        )
        self.to_compare_runtime_stats_checkbox.toggled.connect(
            self.to_plot_combo.setChecked
        )

        # self.select_algorithm_combo.setDisabled(self.to_compare_coverage_coverage_checkbox.isChecked())
        # self.select_height_box.setDisabled(self.to_compare_coverage_coverage_checkbox.isChecked())
        # self.select_width_box.setDisabled(self.to_compare_coverage_coverage_checkbox.isChecked())
        # self.select_minimal_area_coverage_box.setDisabled(self.to_compare_coverage_coverage_checkbox.isChecked())
        # self.nodes_amount_box.setDisabled(self.to_compare_coverage_coverage_checkbox.isChecked())
        # self.nodes_battery_capacity_box.setDisabled(self.to_compare_coverage_coverage_checkbox.isChecked())

        ######################################
        # Runtime info panel layout creation #
        ######################################

        # Runtime information
        self.runtime_info_layout = QFormLayout()

        # Displays the naive alg. times label
        self.naive_label = QLabel()
        self.naive_label.setText("Ilość iteracji algorytmu naiwnego:")

        # Displays the naive average run times
        self.naive_fnd = QLabel()
        self.naive_fnd.setText("0")

        # Displays the naive last run time
        self.naive_hnd = QLabel()
        self.naive_hnd.setText("0")

        # Displays the naive last run time
        self.naive_lnd = QLabel()
        self.naive_lnd.setText("0")

        # Displays the pso alg. times label
        self.pso_label = QLabel()
        self.pso_label.setText("Ilość iteracji algorytmu PSO:")

        # Displays the pso average run times
        self.pso_fnd = QLabel()
        self.pso_fnd.setText("0")

        # Displays the pso hnd
        self.pso_hnd = QLabel()
        self.pso_hnd.setText("0")

        # Displays the pso lnd
        self.pso_lnd = QLabel()
        self.pso_lnd.setText("0")

        self.active_nodes_amount_label = QLabel()
        self.active_nodes_amount_label.setText("Ilość pozostałych sensoróœ")

        self.active_nodes = QLabel()

        # Adding the labels to the layout
        self.runtime_info_layout.addWidget(self.naive_label)
        self.runtime_info_layout.addRow("FND:", self.naive_fnd)
        self.runtime_info_layout.addRow("HND:", self.naive_hnd)
        self.runtime_info_layout.addRow("LND:", self.naive_lnd)
        self.runtime_info_layout.addWidget(self.pso_label)
        self.runtime_info_layout.addRow("FND:", self.pso_fnd)
        self.runtime_info_layout.addRow("HND:", self.pso_hnd)
        self.runtime_info_layout.addRow("LND:", self.pso_lnd)
        self.runtime_info_layout.addWidget(self.active_nodes_amount_label)
        self.runtime_info_layout.addRow("Aktywne sensory:", self.active_nodes)

        #######################################################
        # Adding created layouts to the outer settings layout #
        #######################################################

        # Adding the final "run" button to the layout
        self.run_simulation_button = QPushButton()
        self.run_simulation_button.clicked.connect(self.run_simulation)
        self.run_simulation_button.setText("Uruchom symulację!")

        self.settingsLayout.addLayout(self.algorithm_layout)
        self.settingsLayout.addLayout(self.area_dimensions_layout)
        self.settingsLayout.addLayout(self.node_settings_layout)
        self.settingsLayout.addLayout(self.repetition_amount_layout)
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

        ######################
        # Connecting Signals #
        ######################

        self.backend.signal_send_algorithms_list.connect(
            self.select_algorithm_combo.addItems
        )
        self.backend.signal_send_current_algorithm.connect(self.set_current_algorithm)
        self.backend.signal_send_height.connect(self.set_local_height)
        self.backend.signal_send_width.connect(self.set_local_width)
        self.backend.signal_send_minimum_coverage.connect(
            self.select_minimal_area_coverage_box.setText
        )
        self.backend.signal_send_node_amount.connect(self.set_node_amount)
        self.backend.signal_send_node_battery_capacity.connect(
            self.nodes_battery_capacity_box.setText
        )

        self.backend.signal_update_plot.connect(self.draw_plot)

        self.backend.signal_send_fnd_naive.connect(self.set_fnd_naive)
        self.backend.signal_send_hnd_naive.connect(self.set_hnd_naive)
        self.backend.signal_send_lnd_naive.connect(self.set_lnd_naive)
        self.backend.signal_send_fnd_pso.connect(self.set_fnd_pso)
        self.backend.signal_send_hnd_pso.connect(self.set_hnd_pso)
        self.backend.signal_send_lnd_pso.connect(self.set_lnd_pso)

        self.backend.signal_send_coverage_delta_data_naive.connect(
            self.append_coverage_delta_data_naive
        )
        self.backend.signal_send_coverage_delta_data_pso.connect(
            self.append_coverage_delta_data_pso
        )

        self.backend.signal_send_simulation_finished.connect(
            self.set_simulation_finished
        )
        self.backend.signal_send_active_nodes.connect(self.set_active_nodes)

        ####################################
        # Emitting signals to get the data #
        ####################################

        self.backend.signal_get_algorithms_list.emit()
        self.backend.signal_get_height.emit()
        self.backend.signal_get_width.emit()
        self.backend.signal_get_node_amount.emit()
        self.backend.signal_get_node_battery_capacity.emit()
        self.backend.signal_get_minimum_coverage_value.emit()
        self.backend.signal_initiate_network.emit()
        self.backend.signal_draw_plot.emit()

        print(self.select_minimal_area_coverage_box.text())
        print(self.nodes_amount_box.text())
        self.m_DataCollector.set_coverage(
            int(self.select_minimal_area_coverage_box.text())
        )
        self.m_DataCollector.set_nodes_amount(int(self.nodes_amount_box.text()))

        # Setting as central
        self.setCentralWidget(self.main_widget)

        # Showing the layout on the screen
        self.show()

        # Starting the thread
        self.m_BackendThread.start()

    def to_plot(self, index):
        if index == 0:
            self.m_ToPlot = False
        elif index == 1:
            self.m_ToPlot = True
            if self.m_Repeat < 2:
                self.select_algorithm_combo.setEnabled(True)
                self.select_height_box.setEnabled(True)
                self.select_width_box.setEnabled(True)
                self.select_minimal_area_coverage_box.setEnabled(True)
                self.nodes_amount_box.setEnabled(True)
                self.nodes_battery_capacity_box.setEnabled(True)
                self.repetition_amount_combo.setEnabled(True)
                self.to_plot_combo.setEnabled(True)

                self.to_plot_combo.setChecked(False)
                self.to_compare_coverage_checkbox.setChecked(False)
                self.to_compare_runtime_stats_checkbox.setChecked(False)

                msg = QMessageBox()
                msg.setText("Sprawdź parametry!")
                msg.setInformativeText(
                    "Nie można utworzyć wykresu porównawczego, jeżeli wykonano symulację mniej niż 2 razy!"
                )
                msg.setWindowTitle("Uwaga!")
                msg.exec()

    def to_compare_coverage(self, index):
        if index == 0:
            self.m_ToCompareCoverage = False

            print("Jest tam")
        elif index == 1:
            self.m_ToCompareCoverage = True

            # Warning the user that the data cannot be changed now
            msg = QMessageBox()
            msg.setText("Double check the parameters!")
            msg.setInformativeText(
                "If you want the comparsion to work, you musn't change the runtime parameters after the work has started!"
            )
            msg.setWindowTitle("Remember!")
            msg.exec()

    def to_compare_runtime_stats(self, index):
        if index == 0:
            self.m_ToCompareRuntimeStats = False

            print("Jest tam")
        elif index == 1:
            self.m_ToCompareRuntimeStats = True

            # Warning the user that the data cannot be changed now
            msg = QMessageBox()
            msg.setText("Double check the parameters!")
            msg.setInformativeText(
                "If you want the comparsion to work, you musn't change the runtime parameters after the work has started!"
            )
            msg.setWindowTitle("Remember!")
            msg.exec()

    def set_current_algorithm(self, name=str):
        if self.backend.mutex.tryLock():
            self.m_CurrentAlgorithm = name
        self.backend.mutex.unlock()

    def set_node_amount(self, name=int):
        if self.backend.mutex.tryLock():
            self.m_NodeAmount = name
        self.backend.mutex.unlock()
        self.m_DataCollector.set_nodes_amount(name)
        self.nodes_amount_box.setText(str(self.m_NodeAmount))

    def set_fnd_naive(self, value=int):
        if self.backend.mutex.tryLock():
            self.m_NaiveRoundData[0] = value
        self.backend.mutex.unlock()
        self.naive_fnd.setText(str(self.m_NaiveRoundData[0]))

    def set_hnd_naive(self, value=int):
        if self.backend.mutex.tryLock():
            self.m_NaiveRoundData[1] = copy(value)
        self.backend.mutex.unlock()
        self.naive_hnd.setText(str(self.m_NaiveRoundData[1]))

    def set_lnd_naive(self, value=int):
        if self.backend.mutex.tryLock():
            self.m_NaiveRoundData[2] = copy(value)
        self.backend.mutex.unlock()
        self.naive_lnd.setText(str(self.m_NaiveRoundData[2]))

    def set_fnd_pso(self, value=int):
        if self.backend.mutex.tryLock():
            self.m_psoRoundData[0] = copy(value)
        self.backend.mutex.unlock()
        self.pso_fnd.setText(str(self.m_psoRoundData[0]))

    def set_hnd_pso(self, value=int):
        if self.backend.mutex.tryLock():
            self.m_psoRoundData[1] = copy(value)
        self.backend.mutex.unlock()
        self.pso_hnd.setText(str(self.m_psoRoundData[1]))

    def set_lnd_pso(self, value=int):
        if self.backend.mutex.tryLock():
            self.m_psoRoundData[2] = copy(value)
        self.backend.mutex.unlock()
        self.pso_lnd.setText(str(self.m_psoRoundData[2]))

    def append_coverage_delta_data_naive(self, data=tuple):
        self.m_NaiveCoverageData.append(data)

    def append_coverage_delta_data_pso(self, data=tuple):
        self.m_PsoCoverageData.append(data)

    def set_simulation_finished(self, value=bool):
        if self.backend.mutex.tryLock():
            self.m_SimulationRoundFinished = copy(value)
        self.backend.mutex.unlock()

    def set_active_nodes(self, value=int):
        if self.backend.mutex.tryLock():
            self.m_ActiveNodes = value
        self.backend.mutex.unlock()
        self.active_nodes.setText(str(self.m_ActiveNodes))

    def set_repetition(self, index=int):
        self.m_Repeat = int(self.m_RepetitionValues[index])
        self.m_DataCollector.clear()

    def set_algorithm(self, index=int):
        self.backend.signal_set_algorithm.emit(index)

    def set_height(self, height=str):
        if height != "":
            if int(height) > 0 and int(height) < 20000:
                self.backend.signal_set_height.emit(int(height))
                self.backend.signal_get_height.emit()

        self.m_DataCollector.clear()

    def set_local_height(self, height=int):
        if self.backend.mutex.tryLock():
            self.m_Height = copy(height)
        self.backend.mutex.unlock()
        self.select_height_box.setText(str(self.m_Height))

        self.m_DataCollector.clear()

    def set_width(self, width=str):
        if width != "":
            if int(width) > 0 and int(width) < 20000:
                self.backend.signal_set_width.emit(int(width))
                self.backend.signal_get_width.emit()

        self.m_DataCollector.clear()

    def set_local_width(self, width=int):
        if self.backend.mutex.tryLock():
            self.m_Width = copy(width)
        self.backend.mutex.unlock()
        self.select_width_box.setText(str(self.m_Width))

        self.m_DataCollector.clear()

    def set_minimal_coverage(self, coverage=str):
        if int(coverage) > 0 and int(coverage) <= 100:
            self.backend.signal_set_minimum_coverage_value.emit(int(coverage))
            self.backend.signal_get_minimum_coverage_value.emit()
            self.m_DataCollector.set_coverage(coverage)

        else:
            print("Here I must show and error with OK button")

        self.m_DataCollector.clear()

    def set_nodes_amount(self, amount=str):
        if amount != "":
            if int(amount) > 0 and int(amount) < 2000:
                self.backend.signal_set_node_amount.emit(int(amount))
                self.backend.signal_get_node_amount.emit()

        self.m_DataCollector.clear()

    def set_nodes_battery_capacity(self, capacity=str):
        if capacity != "":
            if int(capacity) > 0 and int(capacity) < 5000:
                self.backend.signal_set_node_battery_capacity.emit(int(capacity))
                self.backend.signal_get_node_battery_capacity.emit()

        self.m_DataCollector.clear()

    def draw_plot(self, temp):
        # Clearing the axes
        self.area_widget.clearAxes()

        # Getting the data from the thread
        if self.backend.mutex.tryLock():
            self.m_PlotData = copy(temp)
        self.backend.mutex.unlock()

        self.area_widget.createAreaPlot(
            self.m_PlotData[0], self.m_PlotData[1], self.m_PlotData[2]
        )

        self.area_widget.updateAxes()

    # Runs the amount of repeated simulations desired
    def run_simulation(self):
        self.m_DataCollector.add_rounds_number(int(self.m_Repeat))
        self.backend.signal_get_current_algorithm.emit()

                        # Taking the data from algorithms combobox
        algorithms = [
            self.select_algorithm_combo.itemText(i)
            for i in range(self.select_algorithm_combo.count())
        ]

        for amount in range(self.m_Repeat):
            if not self.m_ToCompareCoverage and not self.m_ToCompareRuntimeStats:

                self.backend.signal_run_simulation.emit()

                print("Zyje")

                while not self.m_SimulationRoundFinished:
                    sleep(0.15)
                    print("Attempted an update")
                    self.backend.calculate_plot_data().emit()
                    sleep(0.15)

                if self.m_ToPlot:
                    if self.m_CurrentAlgorithm == algorithms[0]:
                        self.m_DataCollector.add_naive_round_data(self.m_NaiveRoundData)
                        self.m_DataCollector.add_naive_coverage_data(
                            self.m_NaiveCoverageData
                        )
                    if self.m_CurrentAlgorithm == algorithms[1]:
                        self.m_DataCollector.add_pso_round_data(self.m_psoRoundData)
                        self.m_DataCollector.add_pso_coverage_data(
                            self.m_PsoCoverageData
                        )

                self.m_NaiveRoundData = [0, 0, 0]
                self.m_psoRoundData = [0, 0, 0]
                print("PSO coverage data len: " + str(len(self.m_PsoCoverageData)))
                print("Naive coverage data len: " + str(len(self.m_NaiveCoverageData)))
                self.m_PsoCoverageData.clear()
                self.m_NaiveCoverageData.clear()

            else:
                for index in range(len(algorithms)):
                    self.set_algorithm(index)
                    
                    self.backend.signal_run_simulation.emit()

                    while not self.m_SimulationRoundFinished:
                        sleep(0.15)
                        self.backend.calculate_plot_data().emit()
                        sleep(0.15)

                    # Continues with another round
                    self.m_SimulationRoundFinished = True

                    if algorithms[index] == algorithms[0]:
                        self.m_DataCollector.add_naive_round_data(self.m_NaiveRoundData)
                        self.m_DataCollector.add_naive_coverage_data(
                            self.m_NaiveCoverageData
                        )
                    if algorithms[index] == algorithms[1]:
                        self.m_DataCollector.add_pso_round_data(self.m_psoRoundData)
                        self.m_DataCollector.add_pso_coverage_data(
                            self.m_PsoCoverageData
                        )

                    self.m_NaiveRoundData = [0, 0, 0]
                    self.m_psoRoundData = [0, 0, 0]
                    self.m_PsoCoverageData.clear()
                    self.m_NaiveCoverageData.clear()

            # Continues with another round
            self.m_SimulationRoundFinished = False

        # DataCollector has to give back the info whether the naive simulation has been run
        timestr = time.strftime("%Y%m%d-%H%M%S")

        self.m_DataCollector.set_plot_name(
            str(
                self.m_CurrentAlgorithm
                + "_"
                + str(self.m_NodeAmount)
                + "_"
                + str(self.m_Height)
                + "_"
                + str(self.m_Width)
                + "_"
                + str(self.m_Repeat)
                + "_"
                + timestr
            )
        )

        print(self.m_DataCollector.mv_PlotName)

        if self.m_ToPlot and (
            not self.m_ToCompareCoverage and not self.m_ToCompareRuntimeStats
        ):
            self.m_DataCollector.save_separate_plot()
            self.m_DataCollector.clear()

        if (
            self.m_ToPlot and self.m_ToCompareCoverage
        ) and not self.m_ToCompareRuntimeStats:
            self.m_DataCollector.save_separate_plot()
            self.m_DataCollector.save_coverage_comparsion_plot()
            self.m_DataCollector.clear()

        if self.m_ToPlot and self.m_ToCompareCoverage and self.m_ToCompareRuntimeStats:
            self.m_DataCollector.save_separate_plot()
            self.m_DataCollector.save_coverage_comparsion_plot()
            self.m_DataCollector.save_runtime_comparsion_plot()
            self.m_DataCollector.clear()