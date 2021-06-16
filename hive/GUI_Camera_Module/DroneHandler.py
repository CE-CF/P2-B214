import threading
import traceback

import pygame
import cv2
import numpy as np
from .BackgroundFrameRead import BackgroundFrameRead

class DroneHandler:

    # Provides the local IP and Port needed for background frame read class
    def get_udp_video_address(self, ID:str) -> str:
        LastIP = ID
        while len(LastIP) < 3:
            LastIP = '0' + LastIP
        RecvPort = int("22" + LastIP)
        address_schema = 'udp://@{ip}:{port}'
        address = address_schema.format(ip='127.0.0.1', port=RecvPort)
        print(f'Sent address is: {address}')
        return address

    # Creates the background frame read of the drone. Called in a new thread.
    def CreateBFR(self):
        BFR_IP = self.get_udp_video_address(str(self.ID))
        print(f"Starting BFR: {self.ID}")
        self.Frame = BackgroundFrameRead(BFR_IP, self.ID)
        print(f"BFR Started: {self.ID}")

    def __init__(self, Sender,  Tello_ID = 0):
        self.ID = Tello_ID
        self.Sender = Sender
        self.Command_Counter = 1
        self.Controllable = False
        self.ControllerMode = False
        self.RC_Mode = False
        self.Move_Speed = 50
        self.Yaw_Speed = 80
        self.Send_Sequence = 0
        self.Battery = 0
        BFRThread = threading.Thread(target=self.CreateBFR)
        BFRThread.start()
        # Dictionary with keyboard controls
        self.Control_Dict = {"land":    pygame.K_b,     "takeoff":  pygame.K_SPACE,
                             "up":      pygame.K_UP,    "down":     pygame.K_DOWN,
                             "cw":      pygame.K_RIGHT, "ccw":      pygame.K_LEFT,
                             "forward": pygame.K_w,     "backward": pygame.K_s,
                             "right":   pygame.K_d,     "left":     pygame.K_a,
                             "rc":      pygame.K_r,
                             "stop":    pygame.K_p,     "emergency":pygame.K_o          }


    # The control handler that takes the input and sends commands to the drone
    # This is currently mapped to the DS4, so I don't know if it works with other controllers
    # It is mapped to work with a keyboard too
    # Takes the keyboard input and the controller input as arguments
    def ControlHandler(self, KeyList, EventList, CD: dict):
        if self.Controllable:
            if self.ControllerMode:
                for e in EventList:
                    if e.type == pygame.JOYBUTTONDOWN:
                        # The X button lands or takes off the drone (Depending on if the drone is flying or not)
                        if CD.get("Button10"):
                            self.Sender.send_udp(self.ID, 0, self.Command_Counter, b"land")
                            self.Command_Counter+=1
                        elif CD.get("Button0"):
                            self.Sender.send_udp(self.ID, 0, self.Command_Counter, b"takeoff")
                            self.Command_Counter+=1
                        # The circle button switches RC_Mode on or off
                        elif CD.get("Button1"):
                            self.RC_Mode = not self.RC_Mode
                            self.Sender.send_udp(self.ID, 0, self.Command_Counter, b"rc 0 0 0 0")
                            self.Command_Counter+=1
                        # The square button sends the stop command that is supposed to let the drone hover in its place
                        elif CD.get("Button2"):
                            self.Sender.send_udp(self.ID, 0, self.Command_Counter, b"stop")
                            self.Command_Counter+=1
                        # The triangle button sends the emergency command that stops the propellers
                        elif CD.get("Button3"):
                            self.Sender.send_udp(self.ID, 0, self.Command_Counter, b"emergency")
                            self.Command_Counter+=1
                # Get the values of each axis
                Axis0 = CD.get("Axis0")                                     # Left analog stick Right-Left
                Axis1 = CD.get("Axis1")                                     # Left analog stick Up-Down
                Axis2 = CD.get("Axis2")                                     # Right analog stick Right-Left
                Axis3 = CD.get("Axis3")                                     # Right analog stick Up-Down
                # Run the RC command if RC mode is on and the drone is flying
                try:
                    #if self.RC_Mode and self.Drone.is_flying:
                    if self.RC_Mode:
                        # Move the RC command in half speed for movement and 80% speed for rotation
                        # The checks if the axis are over a 0.2 deadzone, so that stick drifting does not affect the drone
                        Front = -int(self.Move_Speed*Axis1)*(abs(Axis1)>0.2)
                        Side =   int(self.Move_Speed*Axis0)*(abs(Axis0)>0.2)
                        Up =    -int(self.Move_Speed*Axis3)*(abs(Axis3)>0.2)
                        Yaw =    int(self.Yaw_Speed*Axis2)*(abs(Axis2)>0.2)
                        self.Sender.send_udp(self.ID, 0, self.Command_Counter, bytes(f'rc {Side} {Front} {Up} {Yaw}', "UTF-8"))
                        self.Command_Counter+=1
                        return
                # TypeError occurs when the input dictionary does not have a value for the axis and gives none instead
                except TypeError:
                    print("Controller RC handling: Type error detected")
                    return
            else:
                for e in EventList:
                    if e.type == pygame.KEYDOWN:
                        #print(f'Takeoff button state is: {KeyList[self.Control_Dict.get("takeoff")]}')
                        # The land button lands or takes off the drone (Depending on if the drone is flying or not)
                        if KeyList[self.Control_Dict.get("land")]:
                            self.Sender.send_udp(self.ID, 0, self.Command_Counter, b"land")
                            self.Command_Counter+=1
                        elif KeyList[self.Control_Dict.get("takeoff")]:
                            self.Sender.send_udp(self.ID, 0, self.Command_Counter, b"takeoff")
                            self.Command_Counter+=1
                        elif KeyList[self.Control_Dict.get("rc")]:
                            self.RC_Mode = not self.RC_Mode
                            self.Sender.send_udp(self.ID, 0, self.Command_Counter, b"rc 0 0 0 0")
                            self.Command_Counter+=1
                        # The stop button sends the stop command that is supposed to let the drone hover in its place
                        elif KeyList[self.Control_Dict.get("stop")]:
                            self.Sender.send_udp(self.ID, 0, self.Command_Counter, b"stop")
                            self.Command_Counter+=1
                        # The emergency button sends the emergency command that stops the propellers
                        elif KeyList[self.Control_Dict.get("emergency")]:
                            self.Sender.send_udp(self.ID, 0, self.Command_Counter, b"emergency")
                            self.Command_Counter+=1
                # Run the RC command if RC mode is on and the drone is flying
                try:
                    #if self.RC_Mode and self.Drone.is_flying:
                    if self.RC_Mode:
                        # Move the RC command in half speed for movement and 80% speed for rotation
                        # The checks if the axis are over a 0.2 deadzone, so that stick drifting does not affect the drone
                        Front = (self.Move_Speed*KeyList[self.Control_Dict.get("forward")])-(self.Move_Speed*KeyList[self.Control_Dict.get("backward")])
                        Side =  (self.Move_Speed*KeyList[self.Control_Dict.get("right")])  -(self.Move_Speed*KeyList[self.Control_Dict.get("left")])
                        Up =    (self.Move_Speed*KeyList[self.Control_Dict.get("up")])     -(self.Move_Speed*KeyList[self.Control_Dict.get("down")])
                        Yaw =   (self.Yaw_Speed*KeyList[self.Control_Dict.get("cw")])     -(self.Yaw_Speed*KeyList[self.Control_Dict.get("ccw")])
                        self.Sender.send_udp(self.ID, 0, self.Command_Counter, bytes(f'rc {Side} {Front} {Up} {Yaw}', "UTF-8"))
                        self.Command_Counter+=1
                        return
                # TypeError occurs when the input dictionary does not have a value for the axis and gives none instead
                except TypeError:
                    print("Keyboard RC Handler: Type error detected")
                    return


    # This command sets the controller mode (Intended to switch between controller and keyboard controls)
    def SetControllerMode(self, State):
        self.ControllerMode = State

    # Give the frame from the drone
    def GetFrame(self):
        try:
            if type(self.Frame.frame) == type(None):
                return self.Frame.PlaceholderFrame
            else:
                return self.Frame.frame
        except AttributeError:
            #print(f'GetFrame attribute error')
            #traceback.print_exc()
            f = open('hive/GUI_Camera_Module/NoFrame.jpg', 'rb')
            image_bytes = f.read()
            f.close()
            return cv2.imdecode(np.frombuffer(image_bytes, np.uint8), -1)

    def GetFrameFPS(self):
        try:
            return self.Frame.FPS
        except AttributeError:
            return 0

    # Give the battery status from the drone
    def GetBattery(self):
    #    return self.Drone.get_battery()
        return int(self.Battery)

    # Give the flying state of the drone
    def GetFlying(self):
        #return self.Drone.is_flying
        return False

    # Send an emergency command to the drone
    def Emergency(self, Stop:bool = False):
        if Stop:
            self.Sender.send_udp(self.ID, 0, self.Command_Counter, b"stop")
            self.Command_Counter+=1
        else:
            self.Sender.send_udp(self.ID, 0, self.Command_Counter, b"emergency")
            self.Command_Counter+=1

    # The command that is used when the stop button is pressed. Currently only lands the drone
    def Stop_Button_Command(self):
        self.Sender.send_udp(self.ID, 0, self.Command_Counter, b"land")
        #self.Sender.send_udp(self.ID, 0, self.Command_Counter, b"stop")
        self.Command_Counter+=1

    # Stop the drone
    def Stop(self):
        try:
            self.Frame.stop()
        except AttributeError:
            return

