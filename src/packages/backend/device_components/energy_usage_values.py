
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

#####################
# Object definition #
#####################

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

class energy_usage():

