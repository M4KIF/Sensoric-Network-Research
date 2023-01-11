
######################################
# Collects the data from the runtime #
# and then stores it, to enable a    #
# quick comparsion between runtimes  #
######################################



###########
# Imports #
###########

import time

#####################
# Object Definition #
#####################

class DataCollector():

    def __init__(self):

        ############################################
        # Lists of times for particular sollutions #
        ############################################

        # Contains the list of naive algorithm runtimes
        self.ml_NaiveSollutionTimes = []

        # Contains the list of optimised algorithm runtimes
        self.ml_OptimisedSollutionTimes = []

        ###############################################
        # Last times of the simulation runs variables #
        ###############################################

        # Contains the latest result of a naive algorithm wsn simulation
        self.mv_NaiveLastTime = float(0)

        # Contains the latest result of an optimised wsn simulation
        self.mv_OptimisedLastTime = float(0)

        #####################
        # Runtime variables #
        #####################

        self.mv_MeasureStarted = float
        self.mv_MeasureEnded = float
        self.mv_MeasurementResult = float

        ############
        # Booleans #
        ############

        # Activated if there is a time measure running currently
        self.mb_Measuring = False

        # Activated if there is some data after the measurement that hasn't been saved yet
        self.mb_DataMeasuredNotSaved = False


    ##############################
    # Member methods definitions #
    ##############################


    # Returns the value according to the flag
    def is_ready_to_measure(self):
        if not (self.mb_Measuring and self.mb_DataMeasuredNotSaved):
            return True
        else:
            return False


    # Returns the value according to the flag
    def is_measuring(self):
        if self.mb_Measuring:
            return True
        else:
            return False


    # Returns the value according to the flag
    def is_there_is_data_to_be_saved(self):
        if self.mb_DataMeasuredNotSaved:
            return True
        else:
            return False


    # Starts the measurement
    def start_timer(self):

        if not self.mb_Measuring:
            # Updating the time on the first variable
            self.mv_MeasureStarted = time.time()

            # Activating the measurement flag
            self.mb_Measuring = True
        else:
            # if the timer can't be started throwning an exception
            raise Exception("Measurement Running")

    
    # Ends the measurement
    def end_timer(self):
        if self.mb_Measuring:

            # Updating the measurement end time
            self.mv_MeasureEnded = time.time()

            # Calculating the result
            self.mv_MeasurementResult = self.mv_MeasureEnded - self.mv_MeasureStarted

            # Deactivating the measurement flag
            self.mb_Measuring = False
            self.mb_DataMeasuredNotSaved = True


    # Saves the result to the naive parameters
    def save_result_as_naive(self):

        if self.mb_DataMeasuredNotSaved:
            # Saving to the naive variable
            self.mv_NaiveLastTime = self.mv_MeasurementResult

            # Appending the results list
            self.ml_NaiveSollutionTimes.append(self.mv_NaiveLastTime)

            self.mb_DataMeasuredNotSaved = False
        else:
            raise Exception("There is nothing to be saved")


    # Saves the results to the optimised parameters
    def save_result_as_optimised(self):

        if self.mb_DataMeasuredNotSaved:
            # Saving to the naive variable
            self.mv_OptimisedLastTime = self.mv_MeasurementResult

            # Appending the results list
            self.ml_OptimisedSollutionTimes.append(self.mv_OptimisedLastTime)

            self.mb_DataMeasuredNotSaved = False
        else:
            raise Exception("There is nothing to be saved")


    # Calculates the mean from the list of times for the naive sollution
    def calculate_mean_from_naive_times(self):

        if len(self.ml_NaiveSollutionTimes) != 0:
            result = 0
            for time in self.ml_NaiveSollutionTimes:
                result+=time
            return result / len(self.ml_NaiveSollutionTimes)
        else:
            raise Exception("Not enough results in the list")


    # Calculates the mean from the list of times for the optimised sollution
    def calculate_mean_from_optimised_times(self):

        if len(self.ml_OptimisedSollutionTimes) != 0:
            result = 0
            for time in self.ml_OptimisedSollutionTimes:
                result+=time
            return result / len(self.ml_OptimisedSollutionTimes)
        else:
            raise Exception("Not enough results in the list")