import numpy as np
from matplotlib import pyplot as plt


def plot_points(local_c):
    x = []
    y = []
    #print(len(local_c))
    for i in range(len(local_c)):
        x.append(local_c[i][0]) # = [local_c[0][0], local_c[1][0], local_c[2][0], local_c[3][0]]
        y.append(local_c[i][1]) # = [local_c[0][1], local_c[1][1], local_c[2][1], local_c[3][1]]

    plt.plot(x, y, 'o')  # latitude = y, longitude = x*


plot_function_run_counter = 0


def plot_functions(funcs, color):
    global plot_function_run_counter
    x_func = np.linspace(-5, 5, 2)
    plt.title('Search Area')

    if not isinstance(funcs[0], np.float64):
        for i in range(len(funcs)):
            y = (funcs[i][0] * x_func) + funcs[i][1]
            plt.plot(x_func, y, color)
        plot_function_run_counter = plot_function_run_counter + 1
    else:
        y = (funcs[0] * x_func) + funcs[1]
        plt.plot(x_func, y, color)
        plot_function_run_counter = plot_function_run_counter + 1


def find_limits(points, pad):
    x1, x2, y1, y2 = 0, 0, 0, 0
    padding = pad
    for i in range(len(points)):
        if i == 0:
            print(type(float(points[0][0])))
            print(points[0][1])
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

    # to make the coordinate system fixed
    #if (x1 - x2) < (y1 - y2):
     #   difference = abs((y1 - y2) - (x1 - x2))
      #  x1 = x1 + (difference / 2)
       # x2 = x2 - (difference / 2)
    #else:
#        difference = abs((x1 - x2) - (y1 - y2))
#        y1 = y1 + (difference / 2)
#        y2 = y2 - (difference / 2)


    return x1, x2, y1, y2


def show_plots(plots_list, padding):
    x_limit_1, x_limit_2, y_limit_1, y_limit_2 = 0, 0, 0, 0
    for i in range(len(plots_list)):
        if type(plots_list[i].local_c) != int:
            plot_points(plots_list[i].local_c)
            x_limit_1, x_limit_2, y_limit_1, y_limit_2 = find_limits(plots_list[i].local_c, padding)
        if type(plots_list[i].functions) != int:
            plot_functions(plots_list[i].functions, plots_list[i].color)

    plt.xlim([x_limit_1, x_limit_2])
    plt.ylim([y_limit_1, y_limit_2])

    plt.grid()
    plt.show()


class Plot:
    local_c = None
    functions = None

    def __init__(self, local_c, funcs, color):
        self.local_c = local_c
        self.functions = funcs
        self.color = color
