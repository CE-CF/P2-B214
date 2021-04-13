import numpy as num

from distanceInMeters import DistanceInMeters
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
# Longitude = x og latitude = y
# Koordinaterne er skrevet som [y,x]
A = low_left = num.array([57.028481188091455, 9.948913866684594])
B = low_right = num.array([57.028678655922064, 9.949934871541862])
C = up_right = num.array([57.02895776307729, 9.949560854500227])
D = up_left = num.array([57.02879055029732, 9.948587540647853])

big_array = num.array([[57.02848118809145, 9.948913866684594],
                       [57.02867865592206, 9.949934871541862],
                       [57.02895776307729, 9.949560854500227],
                       [57.02879055029732, 9.948587540647853]])

######################## los testos ##########################

objLocalPoints = GlobalToLocalPoints(big_array)
local_points_arr = objLocalPoints.calculate_local_points()

func1 = LinearFunction(local_points_arr[0], local_points_arr[1])
func2 = LinearFunction(local_points_arr[1], local_points_arr[2])
func3 = LinearFunction(local_points_arr[2], local_points_arr[3])
func4 = LinearFunction(local_points_arr[3], local_points_arr[0])

'''
This is what the quadrilateral is going to look like. It does
not have to be square, but it has to be A, B, C and D in this order.
  B ------------------- C
   |                   |
   |                   |
   |                   |
   |                   |
   |                   |
  A ------------------- D

'''

print("f(x)=" + str(round(func1.calculate_slope(), 2)) + "x+" + str(
    round(func1.calculate_intersection(big_array[objLocalPoints.find_origo()]), 10)))
print("f(x)=" + str(round(func2.calculate_slope(), 2)) + "x+" + str(
    round(func2.calculate_intersection(big_array[objLocalPoints.find_origo()]), 10)))
print("f(x)=" + str(round(func3.calculate_slope(), 2)) + "x+" + str(
    round(func3.calculate_intersection(big_array[objLocalPoints.find_origo()]), 10)))
print("f(x)=" + str(round(func4.calculate_slope(), 2)) + "x+" + str(
    round(func4.calculate_intersection(big_array[objLocalPoints.find_origo()]), 10)))

# The distance between each corner is being calculated.
dist = DistanceInMeters()
AD = dist.calculate_distance(low_left, low_right)
AB = dist.calculate_distance(low_left, up_left)
CD = dist.calculate_distance(low_right, up_right)
BC = dist.calculate_distance(up_left, up_right)
# The different distances are being sorted to find the longest
distList = [AD, AB, CD, BC]
distList.sort()
print("The longest side is: ", distList[-1], "m")
# Which is the longest?
if (distList.index(AD) == 3):
    print("AD is the longest")
elif (distList.index(AB) == 3):
    print("AB is the longest")
elif (distList.index(CD) == 3):
    print("CD is the longest")
else:
    print("BC is the longest")
