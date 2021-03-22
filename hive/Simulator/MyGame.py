import pygame
import Camera
#import OLD_Camera
import Drone

class Game():

    #ScreenSize = ScreenHeight, ScreenWidth = 1080, 640

    #MainCamera = OLD_Camera.Camera()

    def __init__(self, ScreenWidth = 1080, ScreenHeight = 640, FullScreen = False, Run = True):
        pygame.init()
        self.ScreenSize = self.ScreenWidth, self.ScreenHeight = ScreenWidth, ScreenHeight
        #Game.ScreenSize = Game.ScreenHeight, Game.ScreenWidth = ScreenHeight, ScreenWidth
        self.Screen = pygame.display.set_mode(self.ScreenSize, flags= pygame.FULLSCREEN * FullScreen)
        self.Run = Run

    def init(self, ScreenHeight = 1080, ScreenWidth = 640, FullScreen = False, Run = True):
        pygame.init()
        Game.ScreenSize = Game.ScreenHeight, Game.ScreenWidth = ScreenHeight, ScreenWidth
        Game.Screen = pygame.display.set_mode(Game.ScreenSize, flags= pygame.FULLSCREEN * FullScreen)
        Game.Run = Run

    def setup(self):
        #global Drones
        self.Drones = [Drone.Drone(200, 300), Drone.Drone(800, 300, pygame.K_j, pygame.K_l, pygame.K_k, pygame.K_i)]
        #Drones = [Drone.Drone(200,300), Drone.Drone(820,300), Drone.Drone(510, 100, pygame.K_j, pygame.K_l, pygame.K_k, pygame.K_i),Drone.Drone(510, 500, pygame.K_j, pygame.K_l, pygame.K_k, pygame.K_i)]

    def close(self):
        pygame.display.quit()
        pygame.quit()

    def Update_Rects(self):
        for i in self.Drones:
            i.Update_Rect()

    def Update_Key_Holds(self, KeyPressList):
        Camera.Keyhold(KeyPressList)
        #Game.MainCamera.Keyhold(KeyPressList)
        for i in self.Drones:
            #print(f'{i} is being updated for Keyholds')
            i.Keyhold(KeyPressList)

    def Drones_Uniform_Movement_Handler(self, speed):
        for i in self.Drones:
            i.Movement_Handler(speed)

    def Drones_Collision_Handler(self):
        for i in self.Drones:
            for j in self.Drones:
                if i == j:
                    continue
                else:
                    i.Check_Collision(j.Rect)

    def Draw_Sprites(self):
        for i in self.Drones:
            self.Screen.blit(i.Image, i.Rect)

    def Game_Loop(self):
        self.setup()
        global Drones
        while self.Run:
            eventsList = pygame.event.get()
            keyPressList = pygame.key.get_pressed()
            self.Update_Key_Holds(keyPressList)

            self.Screen.fill((255,255,255))
            Camera.Offset_Handler(1)
            #Game.MainCamera.Movement_Handler(1)
            #self.Drones[0].Movement_Handler(1)
            #self.Drones[1].Movement_Handler(1)
            self.Drones_Uniform_Movement_Handler(1)
            #Update_Rects()
            self.Drones_Collision_Handler()
            self.Update_Rects()

            #if len(eventsList) != 0:
            #    print(eventsList)
            #    print(f'Length is: {len(eventsList)}')
            #print(keyPressList[pygame.K_UP])

            for e in eventsList:
                if e.type == pygame.QUIT:
                    self.close()
                    #sys.exit()
                    return

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self.close()
                        #sys.exit()
                        return

            self.Draw_Sprites()
            pygame.display.flip()
