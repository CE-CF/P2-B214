import numpy as np
import coordinates as co
from routing import Routing

big_array = np.array([[57.02848118809145, 9.948913866684594],
                      [57.02867865592206, 9.949934871541862],
                      [57.02895776307729, 9.949560854500227],
                      [57.02879055029732, 9.948587540647853]])


def run():
    sohn = Routing(big_array)
    sohn.get_local_coordinates()
    sohn.analyze_coordinates()


if __name__ == '__main__':
    run()
