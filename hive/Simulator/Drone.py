#import OLD_Camera
import Camera
import pygame
from math import sqrt

class Drone():
    def __init__(self, Start_x, Start_y, Key_Left = pygame.K_LEFT, Key_Right = pygame.K_RIGHT, Key_Down = pygame.K_DOWN, Key_Up = pygame.K_UP):
        self.Pos = self.Pos_x, self.Pos_y = [Start_x, Start_y]
        self.Rect = pygame.Rect(Start_x - Camera.Offset_x, Start_y - Camera.Offset_y, 64, 64)
        #self.Rect = pygame.Rect(Start_x - OLD_Camera.Camera.Offset_x, Start_y - OLD_Camera.Camera.Offset_y, 64, 64)
        self.Image = pygame.image.load("Drone_Icon.png")
        self.Key_Left = Key_Left
        self.Key_Right = Key_Right
        self.Key_Down = Key_Down
        self.Key_Up = Key_Up
        self.Move_Left = False
        self.Move_Right = False
        self.Move_Down = False
        self.Move_Up = False
        self.Speed_x = 0
        self.Speed_y = 0
        self.Colided_Left = False
        self.Colided_Right = False
        self.Colided_Down = False
        self.Colided_Up = False


    def Movement_Handler(self, Speed):
        self.Speed_x = ( self.Move_Right*(Speed - (self.Move_Up   | self.Move_Down)*Speed*((sqrt(2)-1)/sqrt(2)))
                       - self.Move_Left *(Speed - (self.Move_Up   | self.Move_Down)*Speed*((sqrt(2)-1)/sqrt(2))))
        self.Speed_y = ( self.Move_Down *(Speed - (self.Move_Right| self.Move_Left)*Speed*((sqrt(2)-1)/sqrt(2)))
                       - self.Move_Up   *(Speed - (self.Move_Right| self.Move_Left)*Speed*((sqrt(2)-1)/sqrt(2))))
        self.Pos_x += self.Speed_x
        self.Pos_y += self.Speed_y

    def Update_Rect(self):
        self.Rect.topleft = self.Pos_x - Camera.Offset_x, self.Pos_y - Camera.Offset_y
        #self.Rect.topleft = self.Pos_x - OLD_Camera.Camera.Offset_x, self.Pos_y - OLD_Camera.Camera.Offset_y

    def Keyhold(self, keyPressList):
        self.Move_Left = keyPressList[self.Key_Left]
        self.Move_Right = keyPressList[self.Key_Right]
        self.Move_Down = keyPressList[self.Key_Down]
        self.Move_Up = keyPressList[self.Key_Up]

    '''
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

    def Check_Collision(self, Rect):

        self.Update_Rect()
        Collision = self.Rect.colliderect(Rect)
        self.Pos_x -= self.Speed_x * Collision

        self.Update_Rect()
        Collision = self.Rect.colliderect(Rect)
        self.Pos_x += self.Speed_x * Collision
        self.Pos_y -= self.Speed_y * Collision

        self.Update_Rect()
        Collision = self.Rect.colliderect(Rect)
        self.Pos_x -= self.Speed_x * Collision

