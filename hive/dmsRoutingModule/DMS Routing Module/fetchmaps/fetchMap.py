import requests
import shutil

URL = "https://services.kortforsyningen.dk/service?"

service = "WMS"
version = "1.1.1"
requestType = "GetMap"
fileFormat = "image/jpeg"
transparent = "true"
layers = "orto_sommer_2008"
token = "9854d8016b82278607978089147fe729"
servicename = "orto_sommer_2008"
srs = "EPSG%3A25832"
styles = ""
width = "1311"
height = "852"
bbox = "544073.0084478165%2C6322119.425594802%2C545008.2368164387%2C6322727.217028872"

PARAMS = {
    'SERVICE': service,
    'VERSION': version,
    'REQUEST': requestType,
    'FORMAT': fileFormat,
    'TRANSPARENT': transparent,
    'LAYERS': layers,
    'token': token,
    'servicename': servicename,
    'SRS': srs,
    'STYLES': styles,
    'WIDTH': width,
    'HEIGHT': height,
    'BBOX': bbox
}

response = requests.get(url=URL, params=PARAMS)

print(response)
if response.status_code == "200":
    file = open('../img.jpeg', 'wb')
    file.write(response.content)
    file.close()
else:
    print(response.status_code)