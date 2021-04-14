import numpy as np
from matplotlib import pyplot as plt


def plot_points(local_c):
    x = [local_c[0][0], local_c[1][0], local_c[2][0], local_c[3][0]]
    y = [local_c[0][1], local_c[1][1], local_c[2][1], local_c[3][1]]

    plt.plot(y, x, 'o')  # latitude = y, longitude = x


def plot_functions(funcs):
    x_func = np.linspace(-.001, .001, 2)

    y1 = (funcs[0][0] * x_func) + funcs[0][1]
    y2 = (funcs[1][0] * x_func) + funcs[1][1]
    y3 = (funcs[2][0] * x_func) + funcs[2][1]
    y4 = (funcs[3][0] * x_func) + funcs[3][1]

    plt.plot(y1, x_func, 'r')
    plt.plot(y2, x_func, 'r')
    plt.plot(y3, x_func, 'r')
    plt.plot(y4, x_func, 'r')

    plt.title('Headline')
    plt.grid()


def plot(local_c, funcs):
    plot_points(local_c)
    plot_functions(funcs)

    plt.xlim([-.0001, .0015])
    plt.ylim([-.00051, .0004])
    plt.show()
