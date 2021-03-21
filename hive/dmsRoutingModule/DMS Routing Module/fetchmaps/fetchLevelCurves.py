# Boundary box

import requests
import shutil
from requests.models import Response

URL = "https://services.datafordeler.dk/DHMNedboer/dhm/1.0.0/WMS?"

service = "WMS"
version = "1.1.1"
requestType = "GetMap"
fileFormat = "image/png"
transparent = "TRUE"
layers = "dhm_kurve_0_5_m"
password = "Jotu*5jellefikadt"
username = "LCTNUGNNHG"
srs = "EPSG:25832"
styles = ""
width = "5000"
height = "5000"
#bbox = "473830,6262421,475144,6262729"
bbox = "474300,6261200,475100,6262000"

PARAMS = {
    'SERVICE': service,
    'VERSION': version,
    'REQUEST': requestType,
    'FORMAT': fileFormat,
    'TRANSPARENT': transparent,
    'LAYERS': layers,
    'password': password,
    'username': username,
    'SRS': srs,
    'STYLES': styles,
    'WIDTH': width,
    'HEIGHT': height,
    'BBOX': bbox
}

response = requests.get(url=URL, params=PARAMS)

print(response.content)

file = open('../img.png', 'wb')
file.write(response.content)
file.close()