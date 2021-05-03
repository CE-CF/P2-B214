# Import the necessary modules
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import socket
import threading
import time
import sys

class Functions():
    def __init__(self):
        print("Function object has been created")

    def ping(host):
        """
        Returns True if host (str) responds to a ping request.
        Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
        """

        # Option for the number of packets as a function of
        param = '-n' if platform.system().lower()=='windows' else '-c'

        # Building the command. Ex: "ping -c 1 google.com"
        command = ['ping', param, '5', host]

        return subprocess.call(command) == 0

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
                response1, ip_address = sock1.recvfrom(128) # The 128 is a buffer for the received message, it has to be large enough for any message
                #response2, ip_address = sock2.recvfrom(128)
                print("Received message: from Tello EDU #1: " + response1.decode(encoding='utf-8')) # UTF-8 stands for “Unicode Transformation Format - 8 bits.” It can translate any Unicode character to a matching unique binary string, and can also translate the binary string back to a Unicode character. 
                print("Received message: from Tello EDU #2: " + response2.decode(encoding='utf-8'))
            except Exception as e:
                # If there's an error close the socket and break out of the loop
                sock1.close()
                #sock2.close()
                print("Error receiving: " + str(e))
                break