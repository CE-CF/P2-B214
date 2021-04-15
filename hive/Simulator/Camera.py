#from main import ScreenSize, ScreenWidth, ScreenHeight
#from MyGame import Game
from Global_Constants import ScreenSize, ScreenWidth, ScreenHeight
from math import sqrt
import pygame

"""I failed in making this into an object.
And it makes no sense to be one, cause it gotta be used by many different files"""

#ScreenWidth = 1080
#ScreenHeight = 640
#Game.Game.ScreenWidth

Pos = Pos_x, Pos_y = [ScreenWidth/2, ScreenHeight/2]                            # Actual position of the camera
Offset = Offset_x, Offset_y = [Pos_x - ScreenWidth/2, Pos_y - ScreenHeight/2]   # The offset, which all object's need to be moved by

#Pos = Pos_x, Pos_y = [MainGame.ScreenWidth/2, MainGame.ScreenHeight/2]
#Offset = Offset_x, Offset_y = [Pos_x - MainGame.ScreenWidth/2, Pos_y - MainGame.ScreenHeight/2]

print(f'Width is: {ScreenWidth}')
print(f'Height is: {ScreenHeight}')

#Pos = Pos_x, Pos_y = [Game.ScreenWidth/2, Game.ScreenHeight/2]
#Offset = Offset_x, Offset_y = [Pos_x - Game.ScreenWidth/2, Pos_y - Game.ScreenHeight/2]

# Movement booleans for key hold handler
Move_Left = False
Move_Right = False
Move_Down = False
Move_Up = False
Move_xAxis = 0.0
Move_yAxis = 0.0

# Move the camera by a certain speed. Exast same as drone movement handler
def Offset_Handler(Speed):
    global Offset_x
    global Offset_y
    if -0.1<Move_xAxis<0.1 and -0.1<Move_yAxis<0.1:
        xIncrease = ( Move_Right*(Speed - (Move_Up    | Move_Down)*Speed*((sqrt(2)-1)/sqrt(2)))
                    - Move_Left *(Speed - (Move_Up    | Move_Down)*Speed*((sqrt(2)-1)/sqrt(2))))
        yIncrease = ( Move_Down *(Speed - (Move_Right | Move_Left)*Speed*((sqrt(2)-1)/sqrt(2)))
                    - Move_Up   *(Speed - (Move_Right | Move_Left)*Speed*((sqrt(2)-1)/sqrt(2))))
    else:
        xIncrease = Move_xAxis*Speed
        yIncrease = Move_yAxis*Speed
    Offset_x += xIncrease
    Offset_y += yIncrease
    #print(f'New Camera x offset is {Offset_x}')
    #print(f'New Camera y offset is {Offset_y}')
    #print(f'x offset speed is {xIncrease}')
    #print(f'y offset speed is {yIncrease}')

# Check if the movement keys are held
def Keyhold(keyPressList, Joystick_InputDict = {}):
    global Move_Left, Move_Right, Move_Down, Move_Up, Move_xAxis, Move_yAxis
    Move_Left = keyPressList[pygame.K_a]
    Move_Right = keyPressList[pygame.K_d]
    Move_Down = keyPressList[pygame.K_s]
    Move_Up = keyPressList[pygame.K_w]
    Move_xAxis = Joystick_InputDict.get("Axis2")
    Move_yAxis = Joystick_InputDict.get("Axis3")
