import pygame
import sys
import Camera
import Drone

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
pygame.init()
#pygame.display.init()
ScreenSize = ScreenHeight, ScreenWidth = 1080, 640
Screen = pygame.display.set_mode(ScreenSize)
#Screen = pygame.display.set_mode(ScreenSize, flags=pygame.FULLSCREEN)
Drones = []

def setup():
    global Drones
    Drones = [Drone.Drone(200, 300), Drone.Drone(800, 300, pygame.K_j, pygame.K_l, pygame.K_k, pygame.K_i)]
    #Drones = [Drone.Drone(200,300), Drone.Drone(820,300), Drone.Drone(510, 100, pygame.K_j, pygame.K_l, pygame.K_k, pygame.K_i),Drone.Drone(510, 500, pygame.K_j, pygame.K_l, pygame.K_k, pygame.K_i)]

def Update_Rects():
    for i in Drones:
        i.Update_Rect()

def Update_Key_Holds(KeyPressList):
    Camera.Keyhold(KeyPressList)
    for i in Drones:
        #print(f'{i} is being updated for Keyholds')
        i.Keyhold(KeyPressList)

def Drones_Uniform_Movement_Handler(speed):
    for i in Drones:
        i.Movement_Handler(speed)

def Draw_Sprites():
    for i in Drones:
        Screen.blit(i.Image, i.Rect)

def main():
    setup()
    global Drones
    while pygame.display.get_active():
        Screen.fill((255,255,255))
        Camera.Offset_Handler(1)
        #Drones[0].Movement_Handler(1)
        #Drones[1].Movement_Handler(1)
        Drones_Uniform_Movement_Handler(1)
        Update_Rects()

        eventsList = pygame.event.get()
        keyPressList = pygame.key.get_pressed()
        Update_Key_Holds(keyPressList)

        #if len(eventsList) != 0:
        #    print(eventsList)
        #    print(f'Length is: {len(eventsList)}')
        #print(keyPressList[pygame.K_UP])

        for e in eventsList:
            if e.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    sys.exit()

        Draw_Sprites()
        pygame.display.flip()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
