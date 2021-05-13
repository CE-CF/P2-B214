# Import the necessary modules
import platform  # For getting the operating system name
import socket
import subprocess  # For executing a shell command
import sys
import threading
import time

from relayBoxUtilities import *

# IP and port of Tello and Relay Box
tello1 = functions.Functions("192.168.137.103", 8889, 9011)
if tello1.ping() == True:
    # Send connected drone to DMS
    # Receive route navigation commands
    tello1.send("command", 3)
    tello1.send("takeoff", 3)
    # Implement correction algorithm
    tello1.send("land", 1)
    tello1.closeConnection()
else:
    print("Cannot establish connection to tello1")
