from tableHandlers import *

"""
### drone ###
hotSpotIP = "192.168.137"
droneIDList = ["100", "101"]
first_drone = hotSpotIP+"."+droneIDList[0]
PythonDrone = drone.Drone(first_drone, 'PythonTest', 'Offline', 87.654321, 12.345678)
PythonDrone = drone.Drone(first_drone, bat="85")
PythonDrone.insert()
PythonDrone.update()
PythonDrone.delete()

### poi ###
PythonDrone = poi.Poi('PythonDrone', 87.654321, 12.345678)
PythonDrone.insert()

### route ###
PythonDrone = route.Route('PythonDrone2', 0, 87.654321, 12.345678, 87.654321, 12.345678, 87.654321, 12.345678, 87.654321, 12.345678, 87.654321, 12.345678, 87.654321, 12.345678)
PythonDrone.insert()

### video ###
PythonDrone = video.Video('PythonDrone')
PythonDrone.insert()

### fetchall ###
test1 = getTable.fetchall('hive.drone')

OPCstring = "CMD:GET_DRONE;"
for x in range (len(test1)):
    print(test1[x]['drone'])
    print(test1[x]['droneID'])
    OPCstring += test1[x]['drone']+":"+test1[x]['droneID']+";"
print(OPCstring)
"""