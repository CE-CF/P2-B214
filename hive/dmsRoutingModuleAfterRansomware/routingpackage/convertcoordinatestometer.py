import numpy as num


class DistanceInMeters:
    '''
    To find the distance from one point to another, using latitude/longitude-coordinates,
    the haversine formula is being used.
    The haversine formula calculates the great-circle distance between two points, in a straight line
    ignoring any hills etc.
    So this class is called to calculate the distance between each point in the quadrilateral
    and also the lengths of the diagonals.
    '''

    # Lon = x and lat = y, og koordinaterne er (y,x)
    first_point = num.array([])
    second_point = num.array([])
    r = 6371000  # Radius of the earth

    def calculate_distance(self, first_p, second_p):
        # hav = haversine = sin^2(lat/2)

        lat1 = self.first_point[0] * num.pi / 180 # convert to radians
        lat2 = self.second_point[0] * num.pi / 180 # convert to radians

        delta_lat = (first_p[0] - first_p[0]) * num.pi / 180
        delta_lon = (second_p[1] - first_p[1]) * num.pi / 180
        hav_a = (num.sin(delta_lat / 2) * num.sin(delta_lat / 2)) \
                + (num.cos(lat1) * num.cos(lat2) * num.sin(delta_lon / 2) * num.sin(delta_lat / 2))
        hav_c = 2 * num.arctan2(num.sqrt(hav_a), num.sqrt(1 - hav_a))
        distance = self.r * hav_c

        return distance