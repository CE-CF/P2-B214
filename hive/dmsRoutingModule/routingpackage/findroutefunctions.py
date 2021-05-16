import math
from plots import Plot
from .distanceinmeters import DistanceInMeters
from sympy import *
import numpy as np

perp = []
drone_FOV = float(26)


def find_longest_line(global_c):
    # This function checks the length of each side and returns the index of the point combination which together span
    # the longest line. The index values here relates to the order of the functions array

    global_c_correct_order = [[global_c[0][1], global_c[0][0]],
                              [global_c[1][1], global_c[1][0]],
                              [global_c[2][1], global_c[2][0]],
                              [global_c[3][1], global_c[3][0]]]

    longest_line = 0
    longest_line_index = 0
    for i in range(len(global_c_correct_order)):
        adj_i = (i + 1) % 4
        length = DistanceInMeters.calculate_distance(global_c_correct_order[i], global_c_correct_order[adj_i])
        # print(str(length) + "   " + str(global_c_correct_order[i]) + " , " + str(global_c_correct_order[adj_i]))
        if length > longest_line:
            longest_line = length
            longest_line_index = i
    return longest_line_index


# when a plot is created it's put as a parameter to this function
# it then appends this plot to the array perp (for perpendicular)
def set_plot(p):
    global perp
    perp.append(p)


# the Routing-class uses this function to get the saved Plot-objects from the perp-array
def get_plots():
    return perp


def point_furthest_away(local_c, func, index, origo_c):
    # this function finds the point that is the furthest away from the longest line
    # first we find the perpendicular function to the longest lines function
    # next we setup: y=ax+b  -->  b=y-ax
    # which makes us capable of putting in the x and y coordinates of a point and
    # find the intersection with the y-axis for the perpendicular function from that
    # # Afterwards we can now find the distance using our calculate_distance method
    # we return the index and length from the function of the point furthest from the function

    global perp
    perp_func_slope = 0
    longest_dist = 0
    longest_dist_index = 0
    second_longest_dist = 0
    second_longest_dist_index = 0  # index of second and last point that is not on the longest line

    origo_c_correct_order = [origo_c[1], origo_c[0]]

    local_c_correct_order = [[local_c[0][1], local_c[0][0]],
                             [local_c[1][1], local_c[1][0]],
                             [local_c[2][1], local_c[2][0]],
                             [local_c[3][1], local_c[3][0]]]

    for fs in range(2):  # to get both longest and second longest we loop twice - fs does nothing
        for i in range(len(local_c)):
            # Find the perpendicular function to the function of the longest line
            # and find it's intersection with the axis
            perp_func_slope = 1 / -func[index][0]
            perp_intersection = local_c[i][1] - (perp_func_slope * local_c[i][0])

            # Find the x-coordinate, where the original and perp function intersect
            x = Symbol('x')
            solution = (solve(perp_func_slope * x + perp_intersection - func[index][0] * x - func[index][1], x))
            intersect_x = float(solution[0])

            # Find the y-coordinate of that point
            y_of_intersect_x = perp_func_slope * intersect_x + perp_intersection

            # The calculate_distance-method only takes global coordinates
            # so we add the global coordinates of origo to both our sets
            # global_intersect_c = origo_c + [intersect_x, y_of_intersect_x]
            # global_local_c = origo_c + local_c[i]

            # global_intersect_c = origo_c_correct_order + [intersect_x, y_of_intersect_x]
            # global_local_c = origo_c_correct_order + local_c_correct_order[i]

            global_intersect_c = [origo_c_correct_order[0] + y_of_intersect_x, origo_c_correct_order[1] + intersect_x]
            global_local_c = [origo_c_correct_order[0] + local_c_correct_order[i][0],
                              origo_c_correct_order[1] + local_c_correct_order[i][1]]

            # print(global_local_c, global_intersect_c)
            dist = DistanceInMeters.calculate_distance(global_local_c, global_intersect_c)

            # Finding ratio between y-axis intersections in coordinates and meters

            set_plot(Plot(0, [perp_func_slope, perp_intersection], 'b', False))

            # find the longest projection of one of the points to the longest line and the points index
            if dist >= longest_dist:
                longest_dist = dist
                longest_dist_index = i
            elif dist >= second_longest_dist:
                second_longest_dist = dist
                second_longest_dist_index = i

    print("longest line : " + str(longest_dist_index))
    print("longest_dist : " + str(longest_dist))
    print("second longest line : " + str(second_longest_dist_index))
    print("second_longest_dist : " + str(second_longest_dist))
    return longest_dist_index, second_longest_dist_index, longest_dist, perp_func_slope


def find_path_width(longest_dist, ud_path_width):  # user defined path width
    float_number_of_paths = 0
    number_of_paths = 0
    path_width = 0

    if ud_path_width == 0:
        float_number_of_paths = longest_dist / drone_FOV
        number_of_paths = math.ceil(float_number_of_paths)
        path_width = longest_dist / number_of_paths
    else:
        float_number_of_paths = longest_dist / ud_path_width
        number_of_paths = math.ceil(float_number_of_paths)
        path_width = longest_dist / number_of_paths

    return path_width, number_of_paths


