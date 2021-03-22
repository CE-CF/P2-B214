import pygame
import Camera
import Global_Constants as GC
#import OLD_Camera
import Drone

class Game():

    #ScreenSize = ScreenHeight, ScreenWidth = 1080, 640

    #MainCamera = OLD_Camera.Camera()
    # Constructer for game object with it's resolution and other options
    def __init__(self, ScreenWidth = 1080, ScreenHeight = 640, FullScreen = False, Run = True):
        pygame.init()   # Initialize all pygame modules
        self.ScreenSize = self.ScreenWidth, self.ScreenHeight = ScreenWidth, ScreenHeight
        #Game.ScreenSize = Game.ScreenHeight, Game.ScreenWidth = ScreenHeight, ScreenWidth
        self.Screen = pygame.display.set_mode(self.ScreenSize, flags= pygame.FULLSCREEN * FullScreen)
        self.Run = Run
    # This function was used for making a static object. It is not used right now.
    '''def init(self, ScreenHeight = 1080, ScreenWidth = 640, FullScreen = False, Run = True):
        pygame.init()
        Game.ScreenSize = Game.ScreenHeight, Game.ScreenWidth = ScreenHeight, ScreenWidth
        Game.Screen = pygame.display.set_mode(Game.ScreenSize, flags= pygame.FULLSCREEN * FullScreen)
        Game.Run = Run'''
    # Setup for the game loop function
    def setup(self):
        #global Drones
        # Create a list of all drones
        # First drone has base speed of 1, second drone has speed set by start menu
        self.Drones = [Drone.Drone(200, 300),
                       Drone.Drone(800, 300, GC.Uniform_Drones_Speed, pygame.K_j, pygame.K_l, pygame.K_k, pygame.K_i)]
        #Drones = [Drone.Drone(200,300), Drone.Drone(820,300), Drone.Drone(510, 100, 1, pygame.K_j, pygame.K_l, pygame.K_k, pygame.K_i),Drone.Drone(510, 500, 1, pygame.K_j, pygame.K_l, pygame.K_k, pygame.K_i)]
    # Function that uninitializes the pygame module
    def close(self):
        pygame.display.quit()
        pygame.quit()
    # Function that updates the rectangles of all displayed objects
    def Update_Rects(self):
        for i in self.Drones:
            i.Update_Rect()
    # Function that updates the key holds for all objects that need updating them
    def Update_Key_Holds(self, KeyPressList):
        Camera.Keyhold(KeyPressList)
        #Game.MainCamera.Keyhold(KeyPressList)
        for i in self.Drones:
            #print(f'{i} is being updated for Keyholds')
            i.Keyhold(KeyPressList)
    # Function that goes through all drones in the list and runs their movement handler
    def Drones_Movement_Handler(self):
        for i in self.Drones:
            i.Movement_Handler()
    # Function that runs the collision algorithm for all drones in the list
    # This function will also pass obstacles and such as rect arguments when they are implemented
    def Drones_Collision_Handler(self):
        for i in self.Drones:
            for j in self.Drones:
                if i == j:
                    continue
                else:
                    i.Check_Collision(j.Rect)
    # Function that draws the sprites for all displayed objects
    def Draw_Sprites(self):
        for i in self.Drones:
            self.Screen.blit(i.Image, i.Rect)

    # The main game loop
    def Game_Loop(self):
        self.setup()
        global Drones
        # The while loop. Might also just be a while True
        while self.Run:
            eventsList = pygame.event.get()             # Get the list of all events
            keyPressList = pygame.key.get_pressed()     # Get the list of all keyboard key's held
            self.Update_Key_Holds(keyPressList)         # Run the keyhold function

            self.Screen.fill((255,255,255))             # Fill screen with white to refresh
            Camera.Offset_Handler(1)
            #Game.MainCamera.Movement_Handler(1)
            #self.Drones[0].Movement_Handler(1)
            #self.Drones[1].Movement_Handler(1)
            self.Drones_Movement_Handler()
            #Update_Rects()
            self.Drones_Collision_Handler()
            self.Update_Rects()

            #if len(eventsList) != 0:
            #    print(eventsList)
            #    print(f'Length is: {len(eventsList)}')
            #print(keyPressList[pygame.K_UP])
            # Check the event list for events
            for e in eventsList:
                if e.type == pygame.QUIT:   #QUIT is the event of the X button on the top corner being pressed
                    self.close()
                    #sys.exit()
                    return
                # Check an event of a key being pressed
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self.close()
                        #sys.exit()
                        return

            self.Draw_Sprites()
            pygame.display.flip()           # Update the pygame display
