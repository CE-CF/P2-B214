#import OLD_Camera
import Camera
import pygame
import threading
import Global_Constants as GC
import Tello_Communication as TC
from math import sqrt, cos, sin, pi
from time import time, sleep

# Every 65 pixel = 10 cm

class TelloDrone():
    # Arguments( Start x pos, Start y pos, Movement speed, the four keys that move the drone)
    def __init__(self, Start_x, Start_y, MaxSpeed = 65, Online_Mode = False, IP_Address = "0.0.0.0"):
        self.Pos = self.Pos_x, self.Pos_y, self.Pos_z = [Start_x, Start_y, 0]
        self.Last_Pos = self.Last_Pos_x, self.Last_Pos_y, self.Last_Pos_z = self.Pos
        self.Speed = self.Speed_x, self.Speed_y, self.Speed_z = [0,0,0]
        self.Acc = self.Acc_x, self.Acc_y, self.Acc_z = [0,0,0]
        self.Tot_Dist = self.Tot_Dist_x, self.Tot_Dist_y, self.Tot_Dist_z = [0,0,0]
        self.Yaw = 0
        self.Current_Speed = MaxSpeed
        self.Start_Time = time()
        #self.Command_Center = TC.Tello_Communication(self)
        self.IP_Address = IP_Address

        self.Executing_Command = False
        self.Landed = True
        self.Video_Stream = False
        self.Emergency_Stop = False

        # Make a thread that accepts the commands

        # Drone's rectangle object. Used as the place to draw the drone, and as it's collision box.
        # The arguments are it's position and it's size
        self.Rect = pygame.Rect(Start_x - Camera.Offset_x, Start_y - Camera.Offset_y, 64, 64)
        # Load the image of the drone
        self.Init_Image = pygame.image.load("Drone_Icon.png")
        self.Image = self.Init_Image
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
            self.Executing_Command = False
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
        self.Speed_x, self.Speed_y, self.Speed_z = [0,0,0]
        self.Landed = True
        sleep(1)
        self.Emergency_Stop = False

    def Stop_Command(self):
        self.Emergency_Stop = True
        self.Speed_x, self.Speed_y, self.Speed_z = [0,0,0]
        sleep(1)
        self.Emergency_Stop = False
    """
    def Moveto(self, Amount_x = 0, Amount_y = 0, Amount_z = 0, Speed_Ratio = 10):
        # This function works for both the one directional command and the go command
        print("Go command started")
        print(f"Amount to move is: {Amount_x}, {Amount_y}, {Amount_z}")
        Amount_Sum = abs(Amount_x) + abs(Amount_y) + abs(Amount_z)
        if (self.Executing_Command or self.Landed
            or ((not(20<=abs(Amount_x)<=500)) and (Amount_x!=0))
            or ((not(20<=abs(Amount_y)<=500)) and (Amount_y!=0))
            or ((not(20<=abs(Amount_z)<=500)) and (Amount_z!=0))
            or ((not(10<=Speed_Ratio<=100)) and (Speed_Ratio!=0))
            or Amount_Sum == 0):
            print("go command out of range")
            return False
        else:
            # Moves by the certain amount between 20 and 500 in 3 directions
            print("Go command not out of range")
            self.Executing_Command = True
            Initial_Pos = [self.Pos_x, self.Pos_y, self.Pos_z]
            Speed = 0.001
            #Speed = self.MaxSpeed*(Speed_Ratio/100) + self.Current_Speed*(Speed_Ratio==0)
            self.Speed_x = sqrt(abs(Amount_x)/Amount_Sum)*Speed*(1-2*(Amount_x<0))
            self.Speed_y = sqrt(abs(Amount_y)/Amount_Sum)*Speed*(1-2*(Amount_y<0))
            self.Speed_z = sqrt(abs(Amount_z)/Amount_Sum)*Speed*(1-2*(Amount_z<0))
            print("go command starting while loop")
            while (((abs(self.Pos_x - Initial_Pos[0]) < abs(Amount_x)) or
                    (abs(self.Pos_y - Initial_Pos[1]) < abs(Amount_y)) or
                    (abs(self.Pos_z - Initial_Pos[2]) < abs(Amount_z)))):
                #print(self.Speed)
                print(f'{self.Speed_x}, {self.Speed_y}, {self.Speed_z}')
                if self.Emergency_Stop:
                    self.Executing_Command = False
                    return False
                else:
                    self.Pos_x += self.Speed_x*(abs(self.Pos_x - Initial_Pos[0]) < abs(Amount_x))
                    self.Pos_y += self.Speed_y*(abs(self.Pos_y - Initial_Pos[1]) < abs(Amount_y))
                    self.Pos_z += self.Speed_z*(abs(self.Pos_z - Initial_Pos[2]) < abs(Amount_z))
            print("Go command exit while loop")
            self.Pos_x = Initial_Pos[0] + Amount_x
            self.Pos_y = Initial_Pos[1] + Amount_y
            self.Pos_z = Initial_Pos[2] + Amount_z
            self.Executing_Command = False
            return True
    """

    def Moveto(self, Amount_RL = 0, Amount_FB = 0, Amount_z = 0, Speed_Ratio = 10):
        # This function works for both the one directional command and the go command
        Amount_Sum = abs(Amount_RL) + abs(Amount_FB) + abs(Amount_z)
        if (self.Executing_Command or self.Landed
            or ((not(20<=abs(Amount_RL)<=500)) and (Amount_RL!=0))
            or ((not(20<=abs(Amount_FB)<=500)) and (Amount_FB!=0))
            or ((not(20<=abs(Amount_z)<=500)) and (Amount_z!=0))
            or ((not(10<=Speed_Ratio<=100)) and (Speed_Ratio!=0))
            or Amount_Sum == 0):
            print("go command out of range")
            return False
        else:
            # Moves by the certain amount between 20 and 500 in 3 directions
            self.Executing_Command = True
            Initial_Pos = [self.Pos_x, self.Pos_y, self.Pos_z]
            #Speed = 0.01*(Speed_Ratio/100) + 0.01*(Speed_Ratio==0)
            Speed = self.MaxSpeed*(Speed_Ratio/100) + self.Current_Speed*(Speed_Ratio==0)
            """
            Speed_Neutralizer = (Amount_RL+Amount_FB)*(cos(self.Yaw)**2)+(Amount_RL-Amount_FB)*(sin(self.Yaw)**2)+Amount_z
            self.Speed_x = (sqrt(abs(Amount_RL)/Speed_Neutralizer)*Speed*(1-2*(Amount_RL<0))*cos(self.Yaw*(pi/180))-
                            sqrt(abs(Amount_FB)/Speed_Neutralizer)*Speed*(1-2*(Amount_FB>0))*sin(self.Yaw*(pi/180)))
            self.Speed_x *= abs(self.Speed_x)>0.0000001
            self.Speed_y = (sqrt(abs(Amount_FB)/Speed_Neutralizer)*Speed*(1-2*(Amount_FB>0))*cos(self.Yaw*(pi/180))+
                            sqrt(abs(Amount_RL)/Speed_Neutralizer)*Speed*(1-2*(Amount_RL<0))*sin(self.Yaw*(pi/180)))
            self.Speed_y *= abs(self.Speed_y)>0.0000001
            self.Speed_z = sqrt(abs(Amount_z)/Speed_Neutralizer)*Speed*(1-2*(Amount_z<0))
            Target_x = Amount_FB*sin(self.Yaw*(pi/180)) + Amount_RL*cos(self.Yaw*(pi/180))
            Target_x *= abs(Target_x)>0.0000001
            Target_y = -(Amount_FB*cos(self.Yaw*(pi/180))) + Amount_RL*sin(self.Yaw*(pi/180))
            Target_y *= abs(Target_y)>0.0000001
            """
            Target_x = Amount_FB*sin(self.Yaw*(pi/180)) + Amount_RL*cos(self.Yaw*(pi/180))
            Target_x *= abs(Target_x)>0.0000001
            Target_y = Amount_RL*sin(self.Yaw*(pi/180)) - (Amount_FB*cos(self.Yaw*(pi/180)))
            Target_y *= abs(Target_y)>0.0000001
            New_Sum = abs(Target_x) + abs(Target_y) + abs(Amount_z)
            Unit_Vector_Converter = sqrt((Target_x**2 + Target_y**2 + Amount_z**2))/New_Sum
            Speed_Neutralizer = New_Sum*Unit_Vector_Converter
            self.Speed_x = (abs(Target_x)/Speed_Neutralizer)*Speed*(1-2*(Target_x<0))
            self.Speed_y = (abs(Target_y)/Speed_Neutralizer)*Speed*(1-2*(Target_y<0))
            self.Speed_z = (abs(Amount_z)/Speed_Neutralizer)*Speed*(1-2*(Amount_z<0))
            print(f'{self.Speed_x}, {self.Speed_y}, {self.Speed_z}')
            while (((abs(self.Pos_x - Initial_Pos[0]) < abs(Target_x)) or
                    (abs(self.Pos_y - Initial_Pos[1]) < abs(Target_y)) or
                    (abs(self.Pos_z - Initial_Pos[2]) < abs(Amount_z)))):
                #print(self.Speed)
                #print(f'{self.Speed_x}, {self.Speed_y}, {self.Speed_z}')
                if self.Emergency_Stop:
                    self.Executing_Command = False
                    return False
                else:
                    self.Pos_x += self.Speed_x*(abs(self.Pos_x - Initial_Pos[0]) < abs(Target_x))
                    self.Pos_y += self.Speed_y*(abs(self.Pos_y - Initial_Pos[1]) < abs(Target_y))
                    self.Pos_z += self.Speed_z*(abs(self.Pos_z - Initial_Pos[2]) < abs(Amount_z))

                    sleep(1/GC.FPS)
            print("Go command exit while loop")
            print(f'Target x is: {Target_x}')
            self.Pos_x = Initial_Pos[0] + Target_x
            print(f'Target y is: {Target_y}')
            self.Pos_y = Initial_Pos[1] + Target_y
            self.Pos_z = Initial_Pos[2] + Amount_z
            self.Speed_x, self.Speed_y, self.Speed_z = 0,0,0
            self.Executing_Command = False
            return True

    def Rotate_Yaw(self, Rotation, Speed = 1):
        if((not (1<=abs(Rotation)<=360)) or (self.Executing_Command or self.Landed)):
            print("Rotation failed")
            return False
        else:
            self.Executing_Command = True
            Init_Yaw = self.Yaw
            while (abs(self.Yaw - Init_Yaw) < abs(Rotation)):
                if self.Emergency_Stop:
                    self.Executing_Command = False
                    return False
                self.Yaw += Speed*(1-2*(Rotation<0))
                sleep(1/GC.FPS)
            self.Yaw = (Init_Yaw + Rotation) % 360
            #Init_Image = self.Image
            #Init_Rect = self.Rect
            #Rot_Image = pygame.transform.rotate(Init_Image,self.Yaw)
            #Rot_Rect = Init_Image.get_rect(center=Init_Rect.center)
            #self.Image = Rot_Image
            #self.Rect = Rot_Rect
            self.Executing_Command = False
            return True

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

    def Read_Time(self):
        return str(time() - self.Start_Time)

    def Serial_Number(self):
        return str(self)

    # Not all functions are here

    """
    The receive command
    """

    # Inside the Tello_Communication object


    def Get_State(self):
        Dist = sqrt(self.Tot_Dist_x**2 + self.Tot_Dist_y**2 + self.Tot_Dist_z**2)
        Run_Time = time() - self.Start_Time
        State = f"pitch:0;roll:0;yaw:{self.Yaw};vgx:{self.Speed_x};vgy:{self.Speed_y};vgz:{self.Speed_z};templ:12.2;temph:14.2;tof:{Dist};h:{self.Pos_z};bat:55;baro:22;time:{Run_Time};agx:0;agy:0;agz:0;\r\n"
        return State

    def Command_Handler(self, Events):
        #print("Command Handler working")
        for e in Events:
            if e.type == pygame.KEYDOWN:
                print("Keydown get")
                #print(e.key)
                if e.key == pygame.K_z:
                    print(self.Get_State())


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
        #self.Rect.topleft = self.Pos_x - Camera.Offset_x, self.Pos_y - Camera.Offset_y
        self.Rect.center = self.Pos_x - Camera.Offset_x, self.Pos_y - Camera.Offset_y
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
