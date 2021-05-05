from CameraButton import CameraButton
import pygame
import cv2

class CameraWindow:



    #def __init__(self, Drone, Resolution, No_Of_Cameras):
    def __init__(self, Drone):
        self.Buttons = self.Kill_Button, self.Stop_Button, self.Unfocus_Button = (CameraButton(), CameraButton(), CameraButton())
        #self.No_Of_Cameras = No_Of_Cameras
        #self.Resolution = Resolution
        self.Drone = Drone
        self.Focused = False
        #self.FrameWidth = 960
        #self.FrameHeight = 720
        """
        self.Frame = Drone.GetFrame()
        self.FrameWidth = 960
        self.FrameHeight = 720
        self.FrameRatio = 1
        if self.Resolution[0] < 960 or self.Resolution[1] < 720:
                self.FrameRatio = min((self.Resolution[0]/920), (self.Resolution[1]/720))
                self.FrameHeight =int(self.FrameHeight*self.FrameRatio)
                self.FrameWidth = int(self.FrameWidth*self.FrameRatio)
                self.Frame = cv2.resize(self.Frame,(self.FrameWidth,self.FrameHeight))
        self.Image = pygame.image.frombuffer(self.Frame, (self.FrameWidth, self.FrameHeight), "BGR")
        """

    #def Draw_Buttons(self, Image, FrameRatio, Pos_x, Pos_y, FrameWidth, FrameHeight):
    def Draw_Buttons(self):
        self.Kill_Button.Rect = pygame.Rect(0,0,int(110*self.FrameRatio),int(64*self.FrameRatio))
        self.Kill_Button.Rect.topright = ((self.Pos_x + self.FrameWidth), self.Pos_y)
        self.Kill_Button.Font = pygame.font.SysFont("Calibri", int(60*self.FrameRatio))
        self.Kill_Button.Text = self.Kill_Button.Font.render("Kill!!", True, pygame.Color("red"))
        pygame.draw.rect(self.Image,self.Kill_Button.Color, self.Kill_Button.Rect)
        self.Image.blit(self.Kill_Button.Text, self.Kill_Button.Rect)
        self.Stop_Button.Rect = pygame.Rect(0,0,int(110*self.FrameRatio),int(64*self.FrameRatio))
        self.Stop_Button.Rect.bottomleft = (self.Pos_x, (self.Pos_y + self.FrameHeight))
        self.Stop_Button.Font = pygame.font.SysFont("Calibri", int(60*self.FrameRatio))
        self.Stop_Button.Text = self.Stop_Button.Font.render("Stop", True, pygame.Color("red"))
        pygame.draw.rect(self.Image,self.Stop_Button.Color, self.Stop_Button.Rect)
        self.Image.blit(self.Stop_Button.Text, self.Stop_Button.Rect)
        self.Unfocus_Button.Rect = pygame.Rect(0,0,0,0)
        if self.Focused:
            self.Unfocus_Button.Rect = pygame.Rect(0, 0, int(32*self.FrameRatio), int(54*self.FrameRatio))
            self.Unfocus_Button.Rect.topleft = (self.Pos_x, self.Pos_y)
            self.Unfocus_Button.Font = pygame.font.SysFont("Calibri", int(60*self.FrameRatio))
            self.Unfocus_Button.Text = self.Kill_Button.Font.render("X", True, pygame.Color("red"))
            pygame.draw.rect(self.Image, self.Unfocus_Button.Color, self.Unfocus_Button.Rect)
            self.Image.blit(self.Unfocus_Button.Text, self.Unfocus_Button.Rect)


    def Draw_Camera(self, Surface, Camera_Index, Camera_Scroll, Resolution, No_Of_Cameras, FullScreen = False):
        self.FrameWidth = 960; self.FrameHeight = 720
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
            Battery_Level = self.Drone.GetBattery()
            Battery_Text = pygame.font.SysFont("Arial", 16).render(str(int(Battery_Level)), False, (255,255,255))
            self.Image.blit(Battery_Text, (0,(self.Pos_y + 48)))
            Surface.blit(self.Image, self.Rect)
            #Surface.blit(self.Image, (self.Pos_x, self.Pos_y))
        else:
            if No_Of_Cameras > 4:
                if (Camera_Index-2*Camera_Scroll)>=0 and (Camera_Index-2*Camera_Scroll)<4:
                    self.Frame = self.Drone.GetFrame()
                    self.FrameHeight = int(self.FrameHeight*self.FrameRatio/2)
                    self.FrameWidth = int(self.FrameWidth*self.FrameRatio/2)
                    self.Frame = cv2.resize(self.Frame,(self.FrameWidth,self.FrameHeight))
                    self.Image = pygame.image.frombuffer(self.Frame, (self.FrameWidth, self.FrameHeight), "BGR")
                    Index = Camera_Index - 2*Camera_Scroll
                    self.Pos_x = (Resolution[0]/2) - self.FrameWidth*(1 - (Index // 2))
                    self.Pos_y = (Resolution[1]/2) - self.FrameHeight*((Index+1) % 2)
                    self.Rect = pygame.rect.Rect(self.Pos_x, self.Pos_y, self.FrameWidth, self.FrameHeight)
                    self.Draw_Buttons()
                    Battery_Level = self.Drone.GetBattery()
                    Battery_Text = pygame.font.SysFont("Arial", 16).render(str(int(Battery_Level)), False, (255,255,255))
                    self.Image.blit(Battery_Text, (0,(self.Pos_y + 48)))
                    Surface.blit(self.Image, self.Rect)
                    #Surface.blit(self.Image, (self.Pos_x, self.Pos_y))
                else:
                    self.Rect = pygame.rect.Rect(0,0,0,0)
            else:
                self.Frame = self.Drone.GetFrame()
                self.FrameHeight = int(self.FrameHeight*self.FrameRatio/2)
                self.FrameWidth = int(self.FrameWidth*self.FrameRatio/2)
                #print(f'\tFrame width is: {self.FrameWidth}\n\tFrame height is: {self.FrameHeight}')
                self.Frame = cv2.resize(self.Frame,(self.FrameWidth,self.FrameHeight))
                self.Image = pygame.image.frombuffer(self.Frame, (self.FrameWidth, self.FrameHeight), "BGR")
                Index = Camera_Index - 2*Camera_Scroll
                self.Pos_x = (Resolution[0]/2) - self.FrameWidth*((Index // 2) + 1)
                self.Pos_y = (Resolution[1]/2) - self.FrameHeight*((Index+1) % 2)
                self.Rect = pygame.rect.Rect(self.Pos_x, self.Pos_y, self.FrameWidth, self.FrameHeight)
                self.Draw_Buttons()
                Battery_Level = self.Drone.GetBattery()
                Battery_Text = pygame.font.SysFont("Arial", 16).render(str(int(Battery_Level)), False, (255,255,255))
                self.Image.blit(Battery_Text, (0,(self.Pos_y + 48)))
                Surface.blit(self.Image, self.Rect)
                #Surface.blit(self.Image, (self.Pos_x, self.Pos_y))\

    def Camera_Unfocused(self):
        self.Rect = pygame.rect.Rect(0,0,0,0)

    def Detect_Click(self, Mouse_Pos):
        if self.Rect.collidepoint(Mouse_Pos):
            if self.Kill_Button.Rect.collidepoint(Mouse_Pos):
                if self.Kill_Button.Color == (255,255,255):
                    return 0
                else:
                    self.Kill_Button.Update_Press_Time()
                    self.Drone.Emergency()
                    return 1
            elif self.Stop_Button.Rect.collidepoint(Mouse_Pos):
                if self.Stop_Button.Color == (255,255,255):
                    return 0
                else:
                    self.Stop_Button.Update_Press_Time()
                    self.Drone.Stop_Button_Command()
                    return 2
            elif self.Unfocus_Button.Rect.collidepoint(Mouse_Pos):
                self.Focused = False
                return 3
            else:
                self.Focused = True
                return 69
        else:
            return 0

    def ControlHandler(self, KeyList, EventList, CD: dict):
        if self.Focused:
            self.Drone.ControlHandler(KeyList, EventList, CD)
        else:
            return


