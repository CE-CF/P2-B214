import pygame
import DroneHandler as DH
import cv2

class Game:

    #ScreenSize = ScreenHeight, ScreenWidth = 1080, 640

    #MainCamera = OLD_Camera.Camera()
    # Constructer for game object with it's resolution and other options
    def __init__(self, DroneHandler: DH.DroneHandler, ScreenWidth = 960, ScreenHeight = 720,
                 FullScreen = False, Run = True, FPS = 60):
        pygame.init()   # Initialize all pygame modules
        self.DH = DroneHandler # Initialize the drone handler
        self.ScreenSize = self.ScreenWidth, self.ScreenHeight = ScreenWidth, ScreenHeight
        self.Screen = pygame.display.set_mode(self.ScreenSize, flags= pygame.FULLSCREEN * FullScreen)
        self.Run = Run
        self.Joystick_Handler_Ran = 0
        self.clock = pygame.time.Clock()
        self.FPS = FPS
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
        self.DH.Stop()

    # Function that updates the key holds for all objects that need updating them
    def Update_Key_Holds(self, KeyPressList):
        if pygame.joystick.get_count() == 0:
            self.DH.ControlHandler(KeyPressList, {})
        else:
            self.DH.ControlHandler(KeyPressList, self.JoysticksInput[0])

    # Function that draws the sprites for all displayed objects
    def Draw_Sprites(self):
        pass


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
            self.Update_Key_Holds(keyPressList)         # Run the keyhold function
            self.Screen.fill((255,255,255))             # Fill screen with white to refresh
            Frame = self.DH.GetFrame()                  # Get the video frame from the drone handler
            FrameWidth = 960                            # Set the video frame width
            FrameHeight = 720                           # Set the video frame height
            # Check if the screen is smaller than the width of the frame and resize the frame accordingly
            if self.ScreenWidth < 960 or self.ScreenHeight < 720:
                FrameRatio = min((self.ScreenWidth/920), (self.ScreenHeight/720))
                FrameHeight =int(FrameHeight*FrameRatio)
                FrameWidth = int(FrameWidth*FrameRatio)
                Frame = cv2.resize(Frame,(FrameWidth,FrameHeight))
            # Create pygame image surface of the frame and draw it on the main surface
            Image = pygame.image.frombuffer(Frame, (FrameWidth, FrameHeight), "BGR")
            self.Screen.blit(Image, ((self.ScreenWidth - FrameWidth)/2,0))

            for e in eventsList:
                if e.type == pygame.QUIT:   # QUIT is the event of the X button on the top corner being pressed
                    self.close()
                    return
                # Check an event of a key being pressed
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_c: # Pressing c will give drone control to the controller
                        self.DH.SetControllerMode(True)
                    if e.key == pygame.K_ESCAPE:    # Escape will also close the program
                        self.close()
                        return
            # Get the FPS value to print it on the display (Can't really see it in this program)
            FPS = self.clock.get_fps()
            FPS_Text = pygame.font.SysFont("Arial", 16).render(str(int(FPS)), False, (0,0,0))
            self.Screen.blit(FPS_Text, (0,0))
            # Get the battery level of the drone to print it on the display (Did not test it yet)
            Battery_Level = self.DH.GetBattery()
            Battery_Text = pygame.font.SysFont("Arial", 16).render(str(int(Battery_Level)), False, (0,0,0))
            self.Screen.blit(Battery_Text, (0,48))

            self.Draw_Sprites()             # Draw any sprites if available
            pygame.display.flip()           # Update the pygame display
