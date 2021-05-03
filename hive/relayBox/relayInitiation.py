# Import the necessary modules
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import socket
import threading
import time
import sys
from relayBoxUtilities import *

INTERVAL = 0.2
# IP and port of Tello
tello1_address = ('192.168.137.97', 8889)
#tello2_address = ('192.168.0.101', 8889)

# IP and port of local computer
local1_address = ('', 9010)
#local2_address = ('', 9011)

# Create a UDP connection that we'll send the command to
sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the local address and port
sock1.bind(local1_address)
#sock2.bind(local2_address)

def send(message, delay):
        """Try to send the message otherwise print the exception"""
        try:
            sock1.sendto(message.encode(), tello1_address)
            #sock2.sendto(message.encode(), tello2_address)
            print("Sending message: " + message)
        except Exception as e:
            print("Error sending: " + str(e))

        # Delay for a user-defined period of time
        time.sleep(delay)

def receive():
        # Continuously loop and listen for incoming messages
        while True:
            # Try to receive the message otherwise print the exception
            try:
                response1, ip_address = sock1.recvfrom(1024) # The 128 is a buffer for the received message, it has to be large enough for any message
                #response2, ip_address = sock2.recvfrom(128)
                print("Received message: from Tello EDU #1: " + response1.decode(encoding='utf-8')) # UTF-8 stands for “Unicode Transformation Format - 8 bits.” It can translate any Unicode character to a matching unique binary string, and can also translate the binary string back to a Unicode character. 
                #print("Received message: from Tello EDU #2: " + response2.decode(encoding='utf-8'))
                if response == 'ok':
                    continue
                out = response.replace(';', ';\n')
                out = 'Tello State:\n' + out
                report(out)
                sleep(INTERVAL)
            except Exception as e:
                # If there's an error close the socket and break out of the loop
                sock1.close()
                #sock2.close()
                print("Error receiving: " + str(e))
                break

# Create and start a listening thread that runs in the background
# This utilizes our receive functions and will continuously monitor for incoming messages
receiveThread = threading.Thread(target=receive)
receiveThread.daemon = True
receiveThread.start()

send("command", 3)
try:
        index = 0
        while True:
            index += 1
            response, ip = socket.recvfrom(1024)
            if response == 'ok':
                continue
            out = response.replace(';', ';\n')
            out = 'Tello State:\n' + out
            report(out)
            sleep(INTERVAL)
    except KeyboardInterrupt:
        curses.echo()
        curses.nocbreak()
        curses.endwin()
#send("takeoff",8)
#send("land", 3 )
#send('takeoff', 3)
#send('land', 1)
# Close the socket
sock1.close()
#sock2.close()

#testPing = functions.Functions.ping("192.168.137.241")



