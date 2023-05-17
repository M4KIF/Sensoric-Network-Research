######################################
# Collects the data from the runtime #
# and then stores it, to enable a    #
# quick comparsion between runtimes  #
######################################


###########
# Imports #
###########

import time
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from copy import copy

#####################
# Object Definition #
#####################


class DataCollector:
    def __init__(self):
        ############################################
        # Lists of times for particular sollutions #
        ############################################

        # Contains the list of naive algorithm runtimes
        self.ml_NaiveSollutionFND = []
        self.ml_NaiveSollutionHND = []
        self.ml_NaiveSollutionLND = []

        # Could store ten tuple lists of data
        self.ml_NaiveCoverageData = []

        # Contains the list of optimised algorithm runtimes
        self.ml_OptimisedSollutionFND = []
        self.ml_OptimisedSollutionHND = []
        self.ml_OptimisedSollutionLND = []

        # Same as above
        self.ml_PsoCoverageData = []

        self.ml_PsoCoverageMean = []
        self.ml_NaiveCoverageMean = []

        self.mv_NodesAmount = float()
        self.mv_Coverage = int()

        self.mv_PlotName = str()

        self.mb_NaiveRuntimeDataAquired = False
        self.mb_PsoRuntimeDataAquired = False

        self.mb_NaiveCoverageDataAquired = False
        self.mb_PsoCoverageDataAquired = False

        self.mb_NaiveCoverageMeanCalculated = False
        self.mb_PsoCoverageMeanCalculated = False

    ##############################
    # Member methods definitions #
    ##############################

    def can_compare_coverage():
        return mb_NaiveRuntimeDataAquired == mb_PsoRuntimeDataAquired

    def can_compare_runtime():
        return mb_NaiveCoverageDataAquired == mb_PsoCoverageDataAquired

    def add_naive_round_data(self, data):
        self.mb_NaiveRuntimeDataAquired = True
        self.ml_NaiveSollutionFND.append(data[0])
        self.ml_NaiveSollutionHND.append(data[1])
        self.ml_NaiveSollutionLND.append(data[2])

    def add_pso_round_data(self, data):
        self.mb_PsoRuntimeDataAquired = True
        self.ml_OptimisedSollutionFND.append(data[0])
        self.ml_OptimisedSollutionHND.append(data[1])
        self.ml_OptimisedSollutionLND.append(data[2])

    def add_naive_coverage_data(self, data):
        self.mb_NaiveCoverageDataAquired = True

        self.ml_NaiveCoverageData.append(copy(data))

    def add_pso_coverage_data(self, data):
        self.mb_PsoCoverageDataAquired = True

        self.ml_PsoCoverageData.append(copy(data))

    def add_rounds_number(self, amount):
        self.mv_Rounds = amount

    def set_plot_name(self, name):
        self.mv_PlotName = name

    def set_nodes_amount(self, amount):
        self.mv_NodesAmount = amount

    def set_coverage(self, coverage):
        self.mv_Coverage = coverage

    def calculate_pso_coverage_mean(self):
        print("Tez dotarlo do pso")
        iterations_mean = []

        # Initialising the
        for i in range(len(self.ml_PsoCoverageData[0])):
            iterations_mean.append(int(0))

        for item in self.ml_PsoCoverageData:
            for t in range(len(item)):
                iterations_mean[t] += item[t][1]

        for i in range(len(self.ml_PsoCoverageData[0])):
            iterations_mean[i] /= len(self.ml_PsoCoverageData)

        return iterations_mean

    def calculate_naive_coverage_mean(self):
        print("Weszlo")
        iterations_mean = []

        # Initialising the
        for i in range(len(self.ml_NaiveCoverageData[0])):
            iterations_mean.append(int(0))

        for item in self.ml_NaiveCoverageData:
            for t in range(len(item)):
                iterations_mean[t] += item[t][1]

        for i in range(len(self.ml_NaiveCoverageData[0])):
            iterations_mean[i] /= len(self.ml_NaiveCoverageData)
            print(iterations_mean[i])

        # iterations_mean.sort(reverse=True)

        return iterations_mean

    def save_separate_plot(self):

        if self.mb_NaiveRuntimeDataAquired:
            # Setting the labels
            plt.xlabel("Simulation runs count")
            plt.ylabel("Rounds")

            # Plotting the runtime data
            plt.plot(self.ml_NaiveSollutionFND, label="FND")
            plt.plot(self.ml_NaiveSollutionHND, label="HND")
            plt.plot(self.ml_NaiveSollutionLND, label="LND")

            plt.legend()

            # Saving the runtime plot
            plt.savefig("naive_runtime_" + self.mv_PlotName)

            plt.cla()

        if self.mb_PsoRuntimeDataAquired:
            # Setting the labels
            plt.xlabel("Simulation runs count")
            plt.ylabel("Rounds")

            # Plotting the data
            plt.plot(self.ml_OptimisedSollutionFND, label="FND")
            plt.plot(self.ml_OptimisedSollutionHND, label="HND")
            plt.plot(self.ml_OptimisedSollutionLND, label="LND")

            # Showing the legend
            plt.legend()

            # Saving the figure
            plt.savefig("pso_runtime_" + self.mv_PlotName)

            plt.cla()

        if self.mb_NaiveCoverageDataAquired:
            # Adding appropriate labels to the plot
            plt.xlabel("Algorithm Iterations")
            plt.ylabel("Coverage")

            # Calculating the data out of the runs
            mean = self.calculate_naive_coverage_mean()

            # Calculating the coverage data out of the runs
            nodes_dead = [
                (100 - (i + 1) * 100 / self.mv_NodesAmount) for i in range(len(mean))
            ]
            nodes_dead.sort(reverse=True)

            plt.plot(mean, nodes_dead, label="Naive")

            plt.legend()

            plt.savefig("naive_coverage_mean_" + self.mv_PlotName)

            plt.cla()

        if self.mb_PsoCoverageDataAquired:
            # Adding appropriate labels to the plot
            plt.xlabel("Algorithm Iterations")
            plt.ylabel("Coverage")

            # I should take a median out of the data
            mean = self.calculate_pso_coverage_mean()

            # Calculating the coverage data out of the runs
            nodes_dead = [
                (100 - (i + 1) * 100 / self.mv_NodesAmount) for i in range(len(mean))
            ]
            nodes_dead.sort(reverse=True)

            plt.plot(mean, nodes_dead, label="PSO")

            plt.legend()

            plt.savefig("pso_coverage_mean_" + self.mv_PlotName)

            plt.cla()

        # Debug
        print("(PSO)Top-bottom == FND - LND")
        print(self.ml_OptimisedSollutionFND)
        print(self.ml_OptimisedSollutionHND)
        print(self.ml_OptimisedSollutionLND)

        print("(Naive)Top-bottom == FND - LND")
        print(self.ml_NaiveSollutionFND)
        print(self.ml_NaiveSollutionHND)
        print(self.ml_NaiveSollutionLND)

    def save_runtime_comparsion_plot(self):
        if self.mb_NaiveRuntimeDataAquired and self.mb_PsoRuntimeDataAquired:
            plt.xlabel("Simulation runs count")
            plt.ylabel("Rounds")

            # I should take a median out of the data
            mean_pso = self.calculate_pso_coverage_mean()
            mean_naive = self.calculate_naive_coverage_mean()

            plt.plot(self.ml_OptimisedSollutionFND, label="FND-PSO")
            plt.plot(self.ml_OptimisedSollutionHND, label="HND-PSO")
            plt.plot(self.ml_OptimisedSollutionLND, label="LND-PSO")

            plt.plot(self.ml_NaiveSollutionFND, label="FND-Naive")
            plt.plot(self.ml_NaiveSollutionHND, label="HND-Naive")
            plt.plot(self.ml_NaiveSollutionLND, label="LND-Naive")

            plt.legend()

            plt.savefig("runtime_comparsion_" + self.mv_PlotName)

            plt.cla()

    def save_coverage_comparsion_plot(self):
        if self.mb_NaiveCoverageDataAquired and self.mb_PsoCoverageDataAquired:
            plt.ylabel("Algorithm Iterations")
            plt.xlabel("Nodes Dead")

            # I should take a median out of the data
            mean_pso = self.calculate_pso_coverage_mean()
            mean_naive = self.calculate_naive_coverage_mean()

            nodes_dead_pso = [
                (100 - (i + 1) * 100 / self.mv_NodesAmount)
                for i in range(len(mean_pso))
            ]
            nodes_dead_naive = [
                (100 - (i + 1) * 100 / self.mv_NodesAmount)
                for i in range(len(mean_naive))
            ]

            nodes_dead_pso.sort(reverse=True)
            nodes_dead_naive.sort(reverse=True)

            plt.plot(mean_pso, nodes_dead_pso, label="PSO")
            plt.plot(mean_naive, nodes_dead_naive, label="Naive")

            plt.legend()

            plt.savefig("coverage_comparsion_" + self.mv_PlotName)

            plt.cla()

    def clear(self):
        self.mb_PsoRuntimeDataAquired = False
        self.mb_NaiveRuntimeDataAquired = False
        self.mb_NaiveCoverageDataAquired = False
        self.mb_PsoCoverageDataAquired = False

        self.mv_PlotName = ""
        plt.cla()

        self.ml_NaiveSollutionFND.clear()
        self.ml_NaiveSollutionHND.clear()
        self.ml_NaiveSollutionLND.clear()

        self.ml_OptimisedSollutionFND.clear()
        self.ml_OptimisedSollutionHND.clear()
        self.ml_OptimisedSollutionLND.clear()

        self.ml_NaiveCoverageData.clear()
        self.ml_PsoCoverageData.clear()