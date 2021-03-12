import numpy as num
from linearFunction import LinearFunction
from math import sin, cos, sqrt, atan2, radians

low_left = num.array([57.028481188091455, 9.948913866684594])
low_right = num.array([57.028678655922064, 9.949934871541862])
up_left = num.array([57.02879055029732, 9.948587540647853])
up_right = num.array([57.02895776307729, 9.949560854500227])

big_array = num.array([[57.028481188091455, 9.948913866684594],
                      [57.028678655922064, 9.949934871541862],
                      [57.02879055029732, 9.948587540647853],
                      [57.02895776307729, 9.949560854500227]])



# low_left = num.array([9.948913866684594, 57.028481188091455])
# low_right = num.array([9.949934871541862, 57.028678655922064])
# up_left = num.array([9.948587540647853, 57.02879055029732])
# up_right = num.array([9.949560854500227, 57.02895776307729])

local_low_left = num.subtract(low_left, low_left)
local_low_right = num.subtract(low_right, low_left)
local_up_left = num.subtract(up_left, low_left)
local_up_right = num.subtract(up_right, low_left)

# def LonLadToLocalSystem(lll, llr, lul, lur):


# print(local_up_left, "    ", local_up_right, "\n        ", local_low_left, "             ", local_low_right)

######################## los testos ##########################

obj = LinearFunction(local_low_left, local_up_left)
print(obj.calculate_intersection())
