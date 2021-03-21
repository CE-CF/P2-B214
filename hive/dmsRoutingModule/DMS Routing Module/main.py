import numpy as num
from linearFunction import LinearFunction
from globalToLocalPoints import GlobalToLocalPoints
from trashcan.findAngle import FindAngle
from plot import Plot
'''
Vi forventer at modtage fire globale koordinater fra GUI,
som er plottet ind af brugeren i rækkefølge (1,2,3,4) eller (A,B,C,D).
Det er underordnet om rækkefølgen er
med eller mod urets retning, så længe de er i rækkefølge.
'''
# A = low_left = num.array([57.028481188091455, 9.948913866684594])
# B = low_right = num.array([57.028678655922064, 9.949934871541862])
# C = up_right = num.array([57.02895776307729, 9.949560854500227])
# D = up_left = num.array([57.02879055029732, 9.948587540647853])

big_array = num.array([[57.02848118809145, 9.948913866684594],
                       [57.02867865592206, 9.949934871541862],
                       [57.02895776307729, 9.949560854500227],
                       [57.02879055029732, 9.948587540647853]])

######################## los testos ##########################

objLocalPoints = GlobalToLocalPoints(big_array)
local_points_arr = objLocalPoints.calculate_local_points()

obj = LinearFunction(local_points_arr[0], local_points_arr[1])
obj1 = LinearFunction(local_points_arr[0], local_points_arr[2])
obj2 = LinearFunction(local_points_arr[0], local_points_arr[3])
# print(obj.calculate_slope())
# print(obj1.calculate_slope())
# print(obj2.calculate_slope())

angle01 = FindAngle(obj.calculate_slope(), obj1.calculate_slope())

# bob = DistanceInMeters(low_left, low_right)
# bob.calculate_distance()
