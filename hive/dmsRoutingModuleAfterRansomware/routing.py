import numpy as np
from coordinates import Coordinates
from routingpackage.findfunctions import find_functions
import routingpackage.findroutefunctions
from routingpackage.distanceinmeters import *
from plots import Plot, show_plots


class Routing(Coordinates):

    plot_padding = .01
    x_ratio, y_ratio = 0.0, 0.0     # local ratios for straight x- and y-lines
    functions = np.empty(0)
    plots = []

    def __init__(self, coordinates, plot_p):
        super().__init__(coordinates)
        self.plot_padding = plot_p

    def analyze_coordinates(self):
        self.functions = find_functions(self.local_c)
        self.append_plot(Plot(self.local_c, self.functions, 'r'))
        origo_c = self.global_c[self.find_origo()]
        self.x_ratio, self.y_ratio = get_x_y_meter_to_coordinates_ratio(origo_c)
        routingpackage.findroutefunctions.run(self.global_c, self.local_c, self.functions, origo_c, self.y_ratio)
        self.append_plot(routingpackage.findroutefunctions.get_plots())
        show_plots(self.plots, self.plot_padding)

    def append_plot(self, plots):
        if isinstance(plots, list):
            for i in range(len(plots)):
                self.plots.append(plots[i])
        else:
            self.plots.append(plots)
