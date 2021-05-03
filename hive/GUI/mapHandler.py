import requests
import config

class Map:
    size = 640
    lat = 55.669703
    long = 12.019524
    zoom = 13
    key = config.SECRET

    def setCoordinates(self, lat, long):
        self.lat = lat
        self.long = long

    def requestMap(self):
        # https://maps.googleapis.com/maps/api/staticmap?center=Berkeley,CA&zoom=14&size=400x400&key=
        image = requests.get("https://maps.googleapis.com/maps/api/staticmap?center=" + str(self.lat) + "," + str(self.long) + "&zoom=" + str(self.zoom) + "&size=" + str(self.size) + "x" + str(self.size) + "&style=feature:poi|visibility:off&style=feature:landscape.natural.landcover|visibility:simplified" + "&key=" + str(self.key))
        with open("map.png", "wb") as img:
            img.write(image.content)