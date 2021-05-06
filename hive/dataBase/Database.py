from tableHandlers import *

"""
### drone ###
PythonDrone = drone.Drone('PythonDrone', 'Online', 87.654321, 12.345678)
PythonDrone.insert()
PythonDrone = drone.Drone('PythonDrone', 'Updating', 87.654321, 12.345678)
PythonDrone.update()
PythonDrone.delete() 

### poi ###
PythonDrone = poi.Poi('PythonDrone', 87.654321, 12.345678)
PythonDrone.insert()


### route ###
PythonDrone = route.Route('PythonDrone2', 0, 87.654321, 12.345678, 87.654321, 12.345678, 87.654321, 12.345678, 87.654321, 12.345678, 87.654321, 12.345678, 87.654321, 12.345678)
PythonDrone.insert()

"""
### video ###
PythonDrone = video.Video('PythonDrone')
PythonDrone.insert()
"""
### fetchall ###
test = getTable.fetchall('hive.route')
for x in range(len(test)):    
    print(test[x])

for i in test:
    print(i['drone'])
    print("-------------")
    print(i['lat1'])
    print(i['long1'])
    print(i['received'])
    print("\n")
"""