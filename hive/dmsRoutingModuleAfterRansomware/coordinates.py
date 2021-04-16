import numpy as np


class Coordinates:
    global_c = np.empty((2, 4), float)
    local_c = np.empty((0, 2), float)

    def __init__(self, coordinates):
        self.global_c = np.array([[coordinates[0][1], coordinates[0][0]],
                                  [coordinates[1][1], coordinates[1][0]],
                                  [coordinates[2][1], coordinates[2][0]],
                                  [coordinates[3][1], coordinates[3][0]]])

    def find_origo(self):
        temp_origo = 0
        for i in range(1, 4):
            if self.global_c[temp_origo][0] <= self.global_c[i][0]:
                continue
            elif self.global_c[temp_origo][0] > self.global_c[i][0]:
                temp_origo = i
            else:
                if self.global_c[temp_origo][1] <= self.global_c[i][1]:
                    continue
                else:
                    temp_origo = i
        return temp_origo

    def get_local_coordinates(self):
        origo = self.find_origo()

        np.set_printoptions(precision=None, threshold=None,
                            # supresses the scientific notation when showing floating numbers
                            edgeitems=None, linewidth=None,
                            suppress=True, nanstr=None,
                            infstr=None, formatter=None,
                            sign=None, floatmode=None, legacy=None)

        # Subtract origos global coordinate from all 4 points including itself
        # This will retrieve the local coordinates in relation to
        for i in range(4):
            single_local_c = (np.subtract(self.global_c[i], self.global_c[origo]))
            self.local_c = np.insert(self.local_c, i, single_local_c, axis=0)
        return self.local_c