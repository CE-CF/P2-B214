from math import cos, pi

<<<<<<< HEAD
import config
import requests

=======
# https://stackoverflow.com/questions/47106276/converting-pixels-to-latlng-coordinates-from-google-static-image
>>>>>>> 57e3e059cede61d984e7a1b0fdbb9adc73d3aa8b

class Map:
    def __init__(self):
        self.size = 640
        self.lat = 55.669703
        self.long = 12.019524
        self.zoom = 13
        self.key = config.SECRET

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
            + "&style=feature:poi|visibility:off&style=feature:landscape.natural.landcover|visibility:simplified"
            + "&key="
            + str(self.key)
        )
        with open("map.png", "wb") as img:
            img.write(image.content)

    def CalculateCoordinates(self, x, y):
        pixel_degree_x = 360 / 2 ** (self.zoom + 8)
        pixel_degree_y = 360 / 2 ** (self.zoom + 8) * cos(self.lat * pi / 180)
        point_lat = self.lat - pixel_degree_y * (y - self.size / 2)
        point_long = self.long + pixel_degree_x * (x - self.size / 2)

        return point_lat, point_long

    def ZoomIn(self, canvas):
        self.zoom += 1
        self.requestMap()
        canvas.update()

    def ZoomOut(self, canvas):
        self.zoom -= 1
        self.requestMap()
        canvas.update()