def ph():
    pass


# the path_width (found previously) isn't enough for us to calculate the path functions
# it only tells us the distance between the two functions, not the vertical distance (y-axis intersection differences)
# so. we need the new y-axis intersections
# we can find these using this formula where the variable slope = slope of function of the longest border/line/edge:
# EQUATION #        intersection = path_width / sin(90 - atan(slope))
#
# using this formula we find the hypotenuse of a right triangle where the opposite side to the angle is
# our distance path_width
# the hypotenuse is always parallel to the y-axis cuz we wanna find the different function-intersections
# the angle is found by first using atan on the longest-border-function to find it's angle to the x-axis
# afterwards subtracting this from 90 degrees since the hypotenuse was vertical
def find_intersection_corresponding_path_width(path_width, paths, func, x_ratio, y_ratio,
                                               local_c, perp_func_slope, p_not_on_line):
    arr = []
    pon = 0

    if -1 > perp_func_slope > 1:
        pon = math.sqrt(((x_ratio / perp_func_slope) ** 2) + (y_ratio ** 2))
    else:
        pon = math.sqrt((x_ratio ** 2) + ((perp_func_slope * y_ratio) ** 2))

    angle = abs(math.degrees(atan2(perp_func_slope, 1)))
    print("angle " + str(angle))
    print("slope " + str(perp_func_slope))

    # print('{0:f}'.format(pon * path_width))

    semicircle = math.pi / 180
    #print('pi     ' + str(semicircle * angle))

    scaler = (angle / 90)

    pon2 = ((cos(angle) * x_ratio) + (sin(angle) * y_ratio))
    pon3 = (math.cos(semicircle * angle) * x_ratio) + (math.sin(semicircle * angle) * y_ratio)
    pon4 = ((1 - scaler) * x_ratio) + (scaler * y_ratio)
    print('pon  ' + '{0:f}'.format(pon))
    print('pon2 ' + '{0:f}'.format(pon2))

    print("scaler " + str(scaler))
    # print('{0:f}'.format(pon4, '.8f'))

    # print('{0:f}'.format(x_ratio))
    # print('{0:f}'.format(y_ratio))

    path_border_intersection = (path_width * 0.0000093) / (math.sin(math.radians(90 - math.degrees(math.atan(func[0])))))

    # in which direction should the parallel paths be generated? this code solves this problem
    # pseudo code of this -> picture on my phone 15/5-2021
    for i in range(2):  # loops through the two points that is not on the line and
        # y-coordinate intersection of the point's vertical projection onto the longest line
        y_coord_proj_of_point_on_func = func[0] * local_c[p_not_on_line[i]][0] + func[1]
        # print(func[0], local_c[p_not_on_line[i]][0], func[1])
        # print(str(y_coord_proj_of_point_on_func) + " < " + str(local_c[p_not_on_line[i]][1]))

        # if point is above function line
        if y_coord_proj_of_point_on_func < local_c[p_not_on_line[i]][1]:
            # print("point is above:   +intersection")
            path_border_intersection = abs(path_border_intersection)
        else:  # if not the point is below the function line
            # print("point is below:   -intersection")
            path_border_intersection = abs(path_border_intersection) * (-1)

    path_intersection = path_border_intersection / 2
    for i in range(paths):
        arr.append((path_border_intersection * i) + path_intersection + func[1])
    return arr


# just putting slope and intersection together in 2D-array
def complete_path_functions(path_intersections_arr, longest_line):
    arr = []
    for i in range(len(path_intersections_arr)):
        arr.append([longest_line[0], path_intersections_arr[i]])
        set_plot(Plot(0, arr[i], 'g', False))
    return arr


def run(global_c, local_c, func, origo_c, x_ratio, y_ratio, ud_path_width):
    # Find longest line - returns index of the function in the array
    longest_line_index = find_longest_line(global_c)

    # Find point furthest away - returns points index in array and shortest distance from point to function
    longest_dist_index, second_longest_dist_index, longest_dist, perp_func_slope = \
        point_furthest_away(local_c, func, longest_line_index, origo_c)

    # Find width of path - returns width of the path and the total number of paths
    path_width, number_of_paths = find_path_width(longest_dist, ud_path_width)

    # Find the path functions intersection with the y-axis - returns array of intersections
    path_intersection_arr \
        = find_intersection_corresponding_path_width(path_width, number_of_paths, func[longest_line_index],
                                                     x_ratio, y_ratio, local_c, perp_func_slope,
                                                     [longest_dist_index, second_longest_dist_index])

    # Put together the functions - returns an array of all the path functions
    path_functions_arr = complete_path_functions(path_intersection_arr, func[longest_line_index])

    return path_functions_arr, longest_line_index, path_width

    # in the end return the drone fov(meters)
