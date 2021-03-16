import pygame, sys, math

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
pygame.init()
#pygame.display.init()
ScreenSize = ScreenHeight, ScreenWidth = 1080, 640
Screen = pygame.display.set_mode(ScreenSize)
#Screen = pygame.display.set_mode(ScreenSize, flags=pygame.FULLSCREEN)

Camera_Pos = Camera_x, Camera_y = [ScreenHeight/2, ScreenWidth/2]
Camera_Pos_Offset = Camera_Offset_x, Camera_Offset_y = [Camera_x - ScreenHeight/2, Camera_y - ScreenWidth/2]
Camera_Offset_Left = False
Camera_Offset_Right = False
Camera_Offset_Down = False
Camera_Offset_Up = False

Drone_Pos = Drone_x, Drone_y = [500, 300]
Drone_Rect = pygame.Rect(Drone_x - Camera_Offset_x, Drone_y - Camera_Offset_y, 64, 64)
Drone_Img = pygame.image.load("Drone_Icon.png")
Drone_Going_Left = False
Drone_Going_Right = False
Drone_Going_Down = False
Drone_Going_Up = False

def Update_Rects():
    Drone_Rect.topleft = Drone_x - Camera_Offset_x, Drone_y - Camera_Offset_y
def Drone_Movement_Handler(Speed):
    global Drone_x
    global Drone_y
    xIncrease = ( Drone_Going_Right*(Speed - (Drone_Going_Up   | Drone_Going_Down)*Speed*((math.sqrt(2)-1)/math.sqrt(2)))
                - Drone_Going_Left *(Speed - (Drone_Going_Up   | Drone_Going_Down)*Speed*((math.sqrt(2)-1)/math.sqrt(2))))
    yIncrease = ( Drone_Going_Down *(Speed - (Drone_Going_Right| Drone_Going_Left)*Speed*((math.sqrt(2)-1)/math.sqrt(2)))
                - Drone_Going_Up   *(Speed - (Drone_Going_Right| Drone_Going_Left)*Speed*((math.sqrt(2)-1)/math.sqrt(2))))
    Drone_x += xIncrease
    Drone_y += yIncrease
    #print(f'x axis speed is {xIncrease}')
    #print(f'y axis speed is {yIncrease}')

def Camera_Offset_Handler(Speed):
    global Camera_Offset_x
    global Camera_Offset_y
    xIncrease = ( Camera_Offset_Right*(Speed - (Camera_Offset_Up   | Camera_Offset_Down)*Speed*((math.sqrt(2)-1)/math.sqrt(2)))
                - Camera_Offset_Left *(Speed - (Camera_Offset_Up   | Camera_Offset_Down)*Speed*((math.sqrt(2)-1)/math.sqrt(2))))
    yIncrease = ( Camera_Offset_Down *(Speed - (Camera_Offset_Right| Camera_Offset_Left)*Speed*((math.sqrt(2)-1)/math.sqrt(2)))
                - Camera_Offset_Up   *(Speed - (Camera_Offset_Right| Camera_Offset_Left)*Speed*((math.sqrt(2)-1)/math.sqrt(2))))
    Camera_Offset_x += xIncrease
    Camera_Offset_y += yIncrease
    #print(f'x axis speed is {xIncrease}')
    #print(f'y axis speed is {yIncrease}')

def Update_Key_Holds(keyPressList):
    global Drone_Going_Left, Drone_Going_Right, Drone_Going_Down, Drone_Going_Up
    global Camera_Offset_Left, Camera_Offset_Right, Camera_Offset_Down, Camera_Offset_Up
    Drone_Going_Left = keyPressList[pygame.K_LEFT]
    Drone_Going_Right = keyPressList[pygame.K_RIGHT]
    Drone_Going_Down = keyPressList[pygame.K_DOWN]
    Drone_Going_Up = keyPressList[pygame.K_UP]
    Camera_Offset_Left = keyPressList[pygame.K_a]
    Camera_Offset_Right = keyPressList[pygame.K_d]
    Camera_Offset_Down = keyPressList[pygame.K_s]
    Camera_Offset_Up = keyPressList[pygame.K_w]


def main():
    global Drone_Going_Left, Drone_Going_Right, Drone_Going_Down, Drone_Going_Up
    global Camera_Offset_Left, Camera_Offset_Right, Camera_Offset_Down, Camera_Offset_Up
    while pygame.display.get_active():
        Screen.fill((255,255,255))
        Drone_Movement_Handler(1)
        Camera_Offset_Handler(1)
        Update_Rects()
        eventsList = pygame.event.get()
        keyPressList = pygame.key.get_pressed()
        Update_Key_Holds(keyPressList)
        if len(eventsList) != 0:
            print(eventsList)
            print(f'Length is: {len(eventsList)}')
        print(keyPressList[pygame.K_UP])
        for e in eventsList:
            if e.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                '''
                if e.key == pygame.K_LEFT:
                    Drone_Going_Left = True
                elif e.key == pygame.K_RIGHT:
                    Drone_Going_Right = True
                elif e.key == pygame.K_DOWN:
                    Drone_Going_Down = True
                elif e.key == pygame.K_UP:
                    Drone_Going_Up = True
                elif e.key == pygame.K_a:
                    Camera_Offset_Left = True
                elif e.key == pygame.K_d:
                    Camera_Offset_Right = True
                elif e.key == pygame.K_s:
                    Camera_Offset_Down = True
                elif e.key == pygame.K_w:
                    Camera_Offset_Up = True
                elif e.key == pygame.K_ESCAPE:
                    sys.exit()
                '''
                if e.key == pygame.K_ESCAPE:
                    sys.exit()
            '''
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_LEFT:
                    Drone_Going_Left = False
                elif e.key == pygame.K_RIGHT:
                    Drone_Going_Right = False
                elif e.key == pygame.K_DOWN:
                    Drone_Going_Down = False
                elif e.key == pygame.K_UP:
                    Drone_Going_Up = False
                elif e.key == pygame.K_a:
                    Camera_Offset_Left = False
                elif e.key == pygame.K_d:
                    Camera_Offset_Right = False
                elif e.key == pygame.K_s:
                    Camera_Offset_Down = False
                elif e.key == pygame.K_w:
                    Camera_Offset_Up = False
                '''

        Screen.blit(Drone_Img, Drone_Rect)
        pygame.display.flip()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
