import djitellopy as dji

class DroneHandler:

    def __init__(self, Swarm = False):
        # Swarm capabilities not yet made or tested
        if not Swarm:
            self.Drone = dji.Tello()

        self.ControllerMode = False
        self.RC_Mode = True
        self.Drone.connect()
        self.Drone.streamon()
        self.Frame = self.Drone.get_frame_read()

    # The control handler that takes the input and sends commands to the drone
    # This is currently mapped to the DS4, so I don't know if it works with other controllers
    # It can be mapped to a keyboard too, but that is not yet done
    # Takes the keyboard input and the controller input as arguments
    def ControlHandler(self, KeyList, CD: dict):
        if self.ControllerMode:
            # Get the values of each axis
            Axis0 = CD.get("Axis0")                                     # Left analog stick Right-Left
            Axis1 = CD.get("Axis1")                                     # Left analog stick Up-Down
            Axis2 = CD.get("Axis2")                                     # Right analog stick Right-Left
            Axis3 = CD.get("Axis3")                                     # Right analog stick Up-Down
            # The X button lands or takes off the drone (Depending on if the drone is flying or not)
            if CD.get("Button0"):
                if self.Drone.is_flying:
                    self.Drone.land()
                else:
                    self.Drone.takeoff()
            # The circle button switches RC_Mode on or off
            elif CD.get("Button1"):
                self.RC_Mode = not self.RC_Mode
                self.Drone.send_rc_control(0,0,0,0)
            # The square button sends the stop command that is supposed to let the drone hover in its place
            elif CD.get("Button2"):
                self.Drone.send_control_command("stop")
            # The triangle button sends the emergency command that stops the propellers
            elif CD.get("Button3"):
                self.Drone.emergency()
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
            # Run the RC command if RC mode is on and the drone is flying
            try:
                if self.RC_Mode and self.Drone.is_flying:
                    # Move the RC command in half speed for movement and 80% speed for rotation
                    # The checks if the axis are over a 0.2 deadzone, so that stick drifting does not affect the drone
                    Front = -int(50*Axis1)*(abs(Axis1)>0.2)
                    Side =   int(50*Axis0)*(abs(Axis0)>0.2)
                    Up =    -int(50*Axis3)*(abs(Axis3)>0.2)
                    Yaw =    int(80*Axis2)*(abs(Axis2)>0.2)
                    self.Drone.send_rc_control(Side,Front,Up,Yaw)
            # TypeError occurs when the input dictionary does not have a value for the axis and gives none instead
            except TypeError:
                print("Type error detected")
                return
        else:
            return
    # This command sets the controller mode (Intended to switch between controller and keyboard controls)
    def SetControllerMode(self, State):
        self.ControllerMode = State
    # Give the frame from the drone
    def GetFrame(self):
        return self.Frame.frame
    # Give the battery status from the drone
    def GetBattery(self):
        return self.Drone.get_battery()
    # Stop the drone
    def Stop(self):
        self.Drone.end()
