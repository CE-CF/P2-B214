import djitellopy as dji
import threading
import pygame

class DroneHandler:

    def __init__(self, Tello_IP = "192.168.10.1"):
        self.IP_Address = Tello_IP
        print(f'IP Address is: {Tello_IP}, {self.IP_Address}')
        self.Drone = dji.Tello()

        self.Controllable = False
        self.ControllerMode = False
        self.RC_Mode = True
        self.Move_Speed = 50
        self.Yaw_Speed = 80
        self.Drone.connect()
        self.Drone.streamon()
        self.Drone.send_rc_control(0,0,0,0)
        self.Frame = self.Drone.get_frame_read()
        self.Control_Dict = {"land":    pygame.K_SPACE, "takeoff":  pygame.K_SPACE,
                             "up":      pygame.K_UP,    "down":     pygame.K_DOWN,
                             "cw":      pygame.K_RIGHT, "ccw":      pygame.K_LEFT,
                             "forward": pygame.K_w,     "backward": pygame.K_s,
                             "right":   pygame.K_d,     "left":     pygame.K_a,
                             "flipf":   pygame.K_KP8,   "flipb":    pygame.K_KP5,
                             "flipr":   pygame.K_KP6,   "flipl":    pygame.K_KP4,
                             "rc":      pygame.K_r,
                             "stop":    pygame.K_p,     "emergency":pygame.K_o     }

    # Give the frame from the drone
    def GetFrame(self):
        return self.Frame.frame
    # Give the battery status from the drone
    def GetBattery(self):
        return self.Drone.get_battery()
    def GetFlying(self):
        return self.Drone.is_flying
    def Emergency(self, Stop:bool = False):
        if Stop:
            #self.Drone.send_control_command("stop")
            Stop_Command_Thread = threading.Thread(target=self.Drone.send_control_command, args=("stop",))
            Stop_Command_Thread.start()
        else:
            #self.Drone.emergency()
            Emergency_Thread = threading.Thread(target=self.Drone.emergency)
            Emergency_Thread.start()
    def Connect_Network(self, SSID, Pass):
        self.Drone.connect_to_wifi(SSID, Pass)
        Wifi_Connect_Thread = threading.Thread(target=self.Drone.connect_to_wifi, args=("ssid", "pass",))
    def Stop_Button_Command(self):
        if self.Drone.is_flying:
            Land_Thread = threading.Thread(target=self.Drone.land)
            Land_Thread.start()
            #self.Drone.land()
        #self.Stop()
    # Stop the drone
    def Stop(self):
        End_Thread = threading.Thread(target=self.Drone.end)
        End_Thread.start()
        #self.Drone.end()
