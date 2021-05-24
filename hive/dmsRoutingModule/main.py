import numpy as np
import time
from flightpackage.routefollower import get_to_next_point, go_back_to_start

from routing import Routing
from routingpackage.distanceinmeters import DistanceInMeters
from flightpackage.dronecommands import instantiate, the_thread, correct_yaw
from flightpackage.flymodes import get_to_route, search_route, go_home
from flightpackage.relayboxrouting import parser

# These two booleans should be changed when the user chooses either waypoint mode or search route mode on the GUI
waypoint_route = False
calculate_route = False


big_array = np.array([[57.02848118809145, 9.948913866684594],
                      [57.02867865592206, 9.949934871541862],
                      [57.02895776307729, 9.949560854500227],
                      [57.02879055029732, 9.948587540647853]])

thick_arr = np.array([[57.061873611380946, 9.874398700298244],
                      [57.05405179873142, 9.840836323673754],
                      [57.07404859674405, 9.837558984710995],
                      [57.07226714106329, 9.859468601277795]])

odin_arr = np.array([[57.03971214528992, 9.9471389504982],
                     [57.03978507672801, 9.9471133530025],
                     [57.03978728771742, 9.9472126415827],
                     [57.03972236108952, 9.9472286931091]])

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

odin_relay_box = [57.03970014484475, 9.947191148930434]
odin_relay_box_2 = [57.03974701430543, 9.947174416535168]

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


# soccer_rb = [57.01773774865883, 9.952373791864979]

waypoint_arr = np.array([[57.06593344368505, 9.935326097229042],
                         [57.066095679477336, 9.935056452101701],
                         [57.06629285188855, 9.935420028407108],
                         [57.06635455907872, 9.936038260803215]])


def run():
    custom_path_width = 2  # leave the value 0 and it's calculated using the drone FOV specified

    # Routing(  2D-array of global coordinates specifying the corners of the map,
    #           plot padding,
    #           user defined path width in meters - used for testing
    #               - leave the value 0 and it's calculated using the drone FOV specified)
    sohn = Routing(odin_arr, 0.00002, custom_path_width)
    sohn.get_local_coordinates()
    sohn.analyze_coordinates()

    # get_to_route( path limit points,
    #               origo global coordinates,
    #               relay box coordinates,
    #               path functions  )
    get_to_route(sohn.get_path_limit_points(),
                 sohn.get_origo(),
                 odin_relay_box,
                 sohn.get_path_functions())

    # search_route( path width (meters) - if default pass obj.get_path_width as parameter,
    #               path limit points,
    #               origo global points,
    #               path functions,
    #               drone speed (m/s) - default value 1 if 0 is passed as a parameter )
    search_route(custom_path_width,
                 sohn.get_path_limit_points(),
                 sohn.get_origo(),
                 sohn.get_path_functions(),
                 0)

    # print(cmd_string)

    cmd_string = go_home(sohn.get_path_limit_points(), odin_relay_box, sohn.get_origo())

    parser(cmd_string)
    
    #if waypoint_route:
    #    get_to_next_point(True, waypoint_arr)
    #    go_back_to_start(waypoint_arr)

    #elif calculate_route:
    #    custom_path_width = 0               # leave the value 0 and it's calculated using the drone FOV specified
    

if __name__ == '__main__':
    run()
