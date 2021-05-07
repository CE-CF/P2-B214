import numpy as np
import time

from routing import Routing
from routingpackage.distanceinmeters import DistanceInMeters
from routingpackage.dronecommands import instantiate, the_thread

big_array = np.array([[57.02848118809145, 9.948913866684594],
                      [57.02867865592206, 9.949934871541862],
                      [57.02895776307729, 9.949560854500227],
                      [57.02879055029732, 9.948587540647853]])

thick_arr = np.array([[57.061873611380946, 9.874398700298244],
                      [57.05405179873142, 9.840836323673754],
                      [57.07404859674405, 9.837558984710995],
                      [57.07226714106329, 9.859468601277795]])


def run():
    sohn = Routing(big_array, 0.00002)
    sohn.get_local_coordinates()
    sohn.analyze_coordinates()
    bob = DistanceInMeters
    bob.reverse_calculate(20)

    instantiate()
    the_thread("takeoff")
    print("drone has taken off")
    time.sleep(2)
    the_thread("rc 0 0 0 100")
    print("rc +100")
    time.sleep(2)
    the_thread("rc 0 0 0 -100")
    print("rc -100")
    time.sleep(2)
    the_thread("rc 0 0 0 0")
    print("rc 0")
    time.sleep(5)
    the_thread("land")
    print("TOUCHDOWN!!!")



if __name__ == '__main__':
    run()