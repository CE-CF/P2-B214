import pygame
import DroneHandler as DH
import CameraWindow as CW

class Game:

    # Constructer for game object with it's resolution and other options
    def __init__(self, DroneHandler: [DH.DroneHandler], ScreenWidth = 960, ScreenHeight = 720,
                 FullScreen = False, Run = True, FPS = 60):
        pygame.init()   # Initialize all pygame modules
        self.DH = DroneHandler # Initialize the drone handler
        self.DH_Index = 0
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
        for i in self.DH:
            i.Stop()

    # Function that updates the key holds for all objects that need updating them
    def Update_Key_Holds(self, KeyPressList, EventList):
        if pygame.joystick.get_count() == 0:
            for i in self.Camera_Windows:
                i.ControlHandler(KeyPressList, EventList, {})
        else:
            for i in self.Camera_Windows:
                i.ControlHandler(KeyPressList, EventList, self.JoysticksInput[0])

    # Function that draws the Cameras for all available drones
    # So that it shows one full screen camera or four small screen cameras at a time
    def Draw_Cameras(self):
        AdjustedScreenHeight = self.ScreenHeight - self.ScreenHeightAdjuster
        Focused = False; Focused_Cam = 0
        # Check if any of the cameras is focused
        for i in range(len(self.Camera_Windows)):
            if self.Camera_Windows[i].Focused:
                Focused = True
                Focused_Cam = i
                break
            else:
                continue
        # If a camera is focused, then blit that camera in full screen, and the other cameras empty
        if Focused:
            for i in range(len(self.Camera_Windows)):
                if i == Focused_Cam:
                    self.Camera_Windows[i].Draw_Camera(self.Screen, i, 0, (self.ScreenWidth, AdjustedScreenHeight), len(self.Camera_Windows), True)
                else:
                    self.Camera_Windows[i].Camera_Unfocused()
        else:
            for i in range(len(self.Camera_Windows)):
                self.Camera_Windows[i].Draw_Camera(self.Screen, i, 0, (self.ScreenWidth, AdjustedScreenHeight), len(self.Camera_Windows))

    # Draws the buttons that are global to all drones
    def Draw_Buttons(self):
        pygame.draw.rect(self.Screen,pygame.Color("yellow"), self.StopAllRect)
        pygame.draw.rect(self.Screen,pygame.Color("red"), self.KillAllRect)
        self.Screen.blit(self.StopAllText, self.StopAllTextRect)
        self.Screen.blit(self.KillAllText, self.KillAllTextRect)


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
            for e in eventsList:
                if e.type == pygame.QUIT:   # QUIT is the event of the X button on the top corner being pressed
                    self.close()
                    return
                if e.type == pygame.MOUSEBUTTONDOWN:    # Activates if any mouse button is pressed (Even mouse wheel rotations)
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
                    if e.key == pygame.K_v:
                        for i in range(len(self.DH)):
                            self.DH[i].SetControllerMode(False)
                            print(f'Controller mode to drone number {i} is: {self.DH[i].Controllable}')
                    if e.key == pygame.K_x:
                        for i in range(len(self.DH)):
                            self.DH[i].Controllable = not self.DH[i].Controllable
                            print(f'Control to drone number {i} is: {self.DH[i].Controllable}')
                    if e.key == pygame.K_ESCAPE:    # Escape will also close the program
                        self.close()
                        return
            pygame.display.flip()           # Update the pygame display
