import numpy as np
from coordinates import Coordinates
from routingpackage.findfunctions import find_functions
from routingpackage.findroutefunctions import run, getPlot
from plots import Plot, show_plots


class Routing(Coordinates):

    functions = np.empty(0)
    plots = []

    def __init__(self, coordinates):
        super().__init__(coordinates)

    def analyze_coordinates(self):
        self.functions = find_functions(self.local_c)
        print(self.functions)
        self.plots.append(Plot(self.local_c, self.functions))
        run(self.local_c, self.functions)
        self.plots.append(getPlot())
        show_plots(self.plots)



