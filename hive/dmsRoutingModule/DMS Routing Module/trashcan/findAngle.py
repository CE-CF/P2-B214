import numpy as num
import math


class FindAngle:
    # angle_1 = 0
    # angle_2 = 0

    def __init__(self, a1, a2):
        self.angle_1 = a1
        self.angle_2 = a2

    def find_angle(self):
        radians = math.atan(self.angle_1) - math.atan(self.angle_2)
        return math.degrees(radians)
