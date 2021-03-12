import numpy as num


class GlobalToLocalPoints:
    point_array = num.empty((4, 2), float)

    # Constructor
    def __init__(self, p_arr):
        self.point_array = p_arr

    ''' Choose the local origo (0,0) as the point with the 
        lowest value in the second coordinate (longitude).
        If two points have the same longitude, 
        the one with the lowest latitude gets chosen'''

    # Longitude = x and latitude = y
    def find_origo(self):
        temp_origo = 0
        for i in range(1, 4):
            if self.point_array[temp_origo][1] < self.point_array[i][1]:
                continue
            elif self.point_array[temp_origo][1] > self.point_array[i][1]:
                temp_origo = i
            else:
                if self.point_array[temp_origo][0] <= self.point_array[i][0]:
                    continue
                else:
                    temp_origo = i
