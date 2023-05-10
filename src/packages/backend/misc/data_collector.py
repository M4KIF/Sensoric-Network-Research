
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

#####################
# Object Definition #
#####################

class DataCollector():

    def __init__(self):

        ############################################
        # Lists of times for particular sollutions #
        ############################################

        # Contains the list of naive algorithm runtimes
        self.ml_NaiveSollutionFND = []
        self.ml_NaiveSollutionHND = []
        self.ml_NaiveSollutionLND = []

        # Contains the list of optimised algorithm runtimes
        self.ml_OptimisedSollutionFND = []
        self.ml_OptimisedSollutionHND = []
        self.ml_OptimisedSollutionLND = []

        self.mv_PlotName = str()

        self.mb_NaiveData = False
        self.mb_OptimisedData = False


    ##############################
    # Member methods definitions #
    ##############################


    def add_naive_round_data(self, data):
        self.mb_NaiveData = True
        self.ml_NaiveSollutionFND.append(data[0])
        self.ml_NaiveSollutionHND.append(data[1])
        self.ml_NaiveSollutionLND.append(data[2])


    def add_optimised_round_data(self, data):
        self.mb_OptimisedData = True
        self.ml_OptimisedSollutionFND.append(data[0])
        self.ml_OptimisedSollutionHND.append(data[1])
        self.ml_OptimisedSollutionLND.append(data[2])

    
    def add_rounds_number(self, amount):
        self.mv_Rounds = amount


    def set_plot_name(self, name):
        self.mv_PlotName = name

    def save_plot(self):
        if self.mb_NaiveData:
            if not len(self.ml_NaiveSollutionFND) < 2:
                # Setting the labels
                plt.xlabel('Simulation runs count')
                plt.ylabel('Rounds')

                # Plotting the data
                plt.plot(self.ml_NaiveSollutionFND, label="FND")
                plt.plot(self.ml_NaiveSollutionHND, label="HND")
                plt.plot(self.ml_NaiveSollutionLND, label="LND")

                # Showing the legend
                plt.legend()

                # Saving the figure
                plt.savefig("lnd_runtime_details"+self.mv_PlotName)

                print("Top-bottom == FND - LND")
                print(self.ml_NaiveSollutionFND)
                print(self.ml_NaiveSollutionHND)
                print(self.ml_NaiveSollutionLND)

        elif self.mb_OptimisedData:
            if not len(self.ml_OptimisedSollutionFND) < 2:
                # Setting the labels
                plt.xlabel('Simulation runs count')
                plt.ylabel('Rounds')

                # Plotting the data
                plt.plot(self.ml_OptimisedSollutionFND, label="FND")
                plt.plot(self.ml_OptimisedSollutionHND, label="HND")
                plt.plot(self.ml_OptimisedSollutionLND, label="LND")

                # Showing the legend
                plt.legend()

                # Saving the figure
                plt.savefig("lnd_runtime_details" + self.mv_PlotName)

                # Printing the data to the console
                print("Top-bottom == FND - LND")
                print(self.ml_OptimisedSollutionFND)
                print(self.ml_OptimisedSollutionHND)
                print(self.ml_OptimisedSollutionLND)



    def clear(self):
        self.mb_OptimisedData = False
        self.mb_NaiveData = False

        self.mv_PlotName = ''
        plt.cla()

        self.ml_NaiveSollutionFND.clear()
        self.ml_NaiveSollutionHND.clear()
        self.ml_NaiveSollutionLND.clear()

        self.ml_OptimisedSollutionFND.clear()
        self.ml_OptimisedSollutionHND.clear()
        self.ml_OptimisedSollutionLND.clear()