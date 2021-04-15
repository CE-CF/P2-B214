import numpy as np
from matplotlib import pyplot as plt


def plot_points(local_c):
    x = [local_c[0][0], local_c[1][0], local_c[2][0], local_c[3][0]]
    y = [local_c[0][1], local_c[1][1], local_c[2][1], local_c[3][1]]

    plt.plot(y, x, 'o')  # latitude = y, longitude = x*


def plot_functions(funcs):
    x_func = np.linspace(-.001, .001, 2)

    plt.title('Headline')

    for i in range(len(funcs)):
        y = (funcs[i][0] * x_func) + funcs[i][1]
        plt.plot(y, x_func, 'r')


def show_plots(plots_list):
    plot_points(plots_list[0].local_c)
    plot_functions(plots_list[0].functions)
    plot_functions(plots_list[1].functions)

    print(type(plots_list[0].local_c))      # WORKS
    print(type(plots_list[1].functions))    # WORKS

    plt.xlim([-.0001, .0015])
    plt.ylim([-.0006, .00055])
    plt.grid()
    plt.show()

#class Plots:
 #   obj_list = []


class Plot:
    local_c = None
    functions = None

    def __init__(self, local_c, funcs):
        self.local_c = local_c
        self.functions = funcs
