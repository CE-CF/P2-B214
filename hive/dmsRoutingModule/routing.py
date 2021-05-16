import numpy as np
from coordinates import Coordinates
from routingpackage.findfunctions import find_functions
import routingpackage.findroutefunctions
from routingpackage.distanceinmeters import *
from routingpackage.pathlimits import *
from plots import Plot, show_plots


# TLDR: the Routing-cass consists of the analyze-coordinates()-method that:
#   # finds border-functions to the local coordinate system
#   # adds plots of these functions together with the plots of the points
#   # finds the path-functions that the drone(s) need to follow                 <-- big important one
#   # adds plots of these functions and the points' projection-functions        (described in findroutefunctions.py)
#   # shows all the added plots

# Routing extends the Coordinates-class - this means that it can access the global and local coordinates that is defined
# in Coordinates. Routing can also use find_origo() and get_local_coordinates()
class Routing(Coordinates):
    longest_line_index = None
    path_width = 0
    ud_path_width = 0            # user defined path width
    plot_padding = .01
    x_ratio, y_ratio = 0.0, 0.0  # local ratios for straight x- and y-lines
    functions = np.empty(0)
    plots = []
    path_functions = []
    path_limit_points = []

    def __init__(self, coordinates, plot_p, udpw):
        super().__init__(coordinates)
        self.plot_padding = plot_p
        self.ud_path_width = udpw

    def get_path_limit_points(self):
        return self.path_limit_points

    def get_origo(self):
        return self.global_c[self.find_origo()]

    def get_path_functions(self):
        return self.path_functions

    def get_path_width(self):
        return self.path_width

    def analyze_coordinates(self):
        # we find the functions of the borders of the area - it returns a 2D-array [[slope][intersection], ..] of floats
        self.functions = find_functions(self.local_c)

        # print('{0:f}'.format(self.functions[3][0]))
        print("functions:")
        print(self.functions)

        # we append the plot-object of the borders and points to the plots-array(red lines, blue dots)
        # this way we can save the plots and show them at the same time - less inefficient...
        self.append_plot(Plot(self.local_c, self.functions, 'r', True))

        # we get the global coordinates of origo [lon, lat] = [x, y]
        # origo is then used to convert local coordinates back to global - calculate_distance only takes global_c
        origo_c = self.global_c[self.find_origo()]

        # we find the x- and y-axis ratios of coordinate-distances and distances in meters
        # this way we can convert back and forth between those
        # as long as we are working with vertical and horizontal distances - very useful
        self.x_ratio, self.y_ratio = get_x_y_meter_to_coordinates_ratio(origo_c)

        # print(self.x_ratio, self.y_ratio)

        # this function "run" goes through almost all functions in findroutefunctions.py
        # and it gets us an array consisting of functions of the paths(green lines) that the drone(s) need to follow
        self.path_functions, self.longest_line_index, self.path_width = \
            routingpackage.findroutefunctions.run(self.global_c, self.local_c, self.functions,
                                                  origo_c, self.x_ratio, self.y_ratio, self.ud_path_width)

        # print(self.path_functions)

        # in findroutefunctions.py we retrieve the functions of the points' projection(blue lines) onto the function of
        # the border line that is the longest
        self.append_plot(routingpackage.findroutefunctions.get_plots())

        pl = PathLimits(self.path_functions, self.functions, self.longest_line_index, self.local_c)
        self.path_limit_points = pl.run()

        # print(self.path_limit_points)

        self.append_plot(pl.get_plots())

        # after accumulating plots in the plots-array we are now able to show them all at once
        show_plots(self.plots, self.plot_padding)

    # the first if-statement checks if the plots-parameter is an array/list
    # if it is, it will iterate through the array/list while it appends each element to the plots-array
    # if it isn't it will just append that single element to the array
    def append_plot(self, plots):
        if isinstance(plots, list):
            for i in range(len(plots)):
                self.plots.append(plots[i])
        else:
            self.plots.append(plots)
