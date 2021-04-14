import numpy as np
from coordinates import Coordinates
from routingpackage.findfunctions import find_functions
from plots import plot_points, plot_functions, plot


class Routing(Coordinates):

    functions = np.empty(0)

    def __init__(self, coordinates):
        super().__init__(coordinates)

    def analyze_coordinates(self):
        self.functions = find_functions(self.local_c)
        plot(self.local_c, self.functions)
