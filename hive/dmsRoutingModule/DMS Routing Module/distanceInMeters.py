import numpy as num


class DistanceInMeters:
    '''
    To find the distance from one point to another, using latitude/longitude-coordinates,
    the haversine formula is being used.
    The haversine formula calculates the great-circle distance between two points, in a straight line
    ignoring any hills etc.
    '''
    # Lon = x and lat = y, og koordinaterne er (y,x)
    first_point = num.array([])
    second_point = num.array([])
    r = 6371000  # Radius of the earth

    def __init__(self, first_p, second_p):
        self.first_point = first_p
        self.second_point = second_p

    def calculate_distance(self):
        """
        ɸ = latitude
        λ = longitude
        Δ = difference
        hav = haversine = sin^2(ɸ/2)
        """
        ɸ1 = self.first_point[0] * num.pi / 180 #convert to radians
        ɸ2 = self.second_point[0] * num.pi / 180 # convert to radians

        Δɸ = (self.second_point[0] - self.first_point[0]) * num.pi / 180
        Δλ = (self.second_point[1] - self.first_point[1]) * num.pi / 180
        hav_a = (num.sin(Δɸ / 2) * num.sin(Δɸ / 2)) + (num.cos(ɸ1) * num.cos(ɸ2) * num.sin(Δλ / 2) * num.sin(Δλ / 2))
        hav_c = 2 * num.arctan2(num.sqrt(hav_a), num.sqrt(1 - hav_a))
        distance = self.r * hav_c
        return distance
