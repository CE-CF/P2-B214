import requests
import config

class Map:
    size = 800
    long = 12.019524
    lat = 55.669703
    zoom = 15
    key = config.SECRET

    def getCoordinates(self):
        pass

    def requestMap(self):
        # https://maps.googleapis.com/maps/api/staticmap?center=Berkeley,CA&zoom=14&size=400x400&key=
        image = requests.get("https://maps.googleapis.com/maps/api/staticmap?center=" + str(self.lat) + "," + str(self.long) + "&zoom=" + str(self.zoom) + "&size=" + str(self.size) + "x" + str(self.size) + "&key=" + str(self.key))
        with open("map.png", "wb") as img:
            img.write(image.content)