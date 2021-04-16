# 1   - Find the longest line
# 2   - Find the length of the line that is the orthorgonal projection
#       of the point furthest away from the longest line
# 3   - Divide this length in meters with the drone FOV at a desired distance !!! (ex-FOV: 26m) !!!
# 3.1   - This will give us a number which we will round up to the nearest integer
# 3.2   - The number found in #2 divided by the number found in #3.1 is now gives us the width of the path that the
#         drone is going to cover
#       !                           IMPORTANT VARIABLE = path_width
# 3.3   - By dividing this number in two we get the perpendicular distance the drone exactly has to keep to
#         to the line it's flying parallel to
#           - The line referred to here is the line from #1
# 3.4   - We can now calculate the exact perpendicular distance from the drone to #1 through the calculation with the
#         knowledge that "path_no" is the number of the path which the drone is flying on. Here path 1 is closest to #1:
#       !                           IMPORTANT VARIABLE = dist
#       !                           dist =  (path_no - 1) * path_width + (path_width / 2)
# 3.5   -
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

    longest_line = 0
    longest_line_index = 0
    for i in range(len(global_c)):
        adj_i = (i + 1) % 4
        length = DistanceInMeters.calculate_distance(global_c[i], global_c[adj_i])
        if length > longest_line:
            longest_line = length
            longest_line_index = i

    print("Line number " + str(longest_line_index + 1) + " index " + str(longest_line_index) + " was the longest")
    return longest_line_index


def set_plot(p):
    global perp
    perp.append(p)


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
    longest_dist = 0
    longest_dist_index = 0

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
        global_intersect_c = origo_c + [intersect_x, y_of_intersect_x]
        global_local_c = origo_c + local_c[i]

        dist = DistanceInMeters.calculate_distance(global_local_c, global_intersect_c)

        # Finding ratio between y-axis intersections in coordinates and meters

        set_plot(Plot(0, [perp_func_slope, perp_intersection], 'b'))

        # find the longest projection of one of the points to the longest line and the points index
        if dist > longest_dist:
            longest_dist = dist
            longest_dist_index = i

    return longest_dist_index, longest_dist


def find_path_width(longest_dist):
    # path width
    float_number_of_paths = longest_dist / drone_FOV
    number_of_paths = math.ceil(float_number_of_paths)
    path_width = longest_dist / number_of_paths
    return path_width, number_of_paths


# The path width isn't enough for us to make the function
# We need the new y-axis intersections of the path functions
# We find this using sine, arctan, path_width and slope
def find_intersection_corresponding_path_width(path_width, paths, func, y_ratio):
    arr = []
    path_border_intersection = (path_width * y_ratio)/(math.sin(math.radians(90 - math.degrees(math.atan(func[0])))))
    # print((path_width * y_ratio) / math.degrees(math.sin(90 - math.degrees(math.atan(func[0])))))
    path_intersection = path_border_intersection / 2
    for i in range(paths):
        arr.append((path_border_intersection * i) + path_intersection + func[1])
    return arr


def complete_path_functions(path_intersections_arr, longest_line):
    arr = []
    for i in range(len(path_intersections_arr)):
        arr.append([longest_line[0], path_intersections_arr[i]])
        set_plot(Plot(0, arr[i], 'g'))
    return arr


def run(global_c, local_c, func, origo_c, y_ratio):
    # Find longest line - returns index of the function in the array
    longest_line_index = find_longest_line(global_c)

    # Find point furthest away - returns points index in array and shortest distance from point to function
    longest_dist_index, longest_dist = point_furthest_away(local_c, func, longest_line_index, origo_c)

    # Find width of path - returns width of the path and the total number of paths
    path_width, number_of_paths = find_path_width(longest_dist)

    # Find the path functions intersection with the y-axis - returns array of intersections
    path_intersection_arr \
        = find_intersection_corresponding_path_width(path_width, number_of_paths, func[longest_line_index], y_ratio)

    # Put together the functions - returns an array of all the path functions
    path_functions_arr = complete_path_functions(path_intersection_arr, func[longest_line_index])

    return path_functions_arr

    # in the end return the drone fov(meters)
