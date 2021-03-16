import Camera
import pygame
from math import sqrt

class Drone():
    def __init__(self, Start_x, Start_y, Key_Left = pygame.K_LEFT, Key_Right = pygame.K_RIGHT, Key_Down = pygame.K_DOWN, Key_Up = pygame.K_UP):
        self.Pos = self.Pos_x, self.Pos_y = [Start_x, Start_y]
        self.Rect = pygame.Rect(Start_x - Camera.Offset_x, Start_y - Camera.Offset_y, 64, 64)
        self.Image = pygame.image.load("Drone_Icon.png")
        self.Key_Left = Key_Left
        self.Key_Right = Key_Right
        self.Key_Down = Key_Down
        self.Key_Up = Key_Up
        self.Move_Left = False
        self.Move_Right = False
        self.Move_Down = False
        self.Move_Up = False

    def Movement_Handler(self, Speed):
        xIncrease = ( self.Move_Right*(Speed - (self.Move_Up   | self.Move_Down)*Speed*((sqrt(2)-1)/sqrt(2)))
                    - self.Move_Left *(Speed - (self.Move_Up   | self.Move_Down)*Speed*((sqrt(2)-1)/sqrt(2))))
        yIncrease = ( self.Move_Down *(Speed - (self.Move_Right| self.Move_Left)*Speed*((sqrt(2)-1)/sqrt(2)))
                    - self.Move_Up   *(Speed - (self.Move_Right| self.Move_Left)*Speed*((sqrt(2)-1)/sqrt(2))))
        self.Pos_x += xIncrease
        self.Pos_y += yIncrease

    def Update_Rect(self):
        self.Rect.topleft = self.Pos_x - Camera.Offset_x, self.Pos_y - Camera.Offset_y

    def Keyhold(self, keyPressList):
        self.Move_Left = keyPressList[self.Key_Left]
        self.Move_Right = keyPressList[self.Key_Right]
        self.Move_Down = keyPressList[self.Key_Down]
        self.Move_Up = keyPressList[self.Key_Up]
