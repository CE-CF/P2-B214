from threading import Thread
from socket import socket, AF_INET, SOCK_DGRAM, timeout
import traceback

class Tello_Communication(Thread):

    def __init__(self):
        super().__init__()
        self.Running = True
        self.Tello = []


    """
    The receive command
    """

    def Receive_Command(self, Command: str, Drone_ID):
        Command_Array = Command.split(" ")
        if len(Command_Array) == 0:
            return "error"
        elif Command_Array[0] == "command":
            # If it ever happens make this the thing that activates the drone
            return "ok"
        elif Command_Array[0] == "takeoff":
            Result = self.Tello[Drone_ID].Landed_State(False)
            return (Result*"ok" + (not Result)*"error")
        elif Command_Array[0] == "land":
            Result = self.Tello[Drone_ID].Landed_State(True)
            return (Result*"ok" + (not Result)*"error")
        elif Command_Array[0] == "streamon":
            Result = self.Tello[Drone_ID].Stream_OnOff(True)
            return (Result*"ok" + (not Result)*"error")
        elif Command_Array[0] == "streamoff":
            Result = self.Tello[Drone_ID].Stream_OnOff(False)
            return (Result*"ok" + (not Result)*"error")
        elif Command_Array[0] == "emergency":
            self.Tello[Drone_ID].Emergency()
            return "ok"
        elif Command_Array[0] == "up":
            print("Got up command")
            try:
                print("Up command no error")
                print(f'Command array is: {Command_Array}')
                Distance = float(Command_Array[1])
                Result = self.Tello[Drone_ID].Moveto(Amount_z = Distance)
                return (Result*"ok" + (not Result)*"error")
            except(TypeError or ValueError):
                print("Up command error")
                return "error"
        elif Command_Array[0] == "down":
            try:
                Distance = float(Command_Array[1])
                Result = self.Tello[Drone_ID].Moveto(Amount_z = -Distance)
                return (Result*"ok" + (not Result)*"error")
            except(TypeError or ValueError):
                return "error"
        elif Command_Array[0] == "left":
            try:
                print("Left command no error")
                print(f'Command array is: {Command_Array}')
                Distance = float(Command_Array[1])
                Result = self.Tello[Drone_ID].Moveto(Amount_RL = -Distance)
                return (Result*"ok" + (not Result)*"error")
            except(TypeError or ValueError):
                return "error"
        elif Command_Array[0] == "right":
            try:
                Distance = float(Command_Array[1])
                Result = self.Tello[Drone_ID].Moveto(Amount_RL = Distance)
                return (Result*"ok" + (not Result)*"error")
            except(TypeError or ValueError):
                return "error"
        elif Command_Array[0] == "forward":
            try:
                Distance = float(Command_Array[1])
                Result = self.Tello[Drone_ID].Moveto(Amount_FB = Distance)
                print(f'Forward result is: {Result}')
                return (Result*"ok" + (not Result)*"error")
            except(TypeError or ValueError):
                return "error"
        elif Command_Array[0] == "back":
            try:
                Distance = float(Command_Array[1])
                Result = self.Tello[Drone_ID].Moveto(Amount_FB = -Distance)
                return (Result*"ok" + (not Result)*"error")
            except(TypeError or ValueError):
                return "error"
        elif Command_Array[0] == "cw":
            try:
                Rotation = float(Command_Array[1])
                Result = self.Tello[Drone_ID].Rotate_Yaw(Rotation)
                return (Result*"ok" + (not Result)*"error")
            except(TypeError or ValueError):
                return "error"
        elif Command_Array[0] == "ccw":
            try:
                Rotation = float(Command_Array[1])
                Result = self.Tello[Drone_ID].Rotate_Yaw(-Rotation)
                return (Result*"ok" + (not Result)*"error")
            except(TypeError or ValueError):
                return "error"
        elif Command_Array[0] == "flip":
            return "ok"
        elif Command_Array[0] == "go":
            if len(Command_Array) != 5:
                return "error"
            else:
                try:
                    Distance_x = float(Command_Array[1])
                    Distance_y = float(Command_Array[2])
                    Distance_z = float(Command_Array[3])
                    Speed = float(Command_Array[4])
                    Result = self.Tello[Drone_ID].Moveto(Distance_x,Distance_y,Distance_z,Speed)
                    return (Result*"ok" + (not Result)*"error")
                except(TypeError or ValueError):
                    return "error"
        elif Command_Array[0] == "stop":
            self.Tello[Drone_ID].Stop_Command()
            return "ok"
        elif Command_Array[0] == "curve":
            return "error"
        elif Command_Array[0] == "jump":
            return "error"

        elif Command_Array[0] == "speed":
            Speed = Command_Array[1]
            self.Tello[Drone_ID].Set_Speed(Speed)
        elif Command_Array[0] == "rc":
            pass
        elif Command_Array[0] == "wifi":
            pass
        elif Command_Array[0] == "mon":
            return "error"
        elif Command_Array[0] == "moff":
            return "error"
        elif Command_Array[0] == "mdirection":
            return "error"
        elif Command_Array[0] == "ap":
            pass

        elif Command_Array[0] == "speed?":
            return self.Tello[Drone_ID].Read_Speed()
        elif Command_Array[0] == "battery?":
            return self.Tello[Drone_ID].Read_Battery()
        elif Command_Array[0] == "time?":
            return self.Tello[Drone_ID].Read_Time
        elif Command_Array[0] == "wifi?":
            pass
        elif Command_Array[0] == "sdk?":
            return "sdk 2.0"
        elif Command_Array[0] == "sn?":
            return self.Tello[Drone_ID].Serial_Number()

        else:
            return "error"

    def Add_Drone(self, Drone):
        self.Tello.append(Drone)

    def Sort_Command(self, Command: str):
        Command_Array = Command.split(": ")
        Result = None
        IP_Found = False
        print(f'\tCommand Array is: {Command_Array}')
        print(f'\tCommand Array 0 is: {Command_Array[0]}')
        for i in range(len(self.Tello)):
            print(f'\tTello IP is : {self.Tello[i].IP_Address}')
            if self.Tello[i].IP_Address == Command_Array[0]:
                print(f"\tfound a drone in {self.Tello[i].IP_Address}")
                Result = self.Receive_Command(Command_Array[1], i)
                IP_Found = True
            else:
                continue
        print(f'Result is: {Result}')
        if not IP_Found:
            return "error ip not found"
        elif Result == None:
            return "error"
        else:
            return Result


    def run(self):
        Host = ''           # Symbolic name meaning all available interfaces
        #HOST = "192.168.56.1"
        Port = 8889         # Arbitrary non-privileged port
        Buffer_Size = 1024  # Receive Buffer size (power of 2)

        Command_Socket = socket(AF_INET,SOCK_DGRAM) # IPv4, UDP
        Command_Socket.bind((Host, Port))    # Bind sockect to the address
        Command_Socket.settimeout(1)
        print('UDP server running...')
        print('Listening for incoming connections in port '+str(Port))

        while self.Running:
            try:
                r,a = Command_Socket.recvfrom(Buffer_Size)    # Receive datagram
            except timeout:
                #print("\tSocket timout")
                continue
            """
            TODO: Implement the send in a thread,
            so that it does not wait for the drone to finish before taking an order for a different drone.
            """

            # r is the received data
            # a is the address bound to the socket on the other end of the connection
            r_str = str(r, 'UTF-8')
            #UTFr = str(r, encoding = "UTF-8")
            #print(f'\tIncoming text: {UTFr}')
            print(f'\tIncoming text: {r_str}')
            Result = self.Sort_Command(r_str)
            Command_Socket.sendto(bytes(Result, 'UTF-8'), a)
            print(f'\tReturned text: {Result}')

            #s.sendto(bytes(f'General Kenobi. Please stop contacting me. I got your message from {a[0]}','UTF-8'), a)
        print(f'\tOut of while loop')
        Command_Socket.close()


    def close(self):
        print("\tClosing thread")
        self.Running = False
        print('\tThread Closed')