#import OLD_Camera
import Camera
import pygame
from math import sqrt
from time import time, sleep

# Every 65 pixel = 10 cm

class TelloDrone():
    # Arguments( Start x pos, Start y pos, Movement speed, the four keys that move the drone)
    def __init__(self, Start_x, Start_y, MaxSpeed = 1, Online_Mode = False, ip_Address = "0.0.0.0"):
        self.Pos = self.Pos_x, self.Pos_y, self.Pos_z = [Start_x, Start_y, 0]
        self.Last_Pos = self.Last_Pos_x, self.Last_Pos_y, self.Last_Pos_z = self.Pos
        self.Speed = self.Speed_x, self.Speed_y, self.Speed_z = [0,0,0]
        self.Acc = self.Acc_x, self.Acc_y, self.Acc_z = [0,0,0]
        self.Tot_Dist = self.Tot_Dist_x, self.Tot_Dist_y, self.Tot_Dist_z = [0,0,0]
        self.Yaw = 0
        self.Current_Speed = MaxSpeed
        self.Start_Time = time()

        self.Executing_Command = False
        self.Landed = True
        self.Video_Stream = False
        self.Emergency_Stop = False

        # Make a thread that accepts the commands

        # Drone's rectangle object. Used as the place to draw the drone, and as it's collision box.
        # The arguments are it's position and it's size
        self.Rect = pygame.Rect(Start_x - Camera.Offset_x, Start_y - Camera.Offset_y, 64, 64)
        # Load the image of the drone
        self.Image = pygame.image.load("Drone_Icon.png")
        # Set the booleans that activate with the movement keys
        self.Move_Left = False
        self.Move_Right = False
        self.Move_Down = False
        self.Move_Up = False

        self.Move_x = 0.0
        self.Move_y = 0.0
        # The max speed that the drone can move in the simulation
        self.MaxSpeed = MaxSpeed

        self.Control_Type = 0

    def Check_Max_Speed(self):
        return (sqrt(self.Speed_x**2 + self.Speed_y**2 + self.Speed_z**2) >= self.MaxSpeed)

    """
    Control Command Functions
    """

    def Landed_State(self, State):
        if self.Executing_Command or (State == self.Landed):
            return False
        else:
            # Executes once. No thread needed
            self.Executing_Command = True
            self.Speed_x = 0
            self.Speed_y = 0
            self.Speed_z = 0
            self.Acc_x = 0
            self.Acc_y = 0
            self.Acc_z = 0
            # Increases altitude by 50cm if drone is to take off
            # And if it did not take off already
            self.Pos_z += (5*65)*(not State)
            # Makes the altitude 0 if the drone is supposed to land
            self.Pos_z = self.Pos_z*(not State)
            self.Landed = State
            return True


    def Stream_OnOff(self, StreamMode):
        # Executes once, no thread needed
        if StreamMode == self.Video_Stream:
            return False
        else:
            self.Video_Stream = StreamMode
            return True

    def Emergency(self):
        # Function that completely stops the drone in its place
        # No gravity = No crash landing
        # No air resistance = Never stops moving
        # To avoid this the drone goes into landing and it just stops in its place
        self.Emergency_Stop = True
        self.Pos_z = 0
        self.Speed = [0,0,0]
        self.Landed = True

    def Stop_Command(self):
        self.Emergency_Stop = True
        self.Speed = [0,0,0]

    def Moveto(self, Amount_x = 0, Amount_y = 0, Amount_z = 0, Speed_Ratio = 0):
        # This function works for both the one directional command and the go command
        Amount_Sum = Amount_x+Amount_y+Amount_z
        if (self.Executing_Command
            or ((not(20<=abs(Amount_x)<=500)) and (Amount_x!=0))
            or ((not(20<=abs(Amount_y)<=500)) and (Amount_x!=0))
            or ((not(20<=abs(Amount_z)<=500)) and (Amount_x!=0))
            or ((not(10<=Speed_Ratio<=100)) and (Speed_Ratio!=0))
            or Amount_Sum == 0):
            return False
        else:
            # Moves by the certain amount between 20 and 500 in 3 directions
            Initial_Pos = self.Pos
            Speed = self.MaxSpeed*Speed_Ratio + self.Current_Speed*(Speed_Ratio==0)
            self.Speed_x = sqrt(Amount_x/Amount_Sum)*Speed
            self.Speed_y = sqrt(Amount_y/Amount_Sum)*Speed
            self.Speed_z = sqrt(Amount_z/Amount_Sum)*Speed
            """
            while ((self.Pos_x - Initial_Pos[0]) < Amount_x):
                self.Pos_x = Speed*(-1*(Amount_x < 0))
            while ((self.Pos_y - Initial_Pos[1]) < Amount_y):
                self.Pos_y = Speed*(-1*(Amount_y < 0))
            while ((self.Pos_z - Initial_Pos[2]) < Amount_z):
                self.Pos_z = Speed*(-1*(Amount_z < 0))
            """
            while ((((self.Pos_x - Initial_Pos[0]) < Amount_x) or
                    ((self.Pos_y - Initial_Pos[1]) < Amount_y) or
                    ((self.Pos_z - Initial_Pos[2]) < Amount_z)) and (not self.Emergency_Stop)):
                self.Pos_x = self.Speed_x*(-1*(Amount_x < 0))*((self.Pos_x - Initial_Pos[0]) < Amount_x)
                self.Pos_y = self.Speed_y*(-1*(Amount_y < 0))*((self.Pos_y - Initial_Pos[1]) < Amount_y)
                self.Pos_z = self.Speed_z*(-1*(Amount_z < 0))*((self.Pos_z - Initial_Pos[2]) < Amount_z)

            self.Pos_x = Initial_Pos[0] + Amount_x
            self.Pos_y = Initial_Pos[1] + Amount_y
            self.Pos_z = Initial_Pos[2] + Amount_z
            return True

    def Rotate_Yaw(self, Rotation, Speed = 1):
        if((not (1<=abs(Rotation)<=360)) and self.Executing_Command):
            return False
        else:
            Init_Yaw = self.Yaw
            while ((self.Yaw - Init_Yaw) < Rotation) and (not self.Emergency_Stop):
                self.Yaw += Speed*(Rotation>0) - Speed*(Rotation<0)
            self.Yaw = (Init_Yaw + Rotation) % 360

    def Curveto(self, Amount_x, Amount_y, Amount_z, Speed_Ratio):
        # This is so complex, will take so much time to make yey
        # Also needs a lot of math yey
        # Probably should not make this one
        pass

    """
    Set Commands Functions
    """

    def Set_Speed(self, Speed_Ratio):
        if not(10<=Speed_Ratio<=100):
            return False
        else:
            self.Current_Speed = self.MaxSpeed*Speed_Ratio
            return True

    def Remote_Controller(self):
        # Will think how to implement this later
        pass

    # Not all functions are here

    """
    Read Commands Functions
    """

    def Read_Speed(self):
        return str((self.Current_Speed/self.MaxSpeed))

    def Read_Battery(self):
        return "55"

    def Serial_Number(self):
        return str(self)

    # Not all functions are here

    """
    The receive command
    """

    def Receive_Command(self, Command: str):
        Command_Array = Command.split(" ")
        if len(Command_Array) == 0:
            return "error"
        elif Command_Array[0] == "command":
            # If it ever happens make this the thing that activates the drone
            return "ok"
        elif Command_Array[0] == "takeoff":
            Result = self.Landed_State(False)
            return (Result*"ok" + (not Result)*"error")
        elif Command_Array[0] == "land":
            Result = self.Landed_State(True)
            return (Result*"ok" + (not Result)*"error")
        elif Command_Array[0] == "streamon":
            Result = self.Stream_OnOff(True)
            return (Result*"ok" + (not Result)*"error")
        elif Command_Array[0] == "streamoff":
            Result = self.Stream_OnOff(False)
            return (Result*"ok" + (not Result)*"error")
        elif Command_Array[0] == "emergency":
            self.Emergency()
            return "ok"
        elif Command_Array[0] == "up":
            try:
                Distance = float(Command_Array[1])
                Result = self.Moveto(Amount_z = Distance)
                return (Result*"ok" + (not Result)*"error")
            except(TypeError):
                return "error"
        elif Command_Array[0] == "down":
            try:
                Distance = float(Command_Array[1])
                Result = self.Moveto(Amount_z = -Distance)
                return (Result*"ok" + (not Result)*"error")
            except(TypeError):
                return "error"
        elif Command_Array[0] == "left":
            try:
                Distance = float(Command_Array[1])
                Result = self.Moveto(Amount_x = -Distance)
                return (Result*"ok" + (not Result)*"error")
            except(TypeError):
                return "error"
        elif Command_Array[0] == "right":
            try:
                Distance = float(Command_Array[1])
                Result = self.Moveto(Amount_x = Distance)
                return (Result*"ok" + (not Result)*"error")
            except(TypeError):
                return "error"
        elif Command_Array[0] == "forward":
            try:
                Distance = float(Command_Array[1])
                Result = self.Moveto(Amount_y = -Distance)
                return (Result*"ok" + (not Result)*"error")
            except(TypeError):
                return "error"
        elif Command_Array[0] == "back":
            try:
                Distance = float(Command_Array[1])
                Result = self.Moveto(Amount_y = Distance)
                return (Result*"ok" + (not Result)*"error")
            except(TypeError):
                return "error"
        elif Command_Array[0] == "cw":
            try:
                Rotation = float(Command_Array[1])
                Result = self.Rotate_Yaw(Rotation)
                return (Result*"ok" + (not Result)*"error")
            except(TypeError):
                return "error"
        elif Command_Array[0] == "ccw":
            try:
                Rotation = float(Command_Array[1])
                Result = self.Rotate_Yaw(-Rotation)
                return (Result*"ok" + (not Result)*"error")
            except(TypeError):
                return "error"
        elif Command_Array[0] == "flip":
            return "ok"
        elif Command_Array[0] == "go":
            if len(Command_Array) > 5:
                return "error"
            else:
                try:
                    Distance_x = float(Command_Array[1])
                    Distance_y = float(Command_Array[2])
                    Distance_z = float(Command_Array[3])
                    Speed = float(Command_Array[4])
                    Result = self.Moveto(Distance_x,Distance_y,Distance_z,Speed)
                    return (Result*"ok" + (not Result)*"error")
                except(TypeError):
                    return "error"
        elif Command_Array[0] == "stop":
            self.Stop_Command()
            return "ok"
        elif Command_Array[0] == "curve":
            return "error"
        elif Command_Array[0] == "jump":
            return "error"

        elif Command_Array[0] == "speed":
            Speed = Command_Array[1]
            self.Set_Speed(Speed)
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
            return self.Read_Speed()
        elif Command_Array[0] == "battery?":
            return self.Read_Battery()
        elif Command_Array[0] == "time?":
            return str(time() - self.Start_Time)
        elif Command_Array[0] == "wifi?":
            pass
        elif Command_Array[0] == "sdk?":
            return "sdk 2.0"
        elif Command_Array[0] == "sn?":
            return self.Serial_Number()

        else:
            return "error"

    def Get_State(self):
        Dist = sqrt(self.Tot_Dist_x**2 + self.Tot_Dist_y**2 + self.Tot_Dist_z**2)
        Run_Time = time() - self.Start_Time
        State = f"pitch:0;roll:0;yaw:{self.Yaw};vgx:{self.Speed_x};vgy:{self.Speed_y};vgz:{self.Speed_z};templ:12.2;temph:14.2;tof:{Dist};h:{self.Pos_z};bat:55;baro:22;time:{Run_Time};agx:0;agy:0;agz:0;\r\n"
        return State

    # This function handles the movement of the drones by changing their position according to their speed
    # It checks the direction the drone is going and assigns the x and y speeds accordingly
    def Movement_Handler(self):
        if self.Control_Type == 1:
            self.Speed_x = self.Move_x*self.MaxSpeed
            self.Speed_y = self.Move_y*self.MaxSpeed
        else:
            self.Speed_x = ( self.Move_Right*(self.MaxSpeed - (self.Move_Up   | self.Move_Down)*self.MaxSpeed*((sqrt(2)-1)/sqrt(2)))
                           - self.Move_Left *(self.MaxSpeed - (self.Move_Up   | self.Move_Down)*self.MaxSpeed*((sqrt(2)-1)/sqrt(2))))
            self.Speed_y = ( self.Move_Down *(self.MaxSpeed - (self.Move_Right| self.Move_Left)*self.MaxSpeed*((sqrt(2)-1)/sqrt(2)))
                           - self.Move_Up   *(self.MaxSpeed - (self.Move_Right| self.Move_Left)*self.MaxSpeed*((sqrt(2)-1)/sqrt(2))))
        self.Pos_x += self.Speed_x
        self.Pos_y += self.Speed_y


    # This function updates the total flown distance
    def Update_Dist(self):
        self.Tot_Dist_x += abs(self.Pos_x - self.Last_Pos_x)
        self.Tot_Dist_y += abs(self.Pos_y - self.Last_Pos_y)
        self.Tot_Dist_z += abs(self.Pos_z - self.Last_Pos_z)
    # This function updates the rectangle's position to match the drone's position
    def Update_Rect(self):
        self.Rect.topleft = self.Pos_x - Camera.Offset_x, self.Pos_y - Camera.Offset_y
        self.Update_Dist()


    # Final collision algoirthm. Argument(The rectangle to check if the drone collided with)
    def Check_Collision(self, Rect):
        # Checks if the rectangles collided horizontally
        self.Update_Rect()                          # Update this drone's rectangle position
        Collision = self.Rect.colliderect(Rect)     # Check if it collides with the argument rectangle
        self.Pos_x -= self.Speed_x * Collision      # Go back to the previous position horizontally if collided
        # Checks if the rectangles collided vertically
        self.Update_Rect()                          # Update this drone's rectangle to the new position
        Collision = self.Rect.colliderect(Rect)     # Check if it collides with the argument rectangle
        self.Pos_x += self.Speed_x * Collision      # Negate the horizontal back movemenet if collided
        self.Pos_y -= self.Speed_y * Collision      # Go back to the previous position vertically if collided
        # Checks if the rectangles collided both horizontally and vertically
        self.Update_Rect()                          # Update this drone's rectangle to the new position
        Collision = self.Rect.colliderect(Rect)     # Check if it collides with the argument rectangle
        self.Pos_x -= self.Speed_x * Collision      # Go back to the previous position horizontally again if collided

'''
Command = "streamon 22"
Command_Split = Command.split(" ")
print(Command)
print(Command_Split)
print(Command_Split[0] == "streamon")
'''
'''
Result = True
Outcome = Result*"ok" + (not Result)*"error"
print(Result)
print(Outcome)
dronee = TelloDrone(50,0)
print(dronee.Get_State())
sleep(5)
print(dronee.Get_State())
'''
