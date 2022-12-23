
##########################################
# Energy usage table object,             #
# contains the values of energy          #
# consumed by every registered actions   #
# that a WSN node can do                 #
#                                        #
# Implemented as a Singleton creational  #
# design, to prevent it from existing in #
# more than one copy                     #
##########################################

# Learning from:
# https://refactoring.guru/design-patterns/singleton/python/example#example-1
# https://realpython.com/python-metaclasses/



############
# Includes #
############

from threading import Lock, Thread

class EnergyUsageMeta(type):

    _instances = {}

    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class EnergyUsage(metaclass=EnergyUsageMeta):
    value: str = None

    def __init__(self, value: str) -> None:
        self.value = value

    def some_business_logic(self):
        print()


#########################################
# Mean energy usage figures based on    #
# an article titled "Power consumption  #
# measurements of WSN based on Arduino" #
# by U T Salim et al 2021 IOP Conf.     #
# Ser.: Mater. Sci. Eng. 1152 012022    #
#########################################



###################
# Variables in mW #
###################

# Energy that transmitting the data take
transmiter_action = 650

# Energy that data receiving take
receiver_action = 500

# Energy that the sensors take while collecting data
sensors_action = 350

# Energy that either sensing data/receiving/transmitting/
# neighbour_locating calculations take
computing_action = 250