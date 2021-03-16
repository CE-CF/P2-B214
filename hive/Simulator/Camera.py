from main import ScreenWidth, ScreenHeight
from math import sqrt
import pygame


Pos = Pos_x, Pos_y = [ScreenWidth/2, ScreenHeight/2]
Offset = Offset_x, Offset_y = [Pos_x - ScreenWidth/2, Pos_y - ScreenHeight/2]


Move_Left = False
Move_Right = False
Move_Down = False
Move_Up = False

def Offset_Handler(Speed):
    global Offset_x
    global Offset_y
    xIncrease = ( Move_Right*(Speed - (Move_Up    | Move_Down)*Speed*((sqrt(2)-1)/sqrt(2)))
                - Move_Left *(Speed - (Move_Up    | Move_Down)*Speed*((sqrt(2)-1)/sqrt(2))))
    yIncrease = ( Move_Down *(Speed - (Move_Right | Move_Left)*Speed*((sqrt(2)-1)/sqrt(2)))
                - Move_Up   *(Speed - (Move_Right | Move_Left)*Speed*((sqrt(2)-1)/sqrt(2))))
    Offset_x += xIncrease
    Offset_y += yIncrease
    #print(f'New Camera x offset is {Offset_x}')
    #print(f'New Camera y offset is {Offset_y}')
    #print(f'x offset speed is {xIncrease}')
    #print(f'y offset speed is {yIncrease}')

def Keyhold(keyPressList):
    global Move_Left, Move_Right, Move_Down, Move_Up
    Move_Left = keyPressList[pygame.K_a]
    Move_Right = keyPressList[pygame.K_d]
    Move_Down = keyPressList[pygame.K_s]
    Move_Up = keyPressList[pygame.K_w]
