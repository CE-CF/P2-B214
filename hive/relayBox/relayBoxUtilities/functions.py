# Import the necessary modules
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import socket
import threading
import time
import sys

class Functions():
    def __init__(self, droneID, dronePort, rbPort):
        """ Creating a socket to the drone"""
        self.droneID = droneID
        self.drone = (droneID, dronePort)
        self.rb = ('', rbPort)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.rb)
        self.listenThread = self.listen()
        print("Function object has been created")

    def ping(self):
        """
        Returns True if host (str) responds to a ping request.
        Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
        """

        # Option for the number of packets as a function of
        param = '-n' if platform.system().lower()=='windows' else '-c'

        # Building the command. Ex: "ping -c 1 google.com"
        command = ['ping', param, '5', '{}'.format(self.droneID)]

        return subprocess.call(command) == 0

    def send(self, message, delay):
        """Try to send the message otherwise print the exception"""
        try:
            self.sock.sendto(message.encode(), self.drone)
            print("Sending message: " + message)
        except Exception as e:
            print("Error sending: " + str(e))

        # Delay for a user-defined period of time
        time.sleep(delay)

    def receive(self):
        """Setting up the listener"""
        # Continuously loop and listen for incoming messages
        while True:
            # Try to receive the message otherwise print the exception
            try:
                response1, ip_address = self.sock.recvfrom(1024) # The 1024 is a buffer for the received message, it has to be large enough for any message
                print("Received message: from Tello EDU "+droneID+": "+response1.decode(encoding='utf-8')) # UTF-8 stands for “Unicode Transformation Format - 8 bits.” It can translate any Unicode character to a matching unique binary string, and can also translate the binary string back to a Unicode character. 
            except Exception as e:
                # If there's an error close the socket and break out of the loop
                sock1.close()
                print("Error receiving: " + str(e))
                break
    
    def listen(self):
        """Creates udp response listener"""
        receiveThread = threading.Thread(target=self.receive)
        receiveThread.daemon = True
        receiveThread.start()
        return receiveThread

    def closeConnection(self):
        """ Closes socket and listener"""
        self.listenThread.join()
        self.sock.close()
        print("Connection closed")
