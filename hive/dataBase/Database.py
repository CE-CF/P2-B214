from tableHandlers import *

########################################################## Old
#All drone related commands
"""
There are 3 different drone commands:
When using drone_old.insert()
The inserting variables are ('DroneName', 'state', latitude, longitude)
When using drone_old.update()
The updating variables are ('DroneName', 'state', latitude, longitude)
When using the drone_old.delete()
The delete variables are ('DroneName')
"""
#EXAMPLES FOR drone_old.insert/update/delete
#drone_old.insert('PythonTest', 'inserting', 12.345678, 12.345678)
#drone_old.insert('PythonTest2', 'inserting', 87.654321, 87.654321)
#drone_old.update('PythonTest', 'updating', 87.654321, 87.654321)
#drone_old.delete('PythonTest')
#All point of interest related commands
"""
When using poi_old.new()
The inserted variables are ('DroneName', latitude, longitude)
"""
#EXAMPLES FOR poi_old.new()
#poi_old.new('testdrone', 00.000000, 00.000000)
#poi_old.new('Drone1', 11.111111, 11.111111)
#poi_old.new('Drone2', 22.222222, 22.222222)
#poi_old.new('Drone3', 33.333333, 33.333333)

#All route related commands
"""
When using the route_old.new()
The inserted variables are ('DroneName', 'type[1,2]', latitude1, longitude1,..... latitudeN, longitudeN)
"""
#EXAMPLES FOR route_old.new()
#route_old.new('TESTER', 5, 66.666666, 66.666666) #DOES NOT WORK, TYPE IS != [1,2]
#route_old.new('testdrone1', 1, 12.345678, 12.345678)
#route_old.new('testdrone2', 2, 87.654321, 87.654321, 12.345678, 12.345678, 12.345678, 12.345678, 12.345678, 12.345678, 12.345678, 12.345678, 12.345678, 12.345678, 12.345678, 12.345678, 12.345678, 12.345678)

#ALL video related commands
"""
Initiating video stream for drone
video_old.stream()
The streaming variable is ('DroneName')
"""
#EXAMPLE FOR video_old.stream()
#videoV1.stream('PythonTest')



###########################################################

PythonDrone = drone.Drone('PythonDrone', 'Online', 87.654321, 12.345678)

print("drone table handler")
#PythonDrone.insert()


PythonDrone = drone.Drone('PythonDrone', 'Updating', 87.654321, 12.345678)
#PythonDrone.update()
PythonDrone.delete()
print("\n") 
"""
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

test = getTable.fetchall('hive.drone')
for x in range(len(test)):    
    print(test[x])

for i in test:
    print(i['drone'])
    print("-------------")
    print(i['state'])
    print(i['lat'])
    print(i['long'])
    print("\n")
"""