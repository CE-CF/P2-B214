# Import the necessary modules
import platform  # For getting the operating system name
import socket
import subprocess  # For executing a shell command
import sys
import threading
import time


class Drone(threading.Thread):
    def __init__(self, droneID, dronePort, rbPort, cmdstr):
        """ Creating a socket to the drone"""
        if (self.testSocket(droneID, dronePort, rbPort)) == True:
            super(Drone, self).__init__()
            self._stop_event = threading.Event()
            self.droneID = droneID
            self.drone = (droneID, dronePort)
            self.rb = ("", rbPort)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind(self.rb)
            self.yaw_response = []
            self.yaw = 0
            self.oppo_yaw = 0
            self.cmdstr = cmdstr
            self.stopVariable = True
            self.keepThreadRunning = True
            self.threadRunning = True
            self.cmd_seq = 0
        else:
            print("Drone object was not created, port was not open")

    def stop(self):
        self.stopVariable = False

    def stopThread(self):
        self.keepThreadRunning = False

    def testSocket(self, socket_ip, socket_port, bind_port):
        """ Test to see if a socket is open """
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        local = ("", bind_port)
        location = (socket_ip, socket_port)

        a_socket.bind(local)

        result_of_check = a_socket.connect_ex(location)

        if result_of_check == 0:
            print("Port is open")
            output = True
        else:
            print("Port is not open")
            output = False
        a_socket.close()
        # a_socket.shutdown(socket.SHUT_RDWR)

        return output

    def getID(self):
        return self.droneID

    def setYaw(self, yaw):
        self.yaw_response.append(yaw)

    def ping(self):
        """
        Returns True if host (str) responds to a ping request.
        Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
        """

        # Option for the number of packets as a function of
        param = "-n" if platform.system().lower() == "windows" else "-c"

        # Building the command. Ex: "ping -c 1 google.com"
        command = ["ping", param, "5", "{}".format(self.droneID)]

        return subprocess.call(command) == 0

    def send(self, message, delay):
        """Try to send CMD to drone, otherwise print exception"""
        try:
            self.sock.sendto(message.encode(encoding="utf-8"), self.drone)
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
                response1, ip_address = self.sock.recvfrom(
                    1024
                )  # The 1024 is a buffer for the received message, it has to be large enough for any message
                print(
                    "Received message: from Tello EDU "
                    + self.droneID
                    + ": "
                    + response1.decode(encoding="utf-8")
                )  # UTF-8 stands for “Unicode Transformation Format - 8 bits.” It can translate any Unicode character to a matching unique binary string, and can also translate the binary string back to a Unicode character.
            except Exception as e:
                # If there's an error close the socket and break out of the loop
                self.sock.close()
                print("Error receiving: " + str(e))
                break

    def closeConnection(self):
        """ Closes socket and listener"""
        self.sock.close()
        self.sock.shutdown(socket.SHUT_RDWR)
        print("Connection closed")

    def get_yaw_response(self):
        return int(self.yaw_response[-1])

    def uplink(self, cmd):
        try:
            if "end" in cmd:
                print("ending")
                self.sock.close()
                self.sock.shutdown(1)
                pass
            # cmd = "0.0.0.0: " + cmd
            print("Uplinking cmd: " + cmd)
            cmd = cmd.encode(encoding="utf-8")
            self.sock.sendto(cmd, self.drone)
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt\n")
            cmd = "land".encode(encoding="utf-8")
            self.sock.sendto(cmd, self.drone)
            self.sock.close()
            self.sock.shutdown(1)

    # # # PATH FOLLOWING

    def straight(self, straight_yaw, flight_time):
        drone_speed = 100
        delay = 1
        is_deviating = False

        start_time = time.time()

        while (time.time() - start_time) < float(
            flight_time
        ):  # if the drone flies at 1 m/s then this works
            if float(flight_time) - (time.time() - start_time) < 2:
                print()
                drone_speed = 40

            newest_yaw_response = (
                self.get_yaw_response()
            )  # is redefined after each loop
            newest_yaw_response = int(
                newest_yaw_response
            )  # for some reason it doesn't work in one line..

            if newest_yaw_response == int(straight_yaw):  # no deviation
                pass
            else:  # if there is deviation...
                is_deviating = True  # <-- this is set to true

            if is_deviating:
                from_yaw = newest_yaw_response + 180
                to_yaw = int(straight_yaw) + 180

                if (
                    from_yaw < to_yaw
                ):  # checking if the drone should turn cw or ccw
                    diff = to_yaw - from_yaw
                    if diff < 180:
                        yaw_per_sec = abs(
                            diff / delay
                        )  # these lines of code calculate
                    else:  # the angle between the current drone
                        yaw_per_sec = -abs(
                            (360 - diff) / delay
                        )  # self.yaw and the correct drone self.yaw
                else:
                    diff = (
                        from_yaw - to_yaw
                    )  # the code also takes the overflowing
                    if (
                        diff < 180
                    ):  # self.yaw values from -180 to 180 into account
                        yaw_per_sec = -abs(
                            diff / delay
                        )  # so that the shortest angle is always found
                    else:
                        yaw_per_sec = abs((360 - diff) / delay)

                if yaw_per_sec < -100:
                    yaw_per_sec = -100
                elif yaw_per_sec > 100:
                    yaw_per_sec = 100

                is_deviating = False
            else:
                yaw_per_sec = 0

            rc_string = "rc 0 " + str(drone_speed) + " 0 " + str(yaw_per_sec)
            self.uplink(rc_string)
            time.sleep(delay)

    # # # COMMANDS # # #

    def base_commands(self, cmd):

        if cmd == "init":
            print(cmd)
            self.uplink("command")
            time.sleep(3)
            self.uplink("streamon")
            time.sleep(2)
            self.uplink("rc 0 0 0 0")
            time.sleep(2)
            # self.uplink("takeoff")
            # time.sleep(5)

        elif cmd == "rc0":
            print(cmd)
            self.uplink("rc 0 0 0 0")

        elif cmd == "stop":
            print(cmd)
            self.uplink(cmd)

        elif cmd == "land":
            print(cmd)
            self.uplink(cmd)
            time.sleep(2)
            self.uplink("streamoff")

        elif cmd == "getyaw":
            print(cmd)
            if (
                len(self.yaw_response) != 0
            ):  # if array is empty ... this is due to no tello states coming in
                self.yaw = self.yaw_response[-1]
            else:
                self.yaw_response.append(0)
                print("yaw has been set to 0 - use this for test purposes")

        elif cmd == "getoppoyaw":
            print(cmd)
            if self.yaw < 0:
                self.oppo_yaw = 180 + self.yaw
            elif self.yaw > 0:
                self.oppo_yaw = self.yaw - 180
            else:
                self.oppo_yaw = 179

    def param_commands(self, cmd, value):
        if cmd == "rotate":
            if int(float(value)) < 0:
                pass
                print("ccw ", abs(int(float(value))))
                self.uplink("ccw " + str(abs(int(float(value)))))
            elif int(float(value)) > 0:
                pass
                print("cw ", abs(int(float(value))))
                self.uplink("cw " + str(abs(int(float(value)))))
            else:
                pass  # don't rotate

        if cmd == "wait":
            print(cmd, value)
            time.sleep(int(value))

        if cmd == "straight":
            print(cmd, value[0], value[1])
            if value[0] == "yaw":
                self.straight(self.yaw, flight_time=value[1])
            elif value[0] == "oppoyaw":
                self.straight(self.oppo_yaw, flight_time=value[1])
            else:
                self.straight(
                    int(value[0]), flight_time=value[1]
                )  # if it already has a value

        if cmd == "turn":
            print(cmd, value[0], value[1])
            start_time = time.time()
            cmd = "rc 0 50 0 " + str(value[0])
            while (time.time() - start_time) < float(value[1]):
                self.uplink(cmd)

    def parser(self, cmd_str):
        d = {}
        delim1 = ";"
        delim2 = ":"
        element = ""
        print(cmd_str)
        for _, v in enumerate(cmd_str):
            if self.stopVariable:
                if v is not delim1:
                    element += v
                else:
                    arr = element.split(delim2)
                    if len(arr) == 1:
                        self.base_commands(arr[0])
                    elif len(arr) == 2:
                        if (
                            arr[0] == "yaw"
                        ):  # downlink() needs to parse self.yaw
                            return arr[1]
                        self.param_commands(arr[0], arr[1])
                    elif len(arr) == 3:
                        # print("boooooo   ", arr, len(arr))
                        # print("boooooo  ", arr[0], [arr[1], arr[2]])
                        self.param_commands(arr[0], [arr[1], arr[2]])
                    element = ""

    def run(self):
        self.parser(self.cmdstr)
        while True:
            if not self.keepThreadRunning:
                break
