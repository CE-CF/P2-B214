import math
import numpy as np


def get_x_y_meter_to_coordinates_ratio(origo_c):

    origo_correct_order = [origo_c[1], origo_c[0]]

    # x relates to latitude and y to longitude

    x_coord_dist = abs((origo_correct_order[0] - 0.0001) - (origo_correct_order[0] + 0.0001))
    y_coord_dist = abs((origo_correct_order[1] - 0.0001) - (origo_correct_order[1] + 0.0001))

    x_meter_dist = DistanceInMeters.calculate_distance([origo_correct_order[0] - 0.0001, origo_correct_order[1]],
                                                       [origo_correct_order[0] + 0.0001, origo_correct_order[1]])

    y_meter_dist = DistanceInMeters.calculate_distance([origo_correct_order[0], origo_correct_order[1] - 0.0001],
                                                       [origo_correct_order[0], origo_correct_order[1] + 0.0001])

    x_ratio = x_coord_dist / x_meter_dist
    y_ratio = y_coord_dist / y_meter_dist

    # print('{0:f}'.format(x_ratio), '{0:f}'.format(y_ratio))
    # print(x_ratio, y_ratio)

    # return the lat-lon-coordinates to get (lon,lat)
    return y_ratio, x_ratio


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