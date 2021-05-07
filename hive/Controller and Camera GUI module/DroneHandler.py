#import djitellopy as dji
import Loc_djitellopy as dji
import threading
import pygame

class DroneHandler:

    def __init__(self, Tello_IP = "192.168.10.1"):
        self.IP_Address = Tello_IP
        print(f'IP Address is: {Tello_IP}, {self.IP_Address}')
        self.Drone = dji.Tello(self.IP_Address)

        self.Controllable = False
        self.ControllerMode = False
        self.RC_Mode = True
        self.Move_Speed = 50
        self.Yaw_Speed = 80
        self.Drone.connect()
        self.Drone.streamon()
        self.Drone.send_rc_control(0,0,0,0)
        self.Frame = self.Drone.get_frame_read()
        # Dictionary with keyboard controls
        self.Control_Dict = {"land":    pygame.K_SPACE, "takeoff":  pygame.K_SPACE,
                             "up":      pygame.K_UP,    "down":     pygame.K_DOWN,
                             "cw":      pygame.K_RIGHT, "ccw":      pygame.K_LEFT,
                             "forward": pygame.K_w,     "backward": pygame.K_s,
                             "right":   pygame.K_d,     "left":     pygame.K_a,
                             "flipf":   pygame.K_KP8,   "flipb":    pygame.K_KP5,
                             "flipr":   pygame.K_KP6,   "flipl":    pygame.K_KP4,
                             "rc":      pygame.K_r,
                             "stop":    pygame.K_p,     "emergency":pygame.K_o     }


    # The control handler that takes the input and sends commands to the drone
    # This is currently mapped to the DS4, so I don't know if it works with other controllers
    # It can be mapped to a keyboard too, but that is not yet done
    # Takes the keyboard input and the controller input as arguments
    def ControlHandler(self, KeyList, EventList, CD: dict):
        if self.Controllable:
            if self.ControllerMode:
                for e in EventList:
                    if e.type == pygame.JOYBUTTONDOWN:
                        # The X button lands or takes off the drone (Depending on if the drone is flying or not)
                        if CD.get("Button0"):
                            if self.Drone.is_flying:
                                Land_Thread = threading.Thread(target=self.Drone.land)
                                Land_Thread.start()
                                #self.Drone.land()
                            else:
                                Takeoff_Thread = threading.Thread(target=self.Drone.takeoff)
                                Takeoff_Thread.start()
                                #self.Drone.takeoff()
                        # The circle button switches RC_Mode on or off
                        elif CD.get("Button1"):
                            self.RC_Mode = not self.RC_Mode
                            self.Drone.send_rc_control(0,0,0,0)
                        # The square button sends the stop command that is supposed to let the drone hover in its place
                        elif CD.get("Button2"):
                            Stop_Command_Thread = threading.Thread(target=self.Drone.send_control_command, args=("stop",))
                            Stop_Command_Thread.start()
                            #self.Drone.send_control_command("stop")
                        # The triangle button sends the emergency command that stops the propellers
                        elif CD.get("Button3"):
                            Emergency_Thread = threading.Thread(target=self.Drone.emergency)
                            Emergency_Thread.start()
                            #self.Drone.emergency()
                        """ Dangerous :P
                        # The d-pad up does a forward flip (Not yet tested)
                        elif CD.get("Button11"):
                            self.Drone.flip_forward()
                        # The d-pad down does a back flip (Not yet tested)
                        elif CD.get("Button12"):
                            self.Drone.flip_back()
                        # The d-pad left does a left flip (Not yet tested)
                        elif CD.get("Button13"):
                            self.Drone.flip_left()
                        # The d-pad right does a right flip (Not yet tested)
                        elif CD.get("Button14"):
                            self.Drone.flip_right()
                        """
                # Get the values of each axis
                Axis0 = CD.get("Axis0")                                     # Left analog stick Right-Left
                Axis1 = CD.get("Axis1")                                     # Left analog stick Up-Down
                Axis2 = CD.get("Axis2")                                     # Right analog stick Right-Left
                Axis3 = CD.get("Axis3")                                     # Right analog stick Up-Down
                # Run the RC command if RC mode is on and the drone is flying
                try:
                    if self.RC_Mode and self.Drone.is_flying:
                        # Move the RC command in half speed for movement and 80% speed for rotation
                        # The checks if the axis are over a 0.2 deadzone, so that stick drifting does not affect the drone
                        Front = -int(self.Move_Speed*Axis1)*(abs(Axis1)>0.2)
                        Side =   int(self.Move_Speed*Axis0)*(abs(Axis0)>0.2)
                        Up =    -int(self.Move_Speed*Axis3)*(abs(Axis3)>0.2)
                        Yaw =    int(self.Yaw_Speed*Axis2)*(abs(Axis2)>0.2)
                        self.Drone.send_rc_control(Side,Front,Up,Yaw)
                        return
                # TypeError occurs when the input dictionary does not have a value for the axis and gives none instead
                except TypeError:
                    print("Type error detected")
                    return
            else:
                for e in EventList:
                    if e.type == pygame.KEYDOWN:
                        #print(f'Takeoff button state is: {KeyList[self.Control_Dict.get("takeoff")]}')
                        # The land button lands or takes off the drone (Depending on if the drone is flying or not)
                        if KeyList[self.Control_Dict.get("land")]:
                            if self.Drone.is_flying:
                                Land_Thread = threading.Thread(target=self.Drone.land)
                                Land_Thread.start()
                                #self.Drone.land()
                            else:
                                Takeoff_Thread = threading.Thread(target=self.Drone.takeoff)
                                Takeoff_Thread.start()
                                #self.Drone.takeoff()
                        #if KeyList[self.Control_Dict.get("takeoff")]:
                        #    if not self.Drone.is_flying:
                        #        self.Drone.takeoff()
                        # The rc button switches RC_Mode on or off
                        elif KeyList[self.Control_Dict.get("rc")]:
                            self.RC_Mode = not self.RC_Mode
                            #RC_Mode_Thread = threading.Thread(target=self.Drone.send_rc_control, args=(0,0,0,0,))
                            #RC_Mode_Thread.start()
                            self.Drone.send_rc_control(0,0,0,0)
                        # The stop button sends the stop command that is supposed to let the drone hover in its place
                        elif KeyList[self.Control_Dict.get("stop")]:
                            Stop_Command_Thread = threading.Thread(target=self.Drone.send_control_command, args=("stop",))
                            Stop_Command_Thread.start()
                            #self.Drone.send_control_command("stop")
                        # The emergency button sends the emergency command that stops the propellers
                        elif KeyList[self.Control_Dict.get("emergency")]:
                            Emergency_Thread = threading.Thread(target=self.Drone.emergency)
                            Emergency_Thread.start()
                            #self.Drone.emergency()
                        """ Dangerous :P
                        # The d-pad up does a forward flip (Not yet tested)
                        elif KeyList[self.Control_Dict.get("flipf")]:
                            self.Drone.flip_forward()
                        # The d-pad down does a back flip (Not yet tested)
                        elif KeyList[self.Control_Dict.get("flipb")]:
                            self.Drone.flip_back()
                        # The d-pad left does a left flip (Not yet tested)
                        elif KeyList[self.Control_Dict.get("flipl")]:
                            self.Drone.flip_left()
                        # The d-pad right does a right flip (Not yet tested)
                        elif KeyList[self.Control_Dict.get("flipr")]:
                            self.Drone.flip_right()
                        """
                # Run the RC command if RC mode is on and the drone is flying
                try:
                    if self.RC_Mode and self.Drone.is_flying:
                        # Move the RC command in half speed for movement and 80% speed for rotation
                        # The checks if the axis are over a 0.2 deadzone, so that stick drifting does not affect the drone
                        Front = (self.Move_Speed*KeyList[self.Control_Dict.get("forward")])-(self.Move_Speed*KeyList[self.Control_Dict.get("backward")])
                        Side =  (self.Move_Speed*KeyList[self.Control_Dict.get("right")])  -(self.Move_Speed*KeyList[self.Control_Dict.get("left")])
                        Up =    (self.Move_Speed*KeyList[self.Control_Dict.get("up")])     -(self.Move_Speed*KeyList[self.Control_Dict.get("down")])
                        Yaw =   (self.Yaw_Speed*KeyList[self.Control_Dict.get("cw")])     -(self.Yaw_Speed*KeyList[self.Control_Dict.get("ccw")])
                        self.Drone.send_rc_control(Side,Front,Up,Yaw)
                        return
                # TypeError occurs when the input dictionary does not have a value for the axis and gives none instead
                except TypeError:
                    print("Type error detected")
                    return


    # This command sets the controller mode (Intended to switch between controller and keyboard controls)
    def SetControllerMode(self, State):
        self.ControllerMode = State
    # Give the frame from the drone
    def GetFrame(self):
        return self.Frame.frame
    def GetFrameFPS(self):
        return self.Frame.FPS
    # Give the battery status from the drone
    def GetBattery(self):
        return self.Drone.get_battery()
    # Give the speed of the drone (Don't think it actually works. It gives an exception)
    def GetSpeed(self):
        return self.Drone.query_speed()
    # Give the flying state of the drone
    def GetFlying(self):
        return self.Drone.is_flying
    # Send an emergency command to the drone
    def Emergency(self, Stop:bool = False):
        if Stop:
            #self.Drone.send_control_command("stop")
            Stop_Command_Thread = threading.Thread(target=self.Drone.send_control_command, args=("stop",))
            Stop_Command_Thread.start()
        else:
            #self.Drone.emergency()
            Emergency_Thread = threading.Thread(target=self.Drone.emergency)
            Emergency_Thread.start()
    # Connect the drone to a network with a given name and password
    def Connect_Network(self, SSID, Pass):
        self.Drone.connect_to_wifi(SSID, Pass)
        Wifi_Connect_Thread = threading.Thread(target=self.Drone.connect_to_wifi, args=("ssid", "pass",))
    # The command that is used when the stop button is pressed. Currently only lands the drone
    def Stop_Button_Command(self):
        if self.Drone.is_flying:
            Land_Thread = threading.Thread(target=self.Drone.land)
            Land_Thread.start()
            #self.Drone.land()
        #self.Stop()
    # Stop the drone
    def Stop(self):
        End_Thread = threading.Thread(target=self.Drone.end)
        End_Thread.start()
        #self.Drone.end()
