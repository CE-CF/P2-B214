import pygame
import DroneHandler as DH
import CameraWindow as CW
#import cv2

class Game:

    #ScreenSize = ScreenHeight, ScreenWidth = 1080, 640

    #MainCamera = OLD_Camera.Camera()
    # Constructer for game object with it's resolution and other options
    def __init__(self, DroneHandler: [DH.DroneHandler], VideoSorter, ScreenWidth = 960, ScreenHeight = 720,
                 FullScreen = False, Run = True, FPS = 60):
        pygame.init()   # Initialize all pygame modules
        self.VS = VideoSorter
        self.DH = DroneHandler # Initialize the drone handler
        self.DH_Index = 0
        #self.Camera_Windows = [CW.CameraWindow(i) for i in self.DH]
        self.Camera_Windows = []
        for i in self.DH:
            self.Camera_Windows.append(CW.CameraWindow(i))
        self.ScreenHeightAdjuster = int(60*(ScreenHeight/720))
        print(f'Adjuster is: {self.ScreenHeightAdjuster}')
        print(f'Fill screen size is: {ScreenWidth}, {ScreenHeight+self.ScreenHeightAdjuster}')
        self.ScreenSize = self.ScreenWidth, self.ScreenHeight = ScreenWidth, ScreenHeight+self.ScreenHeightAdjuster
        self.Screen = pygame.display.set_mode(self.ScreenSize, flags= pygame.FULLSCREEN * FullScreen)
        print(f'Actual display size is: {self.Screen.get_size()}')
        self.Run = Run
        self.Joystick_Handler_Ran = 0
        self.clock = pygame.time.Clock()
        self.FPS = FPS
        self.KillAllRect = pygame.Rect(0,0,int(self.ScreenWidth/2),self.ScreenHeightAdjuster)
        self.KillAllRect.bottomright = (self.ScreenWidth, self.ScreenHeight)
        self.KillAllText = pygame.font.SysFont("Calibri", int(self.ScreenHeightAdjuster)).render("KILL ALL", True, pygame.Color("black"))
        self.KillAllTextRect = self.KillAllText.get_rect()
        self.KillAllTextRect.center = self.KillAllRect.center
        self.StopAllRect = pygame.Rect(0,0,int(self.ScreenWidth/2),self.ScreenHeightAdjuster)
        self.StopAllRect.bottomleft = (0,self.ScreenHeight)
        self.StopAllText = pygame.font.SysFont("Calibri", int(self.ScreenHeightAdjuster)).render("STOP ALL", True, pygame.Color("black"))
        self.StopAllTextRect = self.StopAllText.get_rect()
        self.StopAllTextRect.center = self.StopAllRect.center
    # Setup for the game loop function
    def setup(self):
        pass

    # Creates the joystick objects according to how many joysticks are connected, and creates input dictionaries for them
    # The input dictionary is a dictionary the has the state of every button, axis, hat and ball of the joystick
    def Joystick_Setup(self):
        self.Joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]  # Creates an array with all joystick objects
        self.JoysticksInput = []  # Creates an array that has the input dictionary for each joystick object
        # Loop through the joystick objects and create their input dictionaries
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

        """
        if (not self.Joystick_Handler_Ran) and (len(self.Joysticks) > 0):
            print(f'Joystick count is: {pygame.joystick.get_count()}')
            print(self.Joysticks)
            print(self.Joysticks[0].get_init())
            print(self.Joysticks[0].get_instance_id())
            print(self.Joysticks[0].get_guid())
            print(self.Joysticks[0].get_name())
            print(self.Joysticks[0].get_numaxes())
            print(self.Joysticks[0].get_numbuttons())
            print(self.JoysticksInput[0])
        """
    # Function that updates the input dictionary values for a joystick object
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
        pygame.display.quit()
        pygame.quit()
        self.VS.Finish()
        for i in self.DH:
            i.Stop()

    # Function that updates the key holds for all objects that need updating them
    def Update_Key_Holds(self, KeyPressList, EventList):
        if pygame.joystick.get_count() == 0:
            #for i in self.DH:
            for i in self.Camera_Windows:
                i.ControlHandler(KeyPressList, EventList, {})
        else:
            #for i in self.DH:
            for i in self.Camera_Windows:
                i.ControlHandler(KeyPressList, EventList, self.JoysticksInput[0])

    # Function that draws the Cameras for all available drones
    def Draw_Cameras(self):
        #print("Drawing camera")
        AdjustedScreenHeight = self.ScreenHeight - self.ScreenHeightAdjuster
        Focused = False; Focused_Cam = 0
        for i in range(len(self.Camera_Windows)):
            #print(f'Checking for focused camera: {i}')
            if self.Camera_Windows[i].Focused:
                Focused = True
                Focused_Cam = i
                break
            else:
                continue
        if Focused:
            for i in range(len(self.Camera_Windows)):
                #print(f'Drawing after detecting focus: {i}')
                if i == Focused_Cam:
                    self.Camera_Windows[i].Draw_Camera(self.Screen, i, 0, (self.ScreenWidth, AdjustedScreenHeight), len(self.Camera_Windows), True)
                else:
                    self.Camera_Windows[i].Camera_Unfocused()
        else:
            for i in range(len(self.Camera_Windows)):
                #print(f'Drawing camera without focus: {i}')
                self.Camera_Windows[i].Draw_Camera(self.Screen, i, 0, (self.ScreenWidth, AdjustedScreenHeight), len(self.Camera_Windows))
                #self.Camera_Windows[i].Draw_Camera(self.Screen, i+1, 0, (self.ScreenWidth, self.ScreenHeight), 3)

    def Draw_Buttons(self):
        pygame.draw.rect(self.Screen,pygame.Color("yellow"), self.StopAllRect)
        pygame.draw.rect(self.Screen,pygame.Color("red"), self.KillAllRect)
        self.Screen.blit(self.StopAllText, self.StopAllTextRect)
        self.Screen.blit(self.KillAllText, self.KillAllTextRect)

    """
    def Draw_Rect_Alpha(self, surface, color, alpha, rect):
        #shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        shape_surf = pygame.Surface(pygame.Rect(rect).size)
        shape_surf.set_alpha(alpha)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
        surface.blit(shape_surf, rect)
    """


    # The main game loop
    def Game_Loop(self):
        self.setup()
        self.Joystick_Setup()
        # The while loop. Might also just be a while True
        while self.Run:
            self.clock.tick(self.FPS)
            eventsList = pygame.event.get()             # Get the list of all events
            keyPressList = pygame.key.get_pressed()     # Get the list of all keyboard key's held
            self.Joystick_Handler(0)                    # Run the joystick input handler (Only running for first joystick currnetly)
            self.Update_Key_Holds(keyPressList, eventsList)         # Run the keyhold function
            self.Screen.fill((255,255,255))             # Fill screen with white to refresh
            self.Draw_Cameras()
            self.Draw_Buttons()
            '''
            Frame = self.DH[self.DH_Index].GetFrame()                  # Get the video frame from the drone handler
            FrameRatio = 1
            FrameWidth = 960                            # Set the video frame width
            FrameHeight = 720                           # Set the video frame height
            #Image = pygame.image.frombuffer(Frame, (FrameWidth, FrameHeight), "BGR")
            # Check if the screen is smaller than the width of the frame and resize the frame accordingly
            if self.ScreenWidth < 960 or self.ScreenHeight < 720:
                FrameRatio = min((self.ScreenWidth/920), (self.ScreenHeight/720))
                FrameHeight =int(FrameHeight*FrameRatio)
                FrameWidth = int(FrameWidth*FrameRatio)
                #pygame.transform.scale(Image, (FrameWidth, FrameHeight))
                Frame = cv2.resize(Frame,(FrameWidth,FrameHeight))
            # Create pygame image surface of the frame and draw it on the main surface
            Button_Rect1 = pygame.Rect(0,0,int(110*FrameRatio),int(64*FrameRatio))
            Button_Rect1.topright = (FrameWidth,0)
            Button_Text1 = pygame.font.SysFont("Calibri", int(60*FrameRatio)).render("Kill!!", True, pygame.Color("red"))
            Button_Rect2 = pygame.Rect(0,0,int(110*FrameRatio),int(64*FrameRatio))
            Button_Rect2.bottomleft = (0,FrameHeight)
            Button_Text2 = pygame.font.SysFont("Calibri", int(60*FrameRatio)).render("Stop", True, pygame.Color("red"))
            Image = pygame.image.frombuffer(Frame, (FrameWidth, FrameHeight), "BGR")
            #self.Draw_Rect_Alpha(Image, (0,0,0), 128, Button_Rect1)
            pygame.draw.rect(Image,(0,0,0,0), Button_Rect1)
            Image.blit(Button_Text1, Button_Rect1)
            #self.Draw_Rect_Alpha(Image, (0,0,0), 128, Button_Rect2)
            pygame.draw.rect(Image,(0,0,0,0), Button_Rect2)
            Image.blit(Button_Text2, Button_Rect2)
            self.Screen.blit(Image, ((self.ScreenWidth - FrameWidth)/2,0))
            #self.Screen.blit(Image, (0,0))
            '''
            for e in eventsList:
                if e.type == pygame.QUIT:   # QUIT is the event of the X button on the top corner being pressed
                    self.close()
                    return
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if self.KillAllRect.collidepoint(pygame.mouse.get_pos()):
                        for i in self.DH:
                            i.Emergency()
                    elif self.StopAllRect.collidepoint(pygame.mouse.get_pos()):
                        for i in self.DH:
                            i.Stop_Button_Command()
                    else:
                        Set_Focus = False; Pressed = 0
                        for i in range(len(self.Camera_Windows)):
                            result = self.Camera_Windows[i].Detect_Click(pygame.mouse.get_pos())
                            if result == 69:
                                Pressed = i
                                Set_Focus = True
                        if Set_Focus:
                            for i in range(len(self.Camera_Windows)):
                                if i == Pressed:
                                    continue
                                else:
                                    self.Camera_Windows[i].Focused = False
                    """
                    if Button_Rect1.collidepoint(pygame.mouse.get_pos()):
                        print("Drone Killed")
                    elif Button_Rect2.collidepoint(pygame.mouse.get_pos()):
                        print("Drone Stopped")
                    """
                # Check an event of a key being pressed
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_1:
                        self.DH_Index = 0
                        print(f'Index number is: {self.DH_Index}')
                    elif e.key == pygame.K_2:
                        self.DH_Index = 1
                        print(f'Index number is: {self.DH_Index}')
                    if e.key == pygame.K_c: # Pressing c will give drone control to the controller
                        for i in range(len(self.DH)):
                            if i == self.DH_Index:
                                self.DH[i].SetControllerMode(True)
                            else:
                                self.DH[i].SetControllerMode(False)
                            #self.DH[i].SetControllerMode(True)
                            #print(f'Controller mode to drone number {i} is: {self.DH[i].Controllable}')
                    if e.key == pygame.K_v:
                        for i in range(len(self.DH)):
                            self.DH[i].SetControllerMode(False)
                            print(f'Controller mode to drone number {i} is: {self.DH[i].Controllable}')
                    if e.key == pygame.K_x:
                        for i in range(len(self.DH)):
                            self.DH[i].Controllable = not self.DH[i].Controllable
                            print(f'Control to drone number {i} is: {self.DH[i].Controllable}')
                    if e.key == pygame.K_z:
                        print("Connecting to ssid now")
                        self.DH[0].Connect_Network("ssid", "pass")
                        print("Connection done")
                    if e.key == pygame.K_ESCAPE:    # Escape will also close the program
                        self.close()
                        return
            # Get the FPS value to print it on the display (Can't really see it in this program)
            #FPS = self.clock.get_fps()
            #FPS_Text = pygame.font.SysFont("Arial", 16).render(str(int(FPS)), False, (255,255,255))
            #self.Screen.blit(FPS_Text, (0,0))
            # Get the battery level of the drone to print it on the display (Did not test it yet)
            #Battery_Level = self.DH[0].GetBattery()
            #Battery_Text = pygame.font.SysFont("Arial", 16).render(str(int(Battery_Level)), False, (255,255,255))
            #self.Screen.blit(Battery_Text, (0,48))

            #self.Draw_Sprites()             # Draw any sprites if available
            pygame.display.flip()           # Update the pygame display
