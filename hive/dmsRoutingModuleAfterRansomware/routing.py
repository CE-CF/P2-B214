import numpy as np
from coordinates import Coordinates
from routingpackage.findfunctions import find_functions
import routingpackage.findroutefunctions
from plots import Plot, show_plots


class Routing(Coordinates):

    functions = np.empty(0)
    plots = []

    def __init__(self, coordinates):
        super().__init__(coordinates)

    def analyze_coordinates(self):
        self.functions = find_functions(self.local_c)
        self.plots.append(Plot(self.local_c, self.functions))
        origo_c = self.global_c[self.find_origo()]
        routingpackage.findroutefunctions.run(self.global_c, self.local_c, self.functions, origo_c)
        self.plots.append(routingpackage.findroutefunctions.getPlot())
        show_plots(self.plots)
