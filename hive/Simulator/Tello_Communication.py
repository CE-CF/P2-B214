import threading
import time
from socket import socket, AF_INET, SOCK_DGRAM, timeout
import traceback

class Tello_Communication(threading.Thread):

    def __init__(self):
        super().__init__()
        self.Host = ''           # Symbolic name meaning all available interfaces
        self.Running = True
        self.Tello = []
        self.Connected_Address = None


    """
    The receive command
    """

    def Receive_Command(self, Command: str, Drone_ID):
        Command_Array = Command.split(" ")
        Array_Len = len(Command_Array)
        if len(Command_Array) == 0:
            return "error"
        elif Command_Array[0] == "command":
            # If it ever happens make this the thing that activates the drone
            if Array_Len != 1:
                return "error"
            else:
                return "command"
        elif Command_Array[0] == "takeoff":
            if Array_Len != 1:
                return "error"
            else:
                Result = self.Tello[Drone_ID].Landed_State(False)
                return (Result*"ok" + (not Result)*"error")
        elif Command_Array[0] == "land":
            if Array_Len != 1:
                return "error"
            else:
                Result = self.Tello[Drone_ID].Landed_State(True)
                return (Result*"ok" + (not Result)*"error")
        elif Command_Array[0] == "streamon":
            if Array_Len != 1:
                return "error"
            else:
                Result = self.Tello[Drone_ID].Stream_OnOff(True)
                return (Result*"ok" + (not Result)*"error")
        elif Command_Array[0] == "streamoff":
            if Array_Len != 1:
                return "error"
            else:
                Result = self.Tello[Drone_ID].Stream_OnOff(False)
                return (Result*"ok" + (not Result)*"error")
        elif Command_Array[0] == "emergency":
            if Array_Len != 1:
                return "error"
            else:
                self.Tello[Drone_ID].Emergency()
                return "ok"
        elif Command_Array[0] == "up":
            if Array_Len != 2:
                return "error"
            else:
                print("Got up command")
                try:
                    print("Up command no error")
                    print(f'Command array is: {Command_Array}')
                    Distance = float(Command_Array[1])
                    Result = self.Tello[Drone_ID].Moveto(Amount_z = Distance, Speed_Ratio = 0)
                    return (Result*"ok" + (not Result)*"error")
                except(TypeError or ValueError):
                    print("Up command error")
                    return "error"
        elif Command_Array[0] == "down":
            if Array_Len != 2:
                return "error"
            else:
                try:
                    Distance = float(Command_Array[1])
                    Result = self.Tello[Drone_ID].Moveto(Amount_z = -Distance, Speed_Ratio = 0)
                    return (Result*"ok" + (not Result)*"error")
                except(TypeError or ValueError):
                    return "error"
        elif Command_Array[0] == "left":
            if Array_Len != 2:
                return "error"
            else:
                try:
                    print("Left command no error")
                    print(f'Command array is: {Command_Array}')
                    Distance = float(Command_Array[1])
                    Result = self.Tello[Drone_ID].Moveto(Amount_RL = -Distance, Speed_Ratio = 0)
                    return (Result*"ok" + (not Result)*"error")
                except(TypeError or ValueError):
                    return "error"
        elif Command_Array[0] == "right":
            if Array_Len != 2:
                return "error"
            else:
                try:
                    Distance = float(Command_Array[1])
                    Result = self.Tello[Drone_ID].Moveto(Amount_RL = Distance, Speed_Ratio = 0)
                    return (Result*"ok" + (not Result)*"error")
                except(TypeError or ValueError):
                    return "error"
        elif Command_Array[0] == "forward":
            if Array_Len != 2:
                return "error"
            else:
                try:
                    Distance = float(Command_Array[1])
                    Result = self.Tello[Drone_ID].Moveto(Amount_FB = Distance, Speed_Ratio = 0)
                    print(f'Forward result is: {Result}')
                    return (Result*"ok" + (not Result)*"error")
                except(TypeError or ValueError):
                    return "error"
        elif Command_Array[0] == "back":
            if Array_Len != 2:
                return "error"
            else:
                try:
                    Distance = float(Command_Array[1])
                    Result = self.Tello[Drone_ID].Moveto(Amount_FB = -Distance, Speed_Ratio = 0)
                    return (Result*"ok" + (not Result)*"error")
                except(TypeError or ValueError):
                    return "error"
        elif Command_Array[0] == "cw":
            if Array_Len != 2:
                print("\t\t\tAREADAD")
                return "error"
            else:
                print("\t\t\tCW SUCCESS")
                try:
                    Rotation = float(Command_Array[1])
                    Result = self.Tello[Drone_ID].Rotate_Yaw(Rotation)
                    print(f'\t\t\tCW Result is: {Result}')
                    return (Result*"ok" + (not Result)*"error")
                except(TypeError or ValueError):
                    print("\t\t\tCW Type Error")
                    return "error"
        elif Command_Array[0] == "ccw":
            if Array_Len != 2:
                return "error"
            else:
                try:
                    Rotation = float(Command_Array[1])
                    Result = self.Tello[Drone_ID].Rotate_Yaw(-Rotation)
                    return (Result*"ok" + (not Result)*"error")
                except(TypeError or ValueError):
                    return "error"
        elif Command_Array[0] == "flip":
            return "ok"
        elif Command_Array[0] == "go":
            if Array_Len != 5:
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
            if Array_Len != 1:
                return "error"
            else:
                self.Tello[Drone_ID].Stop_Command()
                return "ok"
        elif Command_Array[0] == "curve":
            return "error"
        elif Command_Array[0] == "jump":
            return "error"

        elif Command_Array[0] == "speed":
            if Array_Len != 2:
                return "error"
            else:
                try:
                    Speed = float(Command_Array[1])
                    Result = self.Tello[Drone_ID].Set_Speed(Speed)
                    return (Result*"ok" + (not Result)*"error")
                except (TypeError or ValueError):
                    return "error"
        elif Command_Array[0] == "rc":
            if Array_Len != 5:
                return "error"
            else:
                try:
                    Speed_x = float(Command_Array[1])
                    Speed_y = float(Command_Array[2])
                    Speed_z = float(Command_Array[3])
                    Yaw = float(Command_Array[4])
                    #print(f'\t Speed is: {Speed_x}, {Speed_y}, {Speed_z}, {Yaw}')
                    Result = self.Tello[Drone_ID].RC(Speed_x, Speed_y, Speed_z, Yaw)
                    return (Result*"ok" + (not Result)*"error")
                except (TypeError or ValueError):
                    return "error"
        elif Command_Array[0] == "wifi":
            return "error"
        elif Command_Array[0] == "mon":
            return "error"
        elif Command_Array[0] == "moff":
            return "error"
        elif Command_Array[0] == "mdirection":
            return "error"
        elif Command_Array[0] == "ap":
            return "error"

        elif Command_Array[0] == "speed?":
            if Array_Len != 1:
                return "error"
            else:
                return self.Tello[Drone_ID].Read_Speed()
        elif Command_Array[0] == "battery?":
            if Array_Len != 1:
                return "error"
            else:
                return self.Tello[Drone_ID].Read_Battery()
        elif Command_Array[0] == "time?":
            if Array_Len != 1:
                return "error"
            else:
                return self.Tello[Drone_ID].Read_Time
        elif Command_Array[0] == "wifi?":
            return "error"
        elif Command_Array[0] == "sdk?":
            if Array_Len != 1:
                return "error"
            else:
                return "sdk 2.0"
        elif Command_Array[0] == "sn?":
            if Array_Len != 1:
                return "error"
            else:
                return self.Tello[Drone_ID].Serial_Number()

        else:
            return "error"

    def Add_Drone(self, Drone):
        self.Tello.append(Drone)
    '''
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
    '''

    def Send_State(self):
        print("Starting state sending")
        State_Port = 8890
        State_Socket = socket(AF_INET,SOCK_DGRAM)
        #State_Socket.bind((self.Host, State_Port))
        print("State socket ready")
        while self.Running:
            #print(f'\t\t\tConnected Address is: {self.Connected_Address}')
            if type(self.Connected_Address) == type("String"):
                for i in range(len(self.Tello)):
                    State_String = self.Tello[i].Get_State()
                    State_Socket.sendto(bytes(State_String, 'UTF-8'), (self.Connected_Address, State_Port))
            else:
                time.sleep(0.1)
        print("Ending state thread")
        State_Socket.close()

    def Sort_Command(self, Command: str, Socket:socket, SendTo):
        Command_Array = Command.split(": ")
        Result = None
        IP_Found = False
        print(f'\tCommand Array is: {Command_Array}')
        print(f'\tCommand Array 0 is: {Command_Array[0]}')
        for i in range(len(self.Tello)):
            #print(f'\tTello IP is : {self.Tello[i].IP_Address}')
            if self.Tello[i].IP_Address == Command_Array[0]:
                print(f"\tfound a drone in {self.Tello[i].IP_Address}")
                Result = self.Receive_Command(Command_Array[1], i)
                IP_Found = True
                break
            else:
                continue
        print(f'\t\tResult is: {Result}')
        if not IP_Found:
            Result = "error ip not found"
        elif Result == "command":
            print(f'SendTo is: {SendTo}')
            self.Connected_Address = SendTo[0]
            Result = "ok"
        elif Result == None:
            Result = "error"
        try:
            Socket.sendto(bytes(Result, 'UTF-8'), SendTo)
        except:
            print("Intercepted error")
            traceback.print_exc()


    def run(self):
        #Host = ''           # Symbolic name meaning all available interfaces
        #HOST = "192.168.56.1"
        Command_Port = 8889         # Arbitrary non-privileged port
        Buffer_Size = 1024  # Receive Buffer size (power of 2)

        Command_Socket = socket(AF_INET,SOCK_DGRAM) # IPv4, UDP
        Command_Socket.bind((self.Host, Command_Port))    # Bind sockect to the address
        Command_Socket.settimeout(1)

        print('UDP server running...')
        print('Listening for incoming connections in port '+str(Command_Port))
        print("Starting state thread")
        Sort_Thread = None
        State_Thread = threading.Thread(target=self.Send_State)
        State_Thread.start()
        print("State thread started")

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
            Sort_Thread = threading.Thread(target=self.Sort_Command, args=(r_str, Command_Socket, a,))
            Sort_Thread.start()
            #Result = self.Sort_Command(r_str)
            #Command_Socket.sendto(bytes(Result, 'UTF-8'), a)
            #print(f'\tReturned text: {Result}')

            #s.sendto(bytes(f'General Kenobi. Please stop contacting me. I got your message from {a[0]}','UTF-8'), a)
        print(f'\tOut of while loop')
        Command_Socket.close()
        if not Sort_Thread == None:
            Sort_Thread.join()
        State_Thread.join()


    def close(self):
        print("\tClosing thread")
        self.Running = False
        print('\tThread Closed')
