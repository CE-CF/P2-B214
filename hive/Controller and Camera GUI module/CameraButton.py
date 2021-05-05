import pygame
import time

class CameraButton:

    def __init__(self):
        self.Press_Time = time.time()
        self.Rect = pygame.rect.Rect(0,0,110,64)
        self.Font = pygame.font.SysFont("Calibri", int(60))
        self.Text = self.Font.render("????", True, pygame.Color("red"))
        self.Color = pygame.Color("black")

    def Update_Color(self):
        if (time.time() - self.Press_Time) < 5000:
            self.Color = (255,255,255)
        else:
            self.Color = (0,0,0)

    def Update_Press_Time(self):
        self.Press_Time = time.time()
