import numpy as num


class GlobalToLocalPoints:
    # Longitude = x and latitude = y

    point_array = num.empty((4, 2), float)

    # Constructor
    def __init__(self, p_arr):
        self.point_array = p_arr

        """ 
        Choose the local origo (0,0) as the point with the 
        lowest value in the second coordinate (longitude).
        If two points have the same longitude, 
        the one with the lowest latitude gets chosen 
        """

    def find_origo(self):
        """
        the points' coordinates are compared to
        find the lowest longitude value to use this
        point as origo in the local coordinate scheme

        if-statement:
        the array index value of the point with the
        lowest longitude gets saved after each check

        for-loop:
        and when all the points' coordinates has been
        compared then it will return the index value
        of the one


        the lowest latitude that gets saved
        returns the index value of the origo point

        if the two points has the same longitude
        then it's the index value of the point with
        """
        
        temp_origo = 0
        for i in range(1, 4):
            if self.point_array[temp_origo][1] <= self.point_array[i][1]:
                continue
            elif self.point_array[temp_origo][1] > self.point_array[i][1]:
                temp_origo = i
            else:
                if self.point_array[temp_origo][0] <= self.point_array[i][0]:
                    continue
                else:
                    temp_origo = i
        return temp_origo

    def calculate_local_points(self):
        origo = self.find_origo()
        local_point_array = num.empty((0, 2), float)

        num.set_printoptions(precision=None, threshold=None,                    # supresses the scientific notation when showing floating numbers
                             edgeitems=None, linewidth=None,
                             suppress=True, nanstr=None,
                             infstr=None, formatter=None,
                             sign=None, floatmode=None, legacy=None)

        # Subtract origos global coordinate from all 4 points including itself
        # This will retrieve the local coordinates in relation to 
        for i in range(4):
            local_point = (num.subtract(self.point_array[i], self.point_array[origo]))
            local_point_array = num.insert(local_point_array, i, local_point, axis=0)

        return local_point_array
