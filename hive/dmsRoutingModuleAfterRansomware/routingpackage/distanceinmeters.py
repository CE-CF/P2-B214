import numpy as np
from math import *


class DistanceInMeters:
    '''
    To find the distance from one point to another, using latitude/longitude-coordinates,
    the haversine formula is being used.
    The haversine formula calculates the great-circle distance between two points, in a straight line
    ignoring any hills etc.
    So this class is called to calculate the distance between each point in the quadrilateral
    and also the lengths of the diagonals.
    '''

    @staticmethod
    def calculate_distance(first_p, second_p):
        first_p = np.array(first_p)
        second_p = np.array(second_p)

        # print(first_p)
        # print(second_p)

        # hav = haversine = sin^2(lat/2)

        r = 6371000  # Radius of the earth

        lat1 = first_p[0] * np.pi / 180  # convert to radians
        lat2 = second_p[0] * np.pi / 180  # convert to radians

        delta_lat = (second_p[0] - first_p[0]) * np.pi / 180
        delta_lon = (second_p[1] - first_p[1]) * np.pi / 180

        hav_a = (np.sin(delta_lat / 2) * np.sin(delta_lat / 2)) \
                + (np.cos(lat1) * np.cos(lat2) * np.sin(delta_lon / 2)**2)
        hav_c = 2 * np.arctan2(np.sqrt(hav_a), np.sqrt(1 - hav_a))
        distance = r * hav_c

        return distance
