#import OLD_Camera
import Camera
import pygame
from math import sqrt

class Drone():
    # Arguments( Start x pos, Start y pos, Movement speed, Control mode between analog or digital,
    #            the four digital keys that move the drone, the two digital axis that move the drone)
    def __init__(self, Start_x, Start_y, FPS, Speed = 10, Control_Type = 0,
                 Key_Left = pygame.K_LEFT, Key_Right = pygame.K_RIGHT,
                 Key_Down = pygame.K_DOWN, Key_Up = pygame.K_UP,
                 Joystick_xAxis = "Axis 0", Joystick_yAxis = "Axis 1"):
        self.Pos = self.Pos_x, self.Pos_y, self.Pos_z = [Start_x, Start_y, 50]
        # Drone's rectangle object. Used as the place to draw the drone, and as it's collision box.
        # The arguments are it's position and it's size
        self.Rect = pygame.Rect(Start_x - Camera.Offset_x, Start_y - Camera.Offset_y, 16, 16)
        self.Yaw = 0
        #self.Rect = pygame.Rect(Start_x - OLD_Camera.Camera.Offset_x, Start_y - OLD_Camera.Camera.Offset_y, 64, 64)
        # Load the image of the drone
        self.Init_Image = pygame.image.load("Drone_Icon.png")
        self.Image = self.Init_Image
        # Get the initial FPS of the simulation
        self.FPS = FPS
        # Set movement keys
        self.Key_Left = Key_Left
        self.Key_Right = Key_Right
        self.Key_Down = Key_Down
        self.Key_Up = Key_Up
        self.Control_Type = Control_Type
        self.Joystick_xAxis = Joystick_xAxis
        self.Joystick_yAxis = Joystick_yAxis
        # Set the booleans that activate with the movement keys
        self.Move_Left = False
        self.Move_Right = False
        self.Move_Down = False
        self.Move_Up = False

        self.Move_x = 0.0
        self.Move_y = 0.0
        # x, y and z speed of drone. Used to move the drone's position
        self.Speed_x = 0
        self.Speed_y = 0
        self.Speed_z = 0
        # I think these are not used anymore. Remenants of the old collision algorithsm
        #self.Colided_Left = False
        #self.Colided_Right = False
        #self.Colided_Down = False
        #self.Colided_Up = False
        # The length of the speed vector. Will be max speed when controller is implemented
        self.Speed = Speed/self.FPS
        # Arrays with the points of the path of the drone
        self.Real_Path = [(int(Start_x), int(Start_y)), (int(Start_x), int(Start_y))]
        self.Draw_Path = [(int(Start_x), int(Start_y)), (int(Start_x), int(Start_y))]

    # This function handles the movement of the drones by changing their position according to their speed
    # It checks the direction the drone is going and assigns the x and y speeds accordingly
    def Movement_Handler(self):
        if self.Control_Type == 1:
            self.Speed_x = self.Move_x*self.Speed
            self.Speed_y = self.Move_y*self.Speed
        else:
            self.Speed_x = ( self.Move_Right*(self.Speed - (self.Move_Up   | self.Move_Down)*self.Speed*((sqrt(2)-1)/sqrt(2)))
                           - self.Move_Left *(self.Speed - (self.Move_Up   | self.Move_Down)*self.Speed*((sqrt(2)-1)/sqrt(2))))
            self.Speed_y = ( self.Move_Down *(self.Speed - (self.Move_Right| self.Move_Left)*self.Speed*((sqrt(2)-1)/sqrt(2)))
                           - self.Move_Up   *(self.Speed - (self.Move_Right| self.Move_Left)*self.Speed*((sqrt(2)-1)/sqrt(2))))
        self.Pos_x += self.Speed_x
        self.Pos_y += self.Speed_y

    # This function updates the rectangle's position to match the drone's position
    def Update_Rect(self):
        self.Rect.topleft = self.Pos_x - Camera.Offset_x, self.Pos_y - Camera.Offset_y
        #self.Rect.topleft = self.Pos_x - OLD_Camera.Camera.Offset_x, self.Pos_y - OLD_Camera.Camera.Offset_y

    # This function takes the list of keys pressed by the input devices and assigns them to their corresponding move booleans
    def Keyhold(self, keyPressList, Joystick_InputDict = {}):
        if self.Control_Type == 0:
            self.Move_Left = keyPressList[self.Key_Left]
            self.Move_Right = keyPressList[self.Key_Right]
            self.Move_Down = keyPressList[self.Key_Down]
            self.Move_Up = keyPressList[self.Key_Up]
        elif self.Control_Type == 1 and Joystick_InputDict != {}:
            self.Move_x = Joystick_InputDict.get(self.Joystick_xAxis)
            self.Move_x = self.Move_x*(not (-0.1<self.Move_x<0.1))
            self.Move_y = Joystick_InputDict.get(self.Joystick_yAxis)
            self.Move_y = self.Move_y*(not (-0.1<self.Move_y<0.1))
        elif self.Control_Type == 2 and Joystick_InputDict != {}:
            self.Move_Left = Joystick_InputDict.get(self.Key_Left)
            self.Move_Right = Joystick_InputDict.get(self.Key_Right)
            self.Move_Down = Joystick_InputDict.get(self.Key_Down)
            self.Move_Up = Joystick_InputDict.get(self.Key_Up)

    '''
    # Old bad collision algorithms
    def Check_Collision(self, Rect):
        self.Pos_x += (self.Move_Left  and ((Rect.collidepoint(self.Rect.topleft)
                                                 | Rect.collidepoint(self.Rect.midleft)
                                                 | Rect.collidepoint(self.Rect.bottomleft))))  * 2 #self.Speed_x
        self.Pos_x -= (self.Move_Right and ((Rect.collidepoint(self.Rect.topright)
                                                 | Rect.collidepoint(self.Rect.midright)
                                                 | Rect.collidepoint(self.Rect.bottomright)))) * 2 #self.Speed_x
        self.Pos_y -= (self.Move_Down  and ((Rect.collidepoint(self.Rect.bottomleft)
                                                 | Rect.collidepoint(self.Rect.midbottom)
                                                 | Rect.collidepoint(self.Rect.bottomright)))) * 2 #self.Speed_y
        self.Pos_y += (self.Move_Up    and ((Rect.collidepoint(self.Rect.topright)
                                                 | Rect.collidepoint(self.Rect.midtop)
                                                 | Rect.collidepoint(self.Rect.topright))))    * 2 #self.Speed_y
    '''
    '''
    def Check_Collision(self, Rect):

        #self.Update_Rect()
        
        Collide_Left = (self.Rect.midleft[0] < Rect.midright[0])
        Collide_Right = (self.Rect.midright[0] > Rect.midleft[0])
        Collide_Down = (self.Rect.midbottom[1] > Rect.midtop[1])
        Collide_Up = (self.Rect.midtop[1] < Rect.midbottom[1])

        Collided = Collide_Left and Collide_Right and Collide_Down and Collide_Up

        Prevent_Left = not (Collide_Left and self.Colided_Left)
        Prevent_Right = not (Collide_Right and self.Colided_Right)
        Prevent_Down = not (Collide_Down and self.Colided_Down)
        Prevent_Up = not (Collide_Up and self.Colided_Up)

        #self.Move_Left = self.Move_Left and not (    (self.Rect.midleft[0] <= Rect.midright[0])
        #                                     and (self.Rect.midright[0] > Rect.midleft[0])
        #                                     and (self.Rect.midbottom[1] > Rect.midtop[1])
        #                                     and (self.Rect.midtop[1] < Rect.midbottom[1]))
        #self.Move_Up = self.Move_Up and not (    (self.Rect.midleft[0] < Rect.midright[0])
        #                                     and (self.Rect.midright[0] > Rect.midleft[0])
        #                                     and (self.Rect.midbottom[1] >= Rect.midtop[1])
        #                                     and (self.Rect.midtop[1] < Rect.midbottom[1]))


        
        print(f'This drone\'s Left coords: {self.Rect.midleft[0]} \n'
              f'Other Drone\'s Right coords: {Rect.midright[0]} \n'
              f'The first statement is: {(self.Rect.midleft[0] < Rect.midright[0])} \n'
              f'This drone\'s Right coords: {self.Rect.midright[0]} \n'
              f'Other Drone\'s Left coords: {Rect.midleft[0]} \n'
              f'The second statement is: {(self.Rect.midright[0] > Rect.midleft[0])} \n'
              f'This drone\'s Bottom coords: {self.Rect.midbottom[1]} \n'
              f'Other Drone\'s Top coords: {Rect.midtop[1]} \n'
              f'The third statement is: {(self.Rect.midbottom[1] > Rect.midtop[1])} \n'
              f'This drone\'s Top coords: {self.Rect.midtop[1]} \n'
              f'Other Drone\'s Bottom coords: {Rect.midbottom[1]} \n'
              f'The fourth statement is: {(self.Rect.midtop[1] < Rect.midbottom[1])} \n \n')

        self.Pos_x -= (self.Move_Left  and Collided) * self.Speed_x
        self.Pos_x -= (self.Move_Right and Collided) * self.Speed_x
        self.Pos_y -= (self.Move_Down  and Collided) * self.Speed_y
        self.Pos_y -= (self.Move_Up    and Collided) * self.Speed_y

        #self.Pos_x -= (Prevent_Left  and Collided) * self.Speed_x
        #self.Pos_x -= (Prevent_Right and Collided) * self.Speed_x
        #self.Pos_y -= (Prevent_Down  and Collided) * self.Speed_y
        #self.Pos_y -= (Prevent_Up    and Collided) * self.Speed_y

        self.Colided_Left = Collide_Left
        self.Colided_Right = Collide_Right
        self.Colided_Down = Collide_Down
        self.Colided_Up = Collide_Up
    '''

    # Function that updates the path arrays of the drone
    def Update_Path(self):
        X = int(self.Pos_x); Y = int(self.Pos_y)
        if (X == self.Real_Path[-1][0]) and (Y == self.Real_Path[-1][1]):
            pass
        else:
            self.Real_Path.append((X, Y))
        self.Draw_Path = []
        for i in range(len(self.Real_Path)):
            self.Draw_Path.append(((self.Real_Path[i][0] - Camera.Offset_x), (self.Real_Path[i][1] - Camera.Offset_y)))

    # Function to provide the FPS to the drone and update its speed
    def Update_FPS_Speed(self, FPS):
        FPS_Ratio = self.FPS/FPS
        self.FPS = FPS
        self.Speed = self.Speed*FPS_Ratio
        #self.Max_Yaw_Speed = self.Max_Yaw_Speed*FPS_Ratio

    # Final collision algoirthm. Argument(The rectangle to check if the drone collided with)
    def Check_Collision(self, Rect):
        # Checks if the rectangles collided horizontally
        Result = False
        self.Update_Rect()                          # Update this drone's rectangle position
        Collision = self.Rect.colliderect(Rect)     # Check if it collides with the argument rectangle
        self.Pos_x -= self.Speed_x * Collision      # Go back to the previous position horizontally if collided
        Result = Result or Collision
        # Checks if the rectangles collided vertically
        self.Update_Rect()                          # Update this drone's rectangle to the new position
        Collision = self.Rect.colliderect(Rect)     # Check if it collides with the argument rectangle
        self.Pos_x += self.Speed_x * Collision      # Negate the horizontal back movemenet if collided
        self.Pos_y -= self.Speed_y * Collision      # Go back to the previous position vertically if collided
        Result = Result or Collision
        # Checks if the rectangles collided both horizontally and vertically
        self.Update_Rect()                          # Update this drone's rectangle to the new position
        Collision = self.Rect.colliderect(Rect)     # Check if it collides with the argument rectangle
        self.Pos_x -= self.Speed_x * Collision      # Go back to the previous position horizontally again if collided
        Result = Result or Collision
        return Result

