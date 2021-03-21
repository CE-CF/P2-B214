from tableHandlers import *

########################################################## V1
#All drone related commands
"""
There are 3 different drone commands:
When using drone.insert()
The inserting variables are ('DroneName', 'state', latitude, longitude)
When using drone.update()
The updating variables are ('DroneName', 'state', latitude, longitude)
When using the drone.delete()
The delete variables are ('DroneName')
"""
#EXAMPLES FOR drone.insert/update/delete
#droneV1.insert('PythonTest', 'inserting', 12.345678, 12.345678)
#droneV1.update('PythonTest', 'updating', 87.654321, 87.654321)
#droneV1.delete('PythonTest')

#All point of interest related commands
"""
When using poi.new()
The inserted variables are ('DroneName', latitude, longitude)
"""
#EXAMPLES FOR poi.new()
#poiV1.new('testdrone', 00.000000, 00.000000)
#poiV1.new('Drone1', 11.111111, 11.111111)
#poiV1.new('Drone2', 22.222222, 22.222222)
#poiV1.new('Drone3', 33.333333, 33.333333)

#All route related commands
"""
When using the route.new()
The inserted variables are ('DroneName', 'type[1,2]', latitude1, longitude1,..... latitudeN, longitudeN)
"""
#EXAMPLES FOR route.new()
#route.new('TESTER', 5, 66.666666, 66.666666) DOES NOT WORK, TYPE IS != [1,2]
#route.new('testdrone1', 1, 12.345678, 12.345678)
#route.new('testdrone2', 2, 87.654321, 87.654321, 12.345678, 12.345678, 12.345678, 12.345678, 12.345678, 12.345678, 12.345678, 12.345678, 12.345678, 12.345678, 12.345678, 12.345678, 12.345678, 12.345678)

#ALL video related commands
"""
Initiating video stream for drone
video.stream()
The streaming variable is ('DroneName')
"""
#EXAMPLE FOR video.stream()
#video.stream('PythonTest')

###########################################################

PythonDrone = drone.Drone('PythonDrone', 87.654321, 12.345678)
print("drone table handler")
PythonDrone.insert()
PythonDrone.update()
PythonDrone.delete()
print("\n")

print("poi table handler")
PythonDrone = poi.Poi('PythonDrone', 87.654321, 12.345678)

PythonDrone.insert()
print("\n")

print("route table handler")
PythonDrone = route.Route('PythonDrone', 87.654321, 12.345678, 87.654321, 12.345678, 87.654321, 12.345678, 87.654321, 12.345678, 87.654321, 12.345678, 87.654321, 12.345678, 87.654321, 12.345678)

PythonDrone.insert()
print("\n")

print("video table handler")
PythonDrone = video.Video('PythonDrone')
PythonDrone.insert()