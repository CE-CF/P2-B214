import numpy as np
import time

from routing import Routing
from routingpackage.distanceinmeters import DistanceInMeters
from flightpackage.dronecommands import instantiate, the_thread, correct_yaw
from flightpackage.flymodes import get_to_route, search_route, go_home

big_array = np.array([[57.02848118809145, 9.948913866684594],
                      [57.02867865592206, 9.949934871541862],
                      [57.02895776307729, 9.949560854500227],
                      [57.02879055029732, 9.948587540647853]])

thick_arr = np.array([[57.061873611380946, 9.874398700298244],
                      [57.05405179873142, 9.840836323673754],
                      [57.07404859674405, 9.837558984710995],
                      [57.07226714106329, 9.859468601277795]])

odin_arr = np.array([[57.03971588980338, 9.947138200266934],
                    [57.03972749621221, 9.947269769279707],
                    [57.039808785497414, 9.947246843440466],
                    [57.039800183465196, 9.947113241135392]])

test_array = np.array([[57.02848118809145, 9.948913866684594],
                        [57.03848118809145, 9.948913866684594],
                        [57.03448118809145, 9.948913866684594],
                        [57.02848118809145, 9.948913866684594]])


big_relay_box = [57.028239241386345, 9.949700557143565]

odin_relay_box = [57.03967438804014, 9.9472223949503]


def run():
    # Routing(  2D-array of global coordinates specifying the corners of the map,
    #           plot padding,
    #           user defined path width in meters - used for testing
    #               - leave the value 0 and it's calculated using the drone FOV specified)
    sohn = Routing(odin_arr, 0.000002, 2)
    sohn.get_local_coordinates()
    sohn.analyze_coordinates()

    # get_to_route( path limit points,
    #               origo global coordinates,
    #               relay box coordinates,
    #               path functions,
    #               drone speed (m/s) - default value 1 if 0 is passed as a parameter )

    get_to_route(sohn.get_path_limit_points(),
                 sohn.get_origo(),
                 big_relay_box,
                 sohn.get_path_functions(),
                 1)

    # search_route( path width (meters) - pass obj.get_path_width as parameter,
    #               path limit points
    #               origo global points
    #               path functions

    search_route(5,
                 sohn.get_path_limit_points(),
                 sohn.get_origo(),
                 sohn.get_path_functions())

    # search_route(sohn.get_path_width(), sohn.get_path_limit_points(), sohn.get_origo(), sohn.get_path_functions())

    # instantiate()

    # print("go straight")

    # correct_yaw(8)

    # time.sleep(1)
    # the_thread("land")
    # print("TOUCHDOWN!!!")


if __name__ == '__main__':
    run()