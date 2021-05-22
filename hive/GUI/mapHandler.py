from math import cos, pi
from dmsRoutingModule.routingpackage.distanceinmeters import DistanceInMeters as dim
import config
import requests
import numpy as np

class Map:
    def __init__(self):
        self.size = 640
        self.lat = 55.675468
        self.long = 12.029094
        self.zoom = 13
        self.maptype = "roadmap"
        self.key = config.SECRET
        self.requestMap()

    def setCoordinates(self, lat, long):
        self.lat = lat
        self.long = long

    def requestMap(self):
        # https://maps.googleapis.com/maps/api/staticmap?center=Berkeley,CA&zoom=14&size=400x400&key=
        image = requests.get(
            "https://maps.googleapis.com/maps/api/staticmap?center="
            + str(self.lat)
            + ","
            + str(self.long)
            + "&zoom="
            + str(self.zoom)
            + "&size="
            + str(self.size)
            + "x"
            + str(self.size)
            + "&maptype="
            + self.maptype
            + "&style=feature:poi|visibility:off&style=feature:landscape.natural.landcover|visibility:simplified"
            + "&key="
            + str(self.key)
        )
        with open("map.png", "wb") as img:
            img.write(image.content)

    def CalculateCoordinates(self, x, y):
        """
        A function to calculate coordinates from pixel coordinates by Ivan Shukshin
        https://stackoverflow.com/questions/47106276/converting-pixels-to-latlng-coordinates-from-google-static-image
        """
        pixel_degree_x = 360 / 2 ** (self.zoom + 8)
        pixel_degree_y = 360 / 2 ** (self.zoom + 8) * cos(self.lat * pi / 180)
        point_lat = self.lat - pixel_degree_y * (y - self.size / 2)
        point_long = self.long + pixel_degree_x * (x - self.size / 2)

        return point_lat, point_long

    def ZoomIn(self, canvas):
        self.zoom += 1
        self.requestMap()
        canvas.update()
        canvas.UpdateInfo()

    def ZoomOut(self, canvas):
        self.zoom -= 1
        self.requestMap()
        canvas.update()
        canvas.UpdateInfo()


    def setMapType(self, canvas):
        if self.maptype == "roadmap":
            self.maptype = "satellite"
        else:
            self.maptype = "roadmap"
        self.requestMap()
        canvas.update()

    def calcScale(self):
        left_side = np.array(self.CalculateCoordinates(0, 620))
        right_side = np.array(self.CalculateCoordinates(620, 620))
        return round(dim.calculate_distance(left_side, right_side), 2)

