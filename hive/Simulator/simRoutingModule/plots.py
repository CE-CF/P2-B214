import numpy as np
from matplotlib import pyplot as plt


x_limit_1, x_limit_2, y_limit_1, y_limit_2 = 0, 0, 0, 0


# this is how we ensure that our plot of the area fills as much of the plot as possible
# right now though, it doesn't care about fixed axes - might implement that later for more "realistic view"
# this is also where the padding that is set through the Routing-class comes to play
    # it moves the points some chosen distance away from the edge of the plot
def find_limits(points, pad):
    x1, x2, y1, y2 = 0, 0, 0, 0
    padding = pad
    for i in range(len(points)):
        if i == 0:
            x1 = points[0][0] - padding
            x2 = points[0][0] + padding
            y1 = points[0][1] - padding
            y2 = points[0][1] + padding
        else:
            if points[i][0] < x1:
                x1 = points[i][0] - padding
            if points[i][0] > x2:
                x2 = points[i][0] + padding
            if points[i][1] < y1:
                y1 = points[i][1] - padding
            if points[i][1] > y2:
                y2 = points[i][1] + padding

# - - - to make the coordinate system fixed - - -
#
#    if (x1 - x2) < (y1 - y2):
#         difference = abs((y1 - y2) - (x1 - x2))
#         x1 = x1 + (difference / 2)
#         x2 = x2 - (difference / 2)
#    else:
#        difference = abs((x1 - x2) - (y1 - y2))
#        y1 = y1 + (difference / 2)
#        y2 = y2 - (difference / 2)

    return x1, x2, y1, y2


# plot() take the two arrays of coordinates and spits out a scatter plot
# 3rd parameter of plot() is shape of points
def plot_points(local_c, limits, padding):
    global x_limit_1, x_limit_2, y_limit_1, y_limit_2

    if limits:
        x_limit_1, x_limit_2, y_limit_1, y_limit_2 = find_limits(local_c, padding)

    x = []
    y = []

    for i in range(len(local_c)):
        x.append(local_c[i][0])
        y.append(local_c[i][1])
    plt.plot(x, y, 'o')


# some function-inputs come as single arrays of [slope, intersection]
# other function-inputs come as 2D-arrays of [[slope, intersection], [slope, intersection], ... , [slope, intersection]]
# to make sure both inputs work, we check whether the first index-value of the function-array is a float value or not
# if it's a float, it means that it's a single array, as first mentioned
    # it then proceeds to only look through first-dimensional index-values
# if it's not a float but a list or a numpy-array for instance then we need to look through 2D-values:
    # functions[i][j]
def plot_functions(funcs, color):
    x_func = np.linspace(-5, 5, 2)

    if not isinstance(funcs[0], np.float64):
        for i in range(len(funcs)):
            y = (funcs[i][0] * x_func) + funcs[i][1]
            plt.plot(x_func, y, color)
    else:
        y = (funcs[0] * x_func) + funcs[1]
        plt.plot(x_func, y, color)


# we loop through all the plots in the plots array/list and for each and one of them we check if the plot includes
# point coordinates and/or function(s) that needs to be plotted
# to make sure this works, when defining Plot-objects of either only function(s) or point(s) we need to put an
# integer(please put a 0) in the parameter-spot connected to either the functions or points. here's the parameters:
    # (local_c, funcs, color) - so if we want to only plot functions we do (0, funcs[], 'color')
def show_plots(plots_list, padding):
    for i in range(len(plots_list)):
        if type(plots_list[i].local_c) != int:
            plot_points(plots_list[i].local_c, plots_list[i].limits, padding)
        if type(plots_list[i].functions) != int:
            plot_functions(plots_list[i].functions, plots_list[i].color)

    plt.xlim([x_limit_1, x_limit_2])
    plt.ylim([y_limit_1, y_limit_2])
    plt.title('                                                  '  # <-- don't remove
              'Search Area        (be aware axes not fixed)')
    plt.grid()
    plt.show()


# the local_c can only be 2D-arrays of coordinates (otherwise plot don't work)
    # reminder to make plotting dynamic so it can also take one-dimensional inputs: [x, y]
# the functions-array can be 2D or one-dimensional
# the color-attribute defines the color of the functions...
    # needs to be a string to work. see table below.

#   character 	color
#      ‘b’ 	    blue
#      ‘g’ 	    green
#      ‘r’ 	    red
#      ‘c’ 	    cyan
#      ‘m’ 	    magenta
#      ‘y’ 	    yellow
#      ‘k’ 	    black
#      ‘w’ 	    white

class Plot:
    local_c = None
    functions = None
    color = None
    limits = False

    def __init__(self, local_c, funcs, color, lim):
        self.local_c = local_c
        self.functions = funcs
        self.color = color
        self.limits = lim
