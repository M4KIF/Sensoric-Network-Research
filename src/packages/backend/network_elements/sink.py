
#########################################################
# A special type of a Node, that collects the data      #
# and gets it ready to be taken to the research centre, #
# or passes it to another sink node that sits at a      #
# higher level in the Network hierarchy (if a multi     #
# cluster network routing design is used)               #
#########################################################



###########
# Imports #
###########

from .node import Node

#####################
# Object definition #
#####################


# Inherited from Node class
class Sink(Node):

    ###########################
    # Variables/Member object #
    ###########################


    ###########
    # Methods #
    ###########

    def __init__(self):
        print()