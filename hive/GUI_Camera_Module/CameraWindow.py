from .CameraButton import CameraButton
import pygame
import cv2

"""
This class is used to draw the camera feed on the main window, and to draw all buttons and text needed for them
It also detects clicks on each camera window accordingly
"""
class CameraWindow:

    #def __init__(self, Drone, Resolution, No_Of_Cameras):
    def __init__(self, Drone):
        self.Buttons = self.Kill_Button, self.Stop_Button, self.Unfocus_Button = (CameraButton(), CameraButton(), CameraButton())
        self.Drone = Drone
        self.Focused = False

    # This function draws all the buttons on each camera feed
    #def Draw_Buttons(self, Image, FrameRatio, Pos_x, Pos_y, FrameWidth, FrameHeight):
    def Draw_Buttons(self):
        self.Kill_Button.Font = pygame.font.SysFont("Calibri", int(60*self.FrameRatio))
        self.Kill_Button.Text = self.Kill_Button.Font.render("Kill!!", True, pygame.Color("red"))
        self.Kill_Button.Rect = self.Kill_Button.Text.get_rect()
        self.Kill_Button.Click_Rect = self.Kill_Button.Text.get_rect()
        self.Kill_Button.Click_Rect.topright = ((self.Pos_x + self.FrameWidth), self.Pos_y)
        self.Kill_Button.Rect.topright = ((self.FrameWidth), 0)
        pygame.draw.rect(self.Image,self.Kill_Button.Color, self.Kill_Button.Rect)
        self.Image.blit(self.Kill_Button.Text, self.Kill_Button.Rect)
        self.Stop_Button.Font = pygame.font.SysFont("Calibri", int(60*self.FrameRatio))
        self.Stop_Button.Text = self.Stop_Button.Font.render("Stop", True, pygame.Color("red"))
        self.Stop_Button.Rect = self.Kill_Button.Text.get_rect()
        self.Stop_Button.Click_Rect = self.Kill_Button.Text.get_rect()
        self.Stop_Button.Click_Rect.bottomleft = (self.Pos_x, (self.Pos_y + self.FrameHeight))
        self.Stop_Button.Rect.bottomleft = (0, (self.FrameHeight))
        pygame.draw.rect(self.Image,self.Stop_Button.Color, self.Stop_Button.Rect)
        self.Image.blit(self.Stop_Button.Text, self.Stop_Button.Rect)
        self.Unfocus_Button.Rect = pygame.Rect(0,0,0,0)
        self.Unfocus_Button.Click_Rect = pygame.Rect(0,0,0,0)
        if self.Focused:
            self.Unfocus_Button.Font = pygame.font.SysFont("Calibri", int(60*self.FrameRatio))
            self.Unfocus_Button.Text = self.Kill_Button.Font.render("X", True, pygame.Color("red"))
            self.Unfocus_Button.Rect = self.Unfocus_Button.Text.get_rect()
            self.Unfocus_Button.Click_Rect = self.Unfocus_Button.Text.get_rect()
            self.Unfocus_Button.Rect.topleft = (self.Pos_x, self.Pos_y)
            self.Unfocus_Button.Click_Rect.topleft = (self.Pos_x, self.Pos_y)
            pygame.draw.rect(self.Image, self.Unfocus_Button.Color, self.Unfocus_Button.Rect)
            self.Image.blit(self.Unfocus_Button.Text, self.Unfocus_Button.Rect)


    # This function checks the status of the camera and draws the frames accordingly
    def Draw_Camera(self, Surface, Camera_Index, Camera_Scroll, Resolution, No_Of_Cameras, FullScreen = False):
        self.FrameWidth = 960; self.FrameHeight = 720
        # Resizes the camera accordingly if the window is not as big as needed
        if Resolution[0] < 960 or Resolution[1] < 720:
            self.FrameRatio = min((Resolution[0]/920), (Resolution[1]/720))
        else:
            self.FrameRatio = 1
        if FullScreen:
            self.Frame = self.Drone.GetFrame()
            self.FrameHeight = int(self.FrameHeight*self.FrameRatio)
            self.FrameWidth = int(self.FrameWidth*self.FrameRatio)
            self.Frame = cv2.resize(self.Frame,(self.FrameWidth,self.FrameHeight))
            self.Image = pygame.image.frombuffer(self.Frame, (self.FrameWidth, self.FrameHeight), "BGR")
            self.Pos_x = (Resolution[0] - self.FrameWidth)/2
            self.Pos_y = (Resolution[1] - self.FrameHeight)/2
            self.Rect = pygame.rect.Rect(self.Pos_x, self.Pos_y, self.FrameWidth, self.FrameHeight)
            self.Draw_Buttons()
            # Stuff to draw the fps of the camera feed
            Frame_FPS = self.Drone.GetFrameFPS()
            FPS_Text = pygame.font.SysFont("Arial", 32).render(str(int(Frame_FPS)), False, pygame.Color("white"))
            self.Image.blit(FPS_Text, (0,0))
            # Stuff to draw the battery of the drone
            Battery_Level = self.Drone.GetBattery()
            Battery_Text = pygame.font.SysFont("Arial", 32).render(str(int(Battery_Level)), False, pygame.Color("red"))
            self.Image.blit(Battery_Text, (0,64))
            # Stuff to draw the flying status of the drone
            if self.Drone.GetFlying():
                Flying_Text = pygame.font.SysFont("Arial", 32).render(("Flying"), False, pygame.Color("green"))
            else:
                Flying_Text = pygame.font.SysFont("Arial", 32).render(("Flying"), False, pygame.Color("red"))
            self.Image.blit(Flying_Text, (0,128))
            Surface.blit(self.Image, self.Rect)
        else:
            self.FrameRatio = self.FrameRatio/2
            if No_Of_Cameras > 4:
                if (Camera_Index-2*Camera_Scroll)>=0 and (Camera_Index-2*Camera_Scroll)<4:
                    self.Frame = self.Drone.GetFrame()
                    self.FrameHeight = int(self.FrameHeight*self.FrameRatio)
                    self.FrameWidth = int(self.FrameWidth*self.FrameRatio)
                    self.Frame = cv2.resize(self.Frame,(self.FrameWidth,self.FrameHeight))
                    self.Image = pygame.image.frombuffer(self.Frame, (self.FrameWidth, self.FrameHeight), "BGR")
                    Index = Camera_Index - 2*Camera_Scroll
                    self.Pos_x = (Resolution[0]/2) - self.FrameWidth*(1 - (Index // 2))
                    self.Pos_y = (Resolution[1]/2) - self.FrameHeight*((Index+1) % 2)
                    self.Rect = pygame.rect.Rect(self.Pos_x, self.Pos_y, self.FrameWidth, self.FrameHeight)
                    self.Draw_Buttons()
                    # Stuff to draw the fps of the camera feed
                    Frame_FPS = self.Drone.GetFrameFPS()
                    FPS_Text = pygame.font.SysFont("Arial", 16).render(str(int(Frame_FPS)), False, pygame.Color("white"))
                    self.Image.blit(FPS_Text, (0,0))
                    # Stuff to draw the battery of the drone
                    Battery_Level = self.Drone.GetBattery()
                    Battery_Text = pygame.font.SysFont("Arial", 16).render(str(int(Battery_Level)), False, pygame.Color("red"))
                    self.Image.blit(Battery_Text, (0,48))
                    # Stuff to draw the flying status of the drone
                    if self.Drone.GetFlying():
                        Flying_Text = pygame.font.SysFont("Arial", 16).render(("Flying"), False, pygame.Color("green"))
                    else:
                        Flying_Text = pygame.font.SysFont("Arial", 16).render(("Flying"), False, pygame.Color("red"))
                    self.Image.blit(Flying_Text, (0,96))
                    Surface.blit(self.Image, self.Rect)
                else:
                    self.Rect = pygame.rect.Rect(0,0,0,0)
            else:
                self.Frame = self.Drone.GetFrame()
                self.FrameHeight = int(self.FrameHeight*self.FrameRatio)
                self.FrameWidth = int(self.FrameWidth*self.FrameRatio)
                if type(self.Frame) == type(None):
                    self.Image = pygame.surface.Surface((self.FrameWidth, self.FrameHeight))
                else:
                    self.Frame = cv2.resize(self.Frame,(self.FrameWidth,self.FrameHeight))
                    self.Image = pygame.image.frombuffer(self.Frame, (self.FrameWidth, self.FrameHeight), "BGR")
                Index = Camera_Index - 2*Camera_Scroll
                self.Pos_x = (Resolution[0]/2) - self.FrameWidth*(1 - (Index // 2))
                self.Pos_y = (Resolution[1]/2) - self.FrameHeight*((Index+1) % 2)
                self.Rect = pygame.rect.Rect(self.Pos_x, self.Pos_y, self.FrameWidth, self.FrameHeight)
                if type(self.Frame) == type(None):
                    pygame.draw.rect(self.Image, (0,0,0),self.Rect)
                self.Draw_Buttons()
                # Stuff to draw the fps of the camera feed
                Frame_FPS = self.Drone.GetFrameFPS()
                FPS_Text = pygame.font.SysFont("Arial", 16).render(str(int(Frame_FPS)), False, pygame.Color("white"))
                self.Image.blit(FPS_Text, (0,0))
                # Stuff to draw the battery of the drone
                Battery_Level = self.Drone.GetBattery()
                Battery_Text = pygame.font.SysFont("Arial", 16).render(str(int(Battery_Level)), False, pygame.Color("red"))
                self.Image.blit(Battery_Text, (0,48))
                # Stuff to draw the flying status of the drone
                if self.Drone.GetFlying():
                    Flying_Text = pygame.font.SysFont("Arial", 16).render(("Flying"), False, pygame.Color("green"))
                else:
                    Flying_Text = pygame.font.SysFont("Arial", 16).render(("Flying"), False, pygame.Color("red"))
                self.Image.blit(Flying_Text, (0,96))
                Surface.blit(self.Image, self.Rect)

    # This function draws a camera when another camera is focused.
    # It only sets the rectangle to zero so that no click is detected on it
    def Camera_Unfocused(self):
        self.Rect = pygame.rect.Rect(0,0,0,0)

    # Detects if the mouse was placed on a certain place when it was clicked
    def Detect_Click(self, Mouse_Pos):
        # Checks if the mouse was over the entire camera rectangle
        if self.Rect.collidepoint(Mouse_Pos):
            # Detects if it was over the kill button. Sends emergency
            if self.Kill_Button.Click_Rect.collidepoint(Mouse_Pos):
                if self.Kill_Button.Color == (255,255,255):
                    return 0
                else:
                    self.Kill_Button.Update_Press_Time()
                    self.Drone.Emergency()
                    return 1
            # Detects if it was over the stop button. Sends land
            elif self.Stop_Button.Click_Rect.collidepoint(Mouse_Pos):
                if self.Stop_Button.Color == (255,255,255):
                    return 0
                else:
                    self.Stop_Button.Update_Press_Time()
                    self.Drone.Stop_Button_Command()
                    return 2
            # Detects if it was on the unfocus button, so it unfocuses the camera feed
            elif self.Unfocus_Button.Click_Rect.collidepoint(Mouse_Pos):
                self.Focused = False
                return 3
            # If it was on the camera, but not on any button, then it focuses the camera
            else:
                self.Focused = True
                return 69
        else:
            return 0

    # Runs the control handler of its corresponding drone
    def ControlHandler(self, KeyList, EventList, CD: dict):
        if self.Focused:
            self.Drone.ControlHandler(KeyList, EventList, CD)
        else:
            return


