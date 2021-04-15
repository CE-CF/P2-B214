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
import numpy as np

perp = None


def find_longest_line(local_c):
    # This function checks the length of each side and returns the index of the point combination which together span
    # the longest line. The index values here relates to the order of the functions array

    longest_line = 0
    longest_line_index = 0
    for i in range(len(local_c)):
        adj_i = (i + 1) % 4
        x1 = local_c[i][0]
        y1 = local_c[i][1]
        x2 = local_c[adj_i][0]
        y2 = local_c[adj_i][1]
        z = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        if z > longest_line:
            longest_line = z
            longest_line_index = i

    print("Line number " + str(longest_line_index + 1) + " index " + str(longest_line_index) + " was the longest")
    return longest_line_index


def setPlot(p):
    global perp
    perp = p


def getPlot():
    return perp


def point_furthest_away(local_c, func, index):
    # this function find the point that is the furthest away from the longest line
    # first we find the perpendicular function to the longest lines function
    # next we setup: y=ax+b  -->  b=y-ax
    # which makes us capable of putting in the x and y coordinates of a point and
    # find the intersection with the y-axis for the perpendicular function from that
    # # Afterwards we can now do the following distance calculation:
    # dist = sqrt((0 - point_x)^2 + (b - point_y)^2)
    # we return the index and length from the function of the point furthest from the function

    global perp
    longest_dist = 0
    longest_dist_index = 0

    for i in range(len(local_c)):
        perp_func_slope = 1 / -func[index][0]
        print(func[index])
        b_intersection = local_c[i][0] - (perp_func_slope * local_c[i][1])
        dist = math.sqrt((0 - local_c[i][1])**2 + (b_intersection - local_c[i][0])**2)
        setPlot(Plot(0, [[perp_func_slope, b_intersection]]))

        if dist > longest_dist:
            longest_dist_index = i

    return [longest_dist_index, longest_dist]


def run(local_c, func):
    longest_line_index = find_longest_line(local_c)                 # this one works now
    [longest_dist_index, longest_dist] = point_furthest_away(local_c, func, longest_line_index)
    