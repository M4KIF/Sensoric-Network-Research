##############################
# Sensoric network simulator #
##############################

This app emulates the functioning of a wireless sensor network. It implements the simplified network connection model 
and simplified energy consumption model. Which are described in the technical document available in the \docs.

It enables the user to change any important parameter of the wsn. The likes of network area, nodes amount, minimal coverage,
as also the amount of simulation runs to execute.

As a bonus, this program is capable of saving the simulation data to a png file with a plot, that describes the FND(First Node Died),
HND(Half Node Dead) and LND (Last Node Died) parameters values.

The simulation can be run with the use of a naive algorithm, or a particle swarm optimisation routing algorithm.

The modules used in this application:
- pyqt // GUI and threading
- shapely // Point on plane, object on plane, sets calculations
- matplotlib // Plotting of the wsn nodes data and simulation data
- scipy // Used for the psudo-random generator that uses the uniform distribution
