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

round_array = np.array([[57.03992190045029, 9.94593276958847],
                        [57.03492190045028, 9.95593276958846],
                        [57.04992190045027, 9.95493276958845],
                        [57.04992190045026, 9.94593276958844]])

round_arr_2 = np.array([[57.03992190045029, 9.94593276958847],
                        [57.03982190045028, 9.95593276958846],
                        [57.04992190045027, 9.95573276958845],
                        [57.04992190045026, 9.94593276958844]])

round_arr_3 = np.array([[57.03992190045029, 9.94593276958847],  # works - positive very steep slope
                        [57.04092190045028, 9.95593276958846],
                        [57.04992190045027, 9.95493276958845],
                        [57.04992190045026, 9.94593276958844]])

round_arr_4 = np.array([[57.03992190045029, 9.94593276958847],  # doesn't work - negative very steep slope
                        [57.03892190045028, 9.95593276958846],
                        [57.04992190045027, 9.95493276958845],
                        [57.04992190045026, 9.94593276958844]])

round_arr_5 = np.array([[57.04442190045029, 9.95493276958847],
                        [57.04392190045028, 9.96483276958846],
                        [57.04892190045028, 9.96493276958846],
                        [57.05892190045026, 9.95493276958844]])

round_arr_6 = np.array([[57.03992190045029, 9.94593276958847],
                        [57.04182190045028, 9.96593276958846],
                        [57.04992190045027, 9.96573276958845],
                        [57.04992190045026, 9.94593276958844]])

round_arr_7 = np.array([[57.04469923110424, 9.941350604764456],  # approx 45 degrees
                        [57.04431983058689, 9.942146254577343],
                        [57.04332179604662, 9.941749287658181],
                        [57.04343269009751, 9.940075589296312]])

round_arr_8 = np.array([[57.04469923110424, 9.941158604764456],
                        [57.04431983058689, 9.942146254577343],
                        [57.04332179604662, 9.941749287658181],
                        [57.04343269009751, 9.940075589296312]])

round_arr_9 = np.array([[57.04469923110424, 9.940858604764456],
                        [57.04431983058689, 9.942146254577343],
                        [57.04332179604662, 9.941749287658181],
                        [57.04343269009751, 9.940075589296312]])

big_relay_box = [57.028239241386345, 9.949700557143565]

odin_relay_box = [57.03967438804014, 9.9472223949503]

deg_5 = np.array([[57.04469923110424, 9.94018639764456],  # approx 5 degrees
                  [57.04431983058689, 9.942146254577343],
                  [57.04332179604662, 9.941749287658181],
                  [57.04343269009751, 9.940075589296312]])

deg_10 = np.array([[57.04469923110424, 9.94029904764456],  # approx 10 degrees
                  [57.04431983058689, 9.942146254577343],
                  [57.04332179604662, 9.941749287658181],
                  [57.04343269009751, 9.940075589296312]])

deg_15 = np.array([[57.04469923110424, 9.94041504764456],  # approx 15 degrees
                   [57.04431983058689, 9.942146254577343],
                   [57.04332179604662, 9.941749287658181],
                   [57.04343269009751, 9.940075589296312]])

deg_20 = np.array([[57.04469923110424, 9.94053674764456],  # approx 20 degrees
                   [57.04431983058689, 9.942146254577343],
                   [57.04332179604662, 9.941749287658181],
                   [57.04343269009751, 9.940075589296312]])

deg_25 = np.array([[57.04469923110424, 9.94066644764456],  # approx 25 degrees
                   [57.04431983058689, 9.942146254577343],
                   [57.04332179604662, 9.941749287658181],
                   [57.04343269009751, 9.940075589296312]])

deg_30 = np.array([[57.04469923110424, 9.940806904764456],  # approx 30 degrees
                   [57.04431983058689, 9.942146254577343],
                   [57.04332179604662, 9.941749287658181],
                   [57.04343269009751, 9.940075589296312]])

deg_35 = np.array([[57.04469923110424, 9.940963004764456],  # approx 35 degrees
                   [57.04431983058689, 9.942146254577343],
                   [57.04332179604662, 9.941749287658181],
                   [57.04343269009751, 9.940075589296312]])

deg_40 = np.array([[57.04469923110424, 9.941141004764456],  # approx 40 degrees
                   [57.04431983058689, 9.942146254577343],
                   [57.04332179604662, 9.941749287658181],
                   [57.04343269009751, 9.940075589296312]])

deg_45 = np.array([[57.04469923110424, 9.941350604764456],  # approx 45 degrees
                   [57.04431983058689, 9.942146254577343],
                   [57.04332179604662, 9.941749287658181],
                   [57.04343269009751, 9.940075589296312]])

deg_55 = np.array([[57.04469923110424, 9.941883004764456],  # approx 55 degrees
                   [57.04431983058689, 9.942146254577343],
                   [57.04332179604662, 9.941749287658181],
                   [57.04343269009751, 9.940075589296312]])

deg_65 = np.array([[57.04432641010424, 9.941992504764456],  # approx 65 degrees
                   [57.04381983058689, 9.942146254577343],
                   [57.04332179604662, 9.941749287658181],
                   [57.04343269009751, 9.940075589296312]])

deg_75 = np.array([[57.04394621010424, 9.941992504764456],  # approx 75 degrees
                   [57.04361983058689, 9.942146254577343],
                   [57.04332179604662, 9.941749287658181],
                   [57.04343269009751, 9.940075589296312]])

deg_85 = np.array([[57.0436002010424, 9.941992504764456],  # approx 85 degrees
                   [57.04351983058689, 9.942146254577343],
                   [57.04332179604662, 9.941749287658181],
                   [57.04343269009751, 9.940075589296312]])

soccer_arr = np.array([[57.01790968504875, 9.952207436114897],
                       [57.01814477939277, 9.952435387608425],
                       [57.01804259003947, 9.952628518877036],
                       [57.017833800022906, 9.952494389395032]])

soccer_rb = [57.01786594422335, 9.952036864294133]
#soccer_rb = [57.01773774865883, 9.952373791864979]


def run():
    # Routing(  2D-array of global coordinates specifying the corners of the map,
    #           plot padding,
    #           user defined path width in meters - used for testing
    #               - leave the value 0 and it's calculated using the drone FOV specified)
    sohn = Routing(soccer_arr, 0.00002, 3)
    sohn.get_local_coordinates()
    sohn.analyze_coordinates()

    # get_to_route( path limit points,
    #               origo global coordinates,
    #               relay box coordinates,
    #               path functions,
    #               drone speed (m/s) - default value 1 if 0 is passed as a parameter )

    get_to_route(sohn.get_path_limit_points(),
                 sohn.get_origo(),
                 soccer_rb,
                 sohn.get_path_functions(),
                 1)

    # search_route( path width (meters) - if default pass obj.get_path_width as parameter,
    #               path limit points
    #               origo global points
    #               path functions

    search_route(3,
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
