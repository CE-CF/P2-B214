import ipaddress
from relayBoxUtilities import *
import time

# Creating packet content for testing
dest = '192.168.137.103'
p_dest = ipaddress.IPv4Address(dest)
b_dest = p_dest.packed
drone_port = 8889
rb_port = 9000+b_dest[3]
CMD_Amount = 3
data = [[0 for x in range(CMD_Amount)] for x in range(CMD_Amount)]
data[0][0] = 'command'
data[0][1] = 1
data[1][0] = 'takeoff'
data[1][1] = 1
data[2][0] = 'land'
data[2][1] = 1

DroneCheck = droneChecker.DroneChecker("192.168.137")
activeDroneList = DroneCheck.ping()
if (len(activeDroneList) > 0):
    print('There are {} active drones'.format(len(activeDroneList))+"\n")
    for x in range (len(activeDroneList)):
        print('Drone {} has ip {}'.format((x+1), activeDroneList[x]))
else:
    print("There are no active drones")




"""
# IP and port of Tello and Relay Box
tello1 = drone.Drone(str(p_dest), drone_port, rb_port)
if (tello1.ping()):
    # Send connected drone to DMS
    # Receive route navigation commands
    for x in range (len(data)):
        tello1.send(data[x][0], data[x][1])
        # Implement correction algorithm
        time.sleep(data[x][1])
    
    tello1.closeConnection()
else:
    print("\n Cannot establish connection to tello1")
"""