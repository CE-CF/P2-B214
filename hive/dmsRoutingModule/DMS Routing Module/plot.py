import numpy as num
import matplotlib.pyplot as plt


class Plot:
    N = 50
    x = num.random.rand(N)
    y = num.random.rand(N)

    def run(self):
        plt.scatter(self.x, self.y)
        plt.show()
