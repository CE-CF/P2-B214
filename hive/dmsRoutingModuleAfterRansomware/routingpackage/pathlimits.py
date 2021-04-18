from sympy import *
from scipy.optimize import fsolve
import numpy as np
from plots import Plot


class PathLimits:
    path_functions = []
    border_functions = []
    local_c = []
    plot_array = []
    longest_line_index = None

    def __init__(self, path_funcs, b_funcs, l_l_index, local_c):
        self.path_functions = path_funcs
        self.border_functions = b_funcs
        self.local_c = local_c
        self.longest_line_index = l_l_index

    # when a plot is created it's put as a parameter to this function
    # it then appends this plot to the array perp (for perpendicular)
    def set_plot(s, p):
        s.plot_array.append(p)

    # the Routing-class uses this function to get the saved Plot-objects from the perp-array
    def get_plots(s):
        return s.plot_array

    # returns a 2D-array of functions and a one-dimensional with the new array-values old index values
    # if you want to know the original index of the new function with index, lets say 2. then we do: original_index[2]
    def get_intersection_borders(s):
        intersection_functions = \
                   [s.border_functions[(s.longest_line_index - 1 % 4)],     # function clockwise to longest
                    s.border_functions[(s.longest_line_index + 2 % 4)],     # function opposite to longest
                    s.border_functions[(s.longest_line_index + 1 % 4)]]     # function counter-clockwise to longest

        original_indexes = [(s.longest_line_index - 1 % 4),
                            (s.longest_line_index + 2 % 4),
                            (s.longest_line_index + 1 % 4)]

        return intersection_functions, original_indexes

    def find_x_intersection(s, func1, func2):
        if func1[0] - func2[0] == 0:
            return 0
        else:
            if func1[1] - func2[1] == 0:
                return func1[1]
            else:
                return (func2[1] - func1[1]) / (func1[0] - func2[0])

    def get_path_limit_points(s, intersection_functions, original_indexes):
        point_array = []
        min_x = 0
        max_x = 0
        for i in range(len(s.path_functions)):
            for j in range(len(intersection_functions)):
                # this if-else-statement controls which direction
                # the points are being added in
                # when i % 2 == 0: they are added from direction1 to direction2
                # else: they are being added from direction2 to direction1

                if i % 2 == 0:
                    x_intersection = \
                        s.find_x_intersection(s.path_functions[i], intersection_functions[j])
                    if s.local_c[original_indexes[j]][0] > s.local_c[(original_indexes[j] + 1) % 4][0]:
                        min_x = s.local_c[(original_indexes[j] + 1) % 4][0]
                        max_x = s.local_c[original_indexes[j]][0]
                    else:
                        min_x = s.local_c[original_indexes[j]][0]
                        max_x = s.local_c[(original_indexes[j] + 1) % 4][0]

                    if min_x <= x_intersection <= max_x:
                        y_intersection = intersection_functions[j][0] * x_intersection \
                                         + intersection_functions[j][1]
                        point_array.append([x_intersection, y_intersection])
                        s.set_plot(Plot([[x_intersection, y_intersection]], 0, 'b', False))
                else:
                    x_intersection = \
                        s.find_x_intersection(s.path_functions[i], intersection_functions[2-j])
                    if s.local_c[original_indexes[2-j]][0] > s.local_c[(original_indexes[2-j] + 1) % 4][0]:
                        min_x = s.local_c[(original_indexes[2-j] + 1) % 4][0]
                        max_x = s.local_c[original_indexes[2-j]][0]
                    else:
                        min_x = s.local_c[original_indexes[2-j]][0]
                        max_x = s.local_c[(original_indexes[2-j] + 1) % 4][0]

                    if min_x <= x_intersection <= max_x:
                        y_intersection = intersection_functions[2-j][0] * x_intersection \
                                         + intersection_functions[2-j][1]
                        point_array.append([x_intersection, y_intersection])
                        s.set_plot(Plot([[x_intersection, y_intersection]], 0, 'b', False))

    def run(s):
        # works
        intersection_functions, original_indexes = s.get_intersection_borders()

        s.get_path_limit_points(intersection_functions, original_indexes)
