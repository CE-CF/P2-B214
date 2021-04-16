import numpy as np

''' This class can calculate the slope between two local coordinates
    and find the intersection between this slope and the local y-axis '''

two_coordinates = np.empty((2, 2), float)


# This method calculates the difference between two coordinates
def calculate_difference():
    return np.array([two_coordinates[0][1] - two_coordinates[1][1],
                     two_coordinates[0][0] - two_coordinates[1][0]])


# This method calculates the slope between two points
def calculate_slope():
    return calculate_difference()[0] / calculate_difference()[1]


# This method calculates the intersection between the slope and the local y-axis
def calculate_intersection():
    return two_coordinates[0][1] - (calculate_slope() * two_coordinates[0][0])


def find_functions(local_c):
    global two_coordinates
    function_arr = [[0, 0], [0, 0], [0, 0], [0, 0]]
    for i in range(len(local_c)):
        two_coordinates = (local_c[i], local_c[(i + 1) % 4])
        temp_arr = [calculate_slope(), calculate_intersection()]
        function_arr[i] = temp_arr

    # Function of the x-axis
    return np.array([function_arr[0],
                     function_arr[1],
                     function_arr[2],
                     function_arr[3]])
