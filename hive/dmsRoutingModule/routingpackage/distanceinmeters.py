import math

import numpy as np
from math import *


def get_x_y_meter_to_coordinates_ratio(origo_c):
    x_coord_dist = abs((origo_c[0] - 0.005) - (origo_c[0] + 0.005))
    y_coord_dist = abs((origo_c[1] - 0.005) - (origo_c[1] + 0.005))
    x_meter_dist = DistanceInMeters.calculate_distance(origo_c - [0, 0.005], origo_c + [0, 0.005])
    y_meter_dist = DistanceInMeters.calculate_distance(origo_c - [0.005, 0], origo_c + [0.005, 0])

    x_ratio = x_coord_dist / x_meter_dist
    y_ratio = y_coord_dist / y_meter_dist

    return x_ratio, y_ratio


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
                + (np.cos(lat1) * np.cos(lat2) * np.sin(delta_lon / 2) ** 2)
        hav_c = 2 * np.arctan2(np.sqrt(hav_a), np.sqrt(1 - hav_a))
        distance = r * hav_c

        return distance


    @staticmethod
    def reverse_calculate(distance):
        # point = np.array(p)
        r = 6371000  # Radius of the earth
        # Latitude, longitude
        point1 = [57.028508, 9.948725]
        point2 = [57.029086, 9.948725]
        # calculations to find the bearing of the y-axis
        # y = np.sin(point2[1]-point1[1])*np.cos(point2[0])
        # x = np.cos(point1[0])*np.sin(point2[0])-np.sin(point1[0])*np.cos(point2[0])*np.cos(point2[1]-point1[1])
        # q = np.arctan2(y,x)
        # bearing = (q*180/np.pi+360) % 360
        # print(bearing)
        lat1 = point1[0] * (math.pi / 180)

        # Den giver lat2 = 0,99534. Det kan ikke passe
        lat2 = math.asin(math.sin(lat1) * math.cos(distance / r) + (math.cos(lat1) * math.sin(distance / r) * math.cos(0)))
        lon2 = point1[1] + math.atan2(math.sin(0) * math.sin(distance / r) * math.cos(lat1),
                                      math.cos(distance / r) - math.sin(lat1) * math.sin(lat2))
        #print("Latitude er: ", lat2)
