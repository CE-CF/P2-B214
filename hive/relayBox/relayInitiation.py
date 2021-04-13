# Import the necessary modules
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import socket
import threading
import time
from relayBoxUtilities import *

"""
# IP and port of Tello
tello1_address = ('192.168.0.100', 8889)
tello2_address = ('192.168.0.101', 8889)

# IP and port of local computer
local1_address = ('', 9010)
local2_address = ('', 9011)

# Create a UDP connection that we'll send the command to
sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the local address and port
sock1.bind(local1_address)
sock2.bind(local2_address)

# Create and start a listening thread that runs in the background
# This utilizes our receive functions and will continuously monitor for incoming messages
receiveThread = threading.Thread(target=receive)
receiveThread.daemon = True
receiveThread.start()

# Close the socket
sock1.close()
sock2.close()
"""
testPing = functions.Functions.ping("google.com")




