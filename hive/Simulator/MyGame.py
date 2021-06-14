import pygame
import Camera
import Global_Constants as GC
#import OLD_Camera
import Drone
#import New_Drone as ND

import Tello_Drone as TD
import Tello_Communication as TC

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
        self.clock = pygame.time.Clock()
        if GC.TelloMode:
            self.TC = TC.Tello_Communication()
            self.TC.start()
        self.DroneCameraCenterOffset = 0        # Used when centring camera to a drone
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
        # If Tello mode is set then it creates Tello drones
        if GC.TelloMode:
            #self.Drones = [TD.TelloDrone(200,300), TD.TelloDrone(400,300,IP_Address="0.0.0.1")]
            #self.Drones = [TD.TelloDrone(200,300,65*2), TD.TelloDrone(400,300,65*3), TD.TelloDrone(300,200)]
            self.Drones = []
            for i in range(GC.Drone_Number):
                self.Drones.append(TD.TelloDrone(100 + 100*i, 300, MaxSpeed=GC.Uniform_Drones_Speed,
                                                 MaxYawSpeed=GC.Uniform_Yaw_Speed, IP_Address=f'0.0.0.{i}'))
        # Otherwise it creates 3 drones with joystick, or 2 without joystick
        else:
            if pygame.joystick.get_count() == 0:
                self.Drones = [Drone.Drone(200, 300, GC.FPS),
                               Drone.Drone(800, 300, GC.FPS, GC.Uniform_Drones_Speed, 0,
                                           pygame.K_j, pygame.K_l,pygame.K_k, pygame.K_i)]
            else:
                self.Drones = [Drone.Drone(200, 300, GC.FPS),
                               Drone.Drone(800, 300, GC.FPS, GC.Uniform_Drones_Speed, 1,
                                           Joystick_xAxis="Axis0", Joystick_yAxis="Axis1"),
                               Drone.Drone(500, 300, GC.FPS, GC.Uniform_Drones_Speed, 2,
                                           "Button13", "Button14", "Button12", "Button11")]
        # Creates collision array for colouring stuff red on collision
        self.DronesCollided = []
        for i in range(len(self.Drones)):
            self.DronesCollided.append(False)
        #self.Drones = [Drone.Drone(200,300), Drone.Drone(820,300), Drone.Drone(510, 100, 1, pygame.K_j, pygame.K_l, pygame.K_k, pygame.K_i),Drone.Drone(510, 500, 1, pygame.K_j, pygame.K_l, pygame.K_k, pygame.K_i)]
        # Sets up the Tello communication object by providing the Tello drones
        for i in self.Drones:
            if i.__class__ == TD.TelloDrone:
                if GC.TelloMode:
                    self.TC.Add_Drone(i)
            else:
                continue

    # Read documentation (Control module implementation :P)
    def Joystick_Setup(self):
        self.Joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        self.JoysticksInput = []
        for i in range(len(self.Joysticks)):
            InputDict = {}
            for j in range(self.Joysticks[i].get_numaxes()):
                InputDict[f'Axis{j}'] = 0.0
            for j in range(self.Joysticks[i].get_numbuttons()):
                InputDict[f'Button{j}'] = False
            for j in range(self.Joysticks[i].get_numhats()):
                InputDict[f'Hat{j}'] = 0,0
            for j in range(self.Joysticks[i].get_numballs()):
                InputDict[f'Ball{j}'] = 0,0
            self.JoysticksInput.append(InputDict)

        if (len(self.Joysticks) > 0):
            print(f'Joystick count is: {pygame.joystick.get_count()}')
            print(self.Joysticks)
            print(self.Joysticks[0].get_init())
            print(self.Joysticks[0].get_instance_id())
            print(self.Joysticks[0].get_guid())
            print(self.Joysticks[0].get_name())
            print(self.Joysticks[0].get_numaxes())
            print(self.Joysticks[0].get_numbuttons())
            print(self.JoysticksInput[0])

    def Joystick_Handler(self, JoyNum):
        if len(self.Joysticks) != pygame.joystick.get_count():
            self.Joystick_Setup()
        if len(self.Joysticks) > 0:
            for i in range(self.Joysticks[JoyNum].get_numaxes()):
                self.JoysticksInput[JoyNum].update({f'Axis{i}': self.Joysticks[JoyNum].get_axis(i)})
            for i in range(self.Joysticks[JoyNum].get_numbuttons()):
                self.JoysticksInput[JoyNum].update({f'Button{i}': self.Joysticks[JoyNum].get_button(i)})
            for i in range(self.Joysticks[JoyNum].get_numhats()):
                self.JoysticksInput[JoyNum].update({f'Hat{i}': self.Joysticks[JoyNum].get_hat(i)})
            for i in range(self.Joysticks[JoyNum].get_numballs()):
                self.JoysticksInput[JoyNum].update({f'Ball{i}': self.Joysticks[JoyNum].get_ball(i)})
        else:
            return

    # Function that uninitializes the pygame module
    def close(self):
        self.Run = False
        if GC.TelloMode:
            self.TC.close()
        pygame.display.quit()
        pygame.quit()

    # Function that updates the rectangles of all displayed objects
    def Update_Rects(self):
        for i in self.Drones:
            i.Update_Rect()

    # Function that updates the key holds for all objects that need updating them
    def Update_Key_Holds(self, KeyPressList):
        if pygame.joystick.get_count() == 0:
            Camera.Keyhold(KeyPressList)
        else:
            Camera.Keyhold(KeyPressList, self.JoysticksInput[0])
        #Game.MainCamera.Keyhold(KeyPressList)
        for i in self.Drones:
            #print(f'{i} is being updated for Keyholds')
            if i.__class__ != Drone.Drone:
                return
            elif (i.Control_Type == 2 or i.Control_Type == 1) and pygame.joystick.get_count() > 0:
                i.Keyhold(KeyPressList, self.JoysticksInput[0])
            else:
                i.Keyhold(KeyPressList)

    # Function that goes through all drones in the list and runs their movement handler
    def Drones_Movement_Handler(self, EventList):
        for i in self.Drones:
            if i.__class__ == TD.TelloDrone:
                i.Command_Handler(EventList)
                i.RC_Handler()
            else:
                i.Movement_Handler()

    # Function that runs the collision algorithm for all drones in the list
    def Drones_Collision_Handler(self):
        for i in range(len(self.Drones)):
            self.DronesCollided[i] = False
            for j in range(len(self.Drones)):
                if self.Drones[i] == self.Drones[j]:
                    continue
                else:
                    Result = self.Drones[i].Check_Collision(self.Drones[j].Rect)
                    self.DronesCollided[i] = self.DronesCollided[i] or Result
                    self.DronesCollided[j] = self.DronesCollided[j] or Result

    # Function that draws the sprites for all displayed objects
    def Draw_Sprites(self):
        for i in range(len(self.Drones)):
            RectColor = (0,0,0)*(not self.DronesCollided[i]) + (255,0,0)*self.DronesCollided[i]
            pygame.draw.rect(self.Screen, RectColor,self.Drones[i].Rect,2)
            Num_Text = pygame.font.SysFont("Arial", 16).render(str(i), False, RectColor)
            Num_Pos = (self.Drones[i].Rect.left - 8, self.Drones[i].Rect.top -  16)
            self.Screen.blit(Num_Text, Num_Pos)
            self.Screen.blit(self.Drones[i].Image, self.Drones[i].Rect)
            if GC.Draw_Path:
                pygame.draw.lines(self.Screen, ((i*150)%255, (i*100)%255, (i*75)%255), False, self.Drones[i].Draw_Path)
        #print(self.DronesCollided)

    # Draws all the text statically displayed on the screen
    def Draw_Text(self):
        FPS = self.clock.get_fps()
        FPS_Text = pygame.font.SysFont("Arial", 16).render(str(int(FPS)), False, (0,0,0))
        self.Screen.blit(FPS_Text, (0,0))
        Camera_Pos_x_Str = f'X: {int(Camera.Offset_x)}'
        Camera_Pos_y_Str = f'Y: {int(Camera.Offset_y)}'
        Camera_Pos_x_Text = pygame.font.SysFont("Arial", 16).render(Camera_Pos_x_Str, False, (0,0,0))
        Camera_Pos_y_Text = pygame.font.SysFont("Arial", 16).render(Camera_Pos_y_Str, False, (0,0,0))
        self.Screen.blit(Camera_Pos_x_Text, (0,self.ScreenHeight-48))
        self.Screen.blit(Camera_Pos_y_Text, (0,self.ScreenHeight-32))
        for i in range(len(self.Drones)):
            if i<20:
                TextColor = (0,0,0)*(not self.DronesCollided[i]) + (255,0,0)*self.DronesCollided[i]
                DroneInfoStr = (f'Drone {i}: X={int(self.Drones[i].Pos_x)}, '
                                           f'Y={int(self.Drones[i].Pos_y)}, '
                                           f'Z={int(self.Drones[i].Pos_z)}, '
                                           #f'SX={int(self.Drones[i].Speed_x)}, '
                                           #f'SY={int(self.Drones[i].Speed_y)}, '
                                           #f'SZ={int(self.Drones[i].Speed_z)}, '
                                           f'Collided={("True"*self.DronesCollided[i]) + ("False"*(not self.DronesCollided[i]))}')
                DroneInfoText = pygame.font.SysFont("Arial", 16).render(DroneInfoStr, False, TextColor)
                self.Screen.blit(DroneInfoText, (0,32 + 16*i))
            else:
                break

    # Debug function that rotates a drone
    def Temp_Rot_Drone(self, Drone, angle):
        Drone.Yaw += angle
        Drone.Image = pygame.transform.rotate(Drone.Init_Image, Drone.Yaw)
        Drone.Rect = Drone.Image.get_rect(center=Drone.Rect.center)

    # Function that updates the rotation of the drone image
    def Drone_Update_Rot(self):
        for i in self.Drones:
            i.Image = pygame.transform.rotate(i.Init_Image, -i.Yaw)
            i.Rect.size = i.Image.get_size()

    # Function that updates the path taken by the drone
    def Drone_Update_Path(self):
        if GC.Draw_Path:
            for i in range(len(self.Drones)):
                self.Drones[i].Update_Path()

    # Function that updates the FPS value in the drones used to convert speed
    def Drone_Update_FPS_Speed(self, FPS):
        for i in range(len(self.Drones)):
            self.Drones[i].Update_FPS_Speed(FPS)

    # The main game loop
    def Game_Loop(self):
        self.setup()
        self.Joystick_Setup()
        global Drones
        # The while loop. Might also just be a while True
        while self.Run:
            self.clock.tick(GC.FPS)
            FPS_For_Speed = self.clock.get_fps() + 1*(self.clock.get_fps()==0)
            eventsList = pygame.event.get()             # Get the list of all events
            keyPressList = pygame.key.get_pressed()     # Get the list of all keyboard key's held
            self.Joystick_Handler(0)
            self.Update_Key_Holds(keyPressList)         # Run the keyhold function
            #if self.JoysticksInput[0].get("Button5"):
                #print(self.JoysticksInput[0])
                #print("Button 0 is pressed")
            self.Screen.fill((255,255,255))             # Fill screen with white to refresh
            Camera.Offset_Handler(30/FPS_For_Speed)
            #Game.MainCamera.Movement_Handler(1)
            #self.Drones[0].Movement_Handler(1)
            #self.Drones[1].Movement_Handler(1)
            self.Drone_Update_FPS_Speed(FPS_For_Speed)
            self.Drones_Movement_Handler(eventsList)
            #Update_Rects()
            self.Drones_Collision_Handler()
            self.Drone_Update_Rot()
            self.Drone_Update_Path()
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
                if e.type == pygame.JOYBUTTONDOWN:
                #    print("Joystick button pressed.")
                    print(self.JoysticksInput[0])
                #if e.type == pygame.JOYBUTTONUP:
                #    print("Joystick button released.")
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_KP0:
                        Camera.Offset_x = 0; Camera.Offset_y = 0
                    if e.key == pygame.K_KP4:
                        self.DroneCameraCenterOffset = (len(self.Drones) - 1 + self.DroneCameraCenterOffset) % len(self.Drones)
                        Camera.Offset_x = self.Drones[self.DroneCameraCenterOffset].Pos_x - self.ScreenWidth/2
                        Camera.Offset_y = self.Drones[self.DroneCameraCenterOffset].Pos_y - self.ScreenHeight/2
                    if e.key == pygame.K_KP6:
                        self.DroneCameraCenterOffset = (self.DroneCameraCenterOffset + 1) % len(self.Drones)
                        Camera.Offset_x = self.Drones[self.DroneCameraCenterOffset].Pos_x - self.ScreenWidth/2
                        Camera.Offset_y = self.Drones[self.DroneCameraCenterOffset].Pos_y - self.ScreenHeight/2
                    """
                    if e.key == pygame.K_o:
                        self.Temp_Rot_Drone(self.Drones[0], 36)
                    if e.key == pygame.K_u:
                        self.Temp_Rot_Drone(self.Drones[0], -36)
                    if e.key == pygame.K_p:
                        print(self.JoysticksInput)
                        print(pygame.joystick.get_count())
                        for i in range(pygame.joystick.get_count()):
                            print(pygame.joystick.Joystick(i).get_init())
                            print(self.Joysticks[0].get_init())
                            print(pygame.joystick.Joystick(i).get_guid())
                            print(self.Joysticks[0].get_guid())
                            print(pygame.joystick.Joystick(i))
                            print(self.Joysticks[0])
                    """
                    if e.key == pygame.K_ESCAPE:
                        self.close()
                        #sys.exit()
                        return

            self.Draw_Sprites()
            self.Draw_Text()
            pygame.display.flip()           # Update the pygame display
