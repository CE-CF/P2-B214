import tkinter
import Global_Constants as GC

"""Tkinter menu that changes the options and parameters in Global_Constants"""

class StartMenu():

    def __init__(self):
        # The resolution and FPS values that can be chosen from
        self.Resolution_Values = [(640, 480), (1080, 640), (1280, 720), (1600, 900), (1920, 1080)]
        self.FPS_Values = ('30', '60', '120', '240')

    # Makes the list and dictionary that are used to change the resolution of the simulator
    def Creat_Resolution_Lists(self, Resolution_Values):    # Argument(An n by 2 list with the wanted resolutions)
        Resolution_List = []
        Resolution_Dict = {}
        for i in range(len(Resolution_Values)):
            # List contains the resolutions as strings ("Width x Height")
            Resolution_List.append(f'{Resolution_Values[i][0]} x {Resolution_Values[i][1]}')
            # Dict format: (Resolution string: Resolution tuple)
            Resolution_Dict[Resolution_List[i]] = Resolution_Values[i]
        return Resolution_List, Resolution_Dict

    # Setup function for the start menu
    def setup(self):
        self.Resolution_List, self.Resolution_Dict = self.Creat_Resolution_Lists(self.Resolution_Values)
        print(self.Resolution_List)
        print(self.Resolution_Dict)

    # Function that changes the resolution.
    # Called when a resolution is selected in the option menu
    def Change_Resolution(self, Resolution):    # Argument(The chosen resolution. A string of format "Width x Height"
            print(f'Resolution is: {Resolution}')
            print(self.Resolution_Dict.get(Resolution))
            GC.ScreenSize = GC.ScreenWidth, GC.ScreenHeight = self.Resolution_Dict.get(Resolution)
            print(f'ScreenSize is: {GC.ScreenSize}')
            print(f'ScreenWidth is: {GC.ScreenWidth}')
            print(f'ScreenHeight is: {GC.ScreenHeight}')

    # Called when FPS is changed to change the FPS value in GC
    def Change_FPS(self, FPS):
        try:
            GC.FPS = int(FPS)
            print(f'FPS changed to {GC.FPS}')
        except TypeError or ValueError:
            GC.FPS = 60
            print("Type or Value Error. FPS is now 60")

    # Changes Tello mode when the tickbox is changed
    def Change_TelloMode(self):
        GC.TelloMode = self.TelloMode_Bool.get()
        print(f'Tello mode is: {GC.TelloMode}')

    # Changes if the position is sent in the Tello state when the PosMode tickbox is changed
    def Change_PosMode(self):
        GC.PosMode = self.PosMode_Bool.get()
        print(f'GPS mode is: {GC.TelloMode}')

    # Changes the full screen boolean according the full screen tick box
    def Change_FullScreen(self):
        GC.FullScreen = self.FullScreen_Bool.get()
        print(f'Full screen is: {GC.FullScreen}')

    # Changes the boolean to draw the path of the drones according to its tickbox
    def Change_DrawPath(self):
        GC.Draw_Path = self.DrawPath_Bool.get()
        print(f'Draw path is: {GC.Draw_Path}')

    """This is changed"""
    # Changes the speed according to the spinbox.
    # Initiated only when up or down arrow are used in the spinbox
    #def Change_Speed(self):
    #    GC.Uniform_Drones_Speed = int(self.Speed_Spinbox.get())
    #    print(f'Speed is: {GC.Uniform_Drones_Speed}')

    # Update the drone linear speed when the scale is changed
    def Change_Speed(self, Speed):
        GC.Uniform_Drones_Speed = int(Speed)
        print(f'Speed is: {GC.Uniform_Drones_Speed}')

    # Update the drone rotation speed when the scale is changed
    def Change_Yaw(self, Speed):
        GC.Uniform_Yaw_Speed = Speed
        print(f'Yaw Speed is: {GC.Uniform_Yaw_Speed}')

    # Changes the number of spawned drones in Tello Mode
    def Change_Drone_Number(self):
        GC.Drone_Number = int(self.Drone_Number_Spinbox.get())
        print(f'Number of Tello drones is: {GC.Drone_Number}')

    # Sets the boolean that tells the main function to run the game
    # Called when the run button is pressed. It destroys the start menu
    def Run_Game(self):
        print("Run button has been pressed")
        self.Run_Bool = True
        self.root.destroy()

    # The main run function of the menu
    def run(self):
        self.root = tkinter.Tk()                        # Create main tkinter window
        Main_Frame = tkinter.Frame(self.root)           # Create a frame inside the root window
        Speed_Frame = tkinter.Frame(Main_Frame)         # Create a frame for the speed spinbox inside the main frame
        Yaw_Frame = tkinter.Frame(Main_Frame)
        Drone_Number_Frame = tkinter.Frame(Main_Frame)
        Resolution_Frame = tkinter.Frame(Main_Frame)
        FPS_Frame = tkinter.Frame(Main_Frame)
        # Tkinter widgets use tkinter objects that have to be created
        # These following line create the objects for each of the widgets and sets them
        Resolution = tkinter.StringVar(Main_Frame)
        Resolution.set(self.Resolution_List[1])
        FPS = tkinter.StringVar(Main_Frame)
        FPS.set(self.FPS_Values[1])
        self.TelloMode_Bool = tkinter.BooleanVar()
        self.TelloMode_Bool.set(False)
        self.PosMode_Bool = tkinter.BooleanVar()
        self.PosMode_Bool.set(False)
        self.FullScreen_Bool = tkinter.BooleanVar()
        self.FullScreen_Bool.set(False)
        self.DrawPath_Bool = tkinter.BooleanVar()
        self.DrawPath_Bool.set(False)
        #self.Speed = tkinter.DoubleVar()
        #self.Speed.set(1)
        self.Run_Bool = False

        TelloMode_Checkbox = tkinter.Checkbutton(Main_Frame, text = "Tello Mode", variable = self.TelloMode_Bool,
                                                 offvalue = False, onvalue = True, command = self.Change_TelloMode)
        PosMode_Checkbox = tkinter.Checkbutton(Main_Frame, text = "GPS Mode", variable = self.PosMode_Bool,
                                                 offvalue = False, onvalue = True, command = self.Change_PosMode)
        FullScreen_Checkbox = tkinter.Checkbutton(Main_Frame, text = "Full Screen", variable = self.FullScreen_Bool,
                                                  offvalue = False, onvalue = True, command = self.Change_FullScreen)
        DrawPath_Checkbox = tkinter.Checkbutton(Main_Frame, text = "Draw Drones' Path", variable = self.DrawPath_Bool,
                                                  offvalue = False, onvalue = True, command = self.Change_DrawPath)
        Resolution_Label = tkinter.Label(Resolution_Frame, text="Resolution")
        Resolution_Option = tkinter.OptionMenu(Resolution_Frame, Resolution, *self.Resolution_List,
                                               command = self.Change_Resolution)
        FPS_Label = tkinter.Label(FPS_Frame, text="Frames Per Second")
        FPS_Option = tkinter.OptionMenu(FPS_Frame, FPS, *self.FPS_Values, command = self.Change_FPS)
        #Speed_Label = tkinter.Label(Speed_Frame, text="Drone's Speed            ")
        Speed_Label = tkinter.Label(Speed_Frame, text="Drones' Speed    ")
        #self.Speed_Spinbox = tkinter.Spinbox(Speed_Frame,text="Speed", from_=1, to=30, increment=1,
        #                                     width=5, command = self.Change_Speed)
        Speed_Scale = tkinter.Scale(Speed_Frame, from_=1, to=200, orient=tkinter.HORIZONTAL, command=self.Change_Speed)
        Yaw_Label = tkinter.Label(Yaw_Frame, text="Drones' Rotation")
        Yaw_Scale = tkinter.Scale(Yaw_Frame, from_=1, to=200, orient=tkinter.HORIZONTAL, command=self.Change_Yaw)
        Drone_Number_Label = tkinter.Label(Drone_Number_Frame, text="No. of Drones            ")
        self.Drone_Number_Spinbox = tkinter.Spinbox(Drone_Number_Frame,text="No. of Drones", from_=1, to=10, increment=1,
                                                    width=5, command = self.Change_Drone_Number)
        Run_Button = tkinter.Button(Main_Frame, text = "Run", command = self.Run_Game)

        # Following lines pack the frames and widgets
        Main_Frame.pack()
        Speed_Frame.pack()
        Speed_Label.pack(side=tkinter.LEFT)
        #self.Speed_Spinbox.pack(side=tkinter.RIGHT)
        Speed_Scale.pack(side=tkinter.RIGHT)
        Yaw_Frame.pack()
        Yaw_Label.pack(side=tkinter.LEFT)
        Yaw_Scale.pack(side=tkinter.RIGHT)
        Drone_Number_Frame.pack()
        Drone_Number_Label.pack(side=tkinter.LEFT)
        self.Drone_Number_Spinbox.pack(side=tkinter.RIGHT)
        Resolution_Frame.pack()
        Resolution_Label.pack(side=tkinter.LEFT)
        Resolution_Option.pack(side=tkinter.RIGHT)
        FPS_Frame.pack()
        FPS_Label.pack(side=tkinter.LEFT)
        FPS_Option.pack(side=tkinter.RIGHT)
        TelloMode_Checkbox.pack()
        PosMode_Checkbox.pack()
        FullScreen_Checkbox.pack()
        DrawPath_Checkbox.pack()
        Run_Button.pack()

        print("Entering menu main loop")
        self.root.mainloop()                # Start tkinter GUI loop
        print("Exiting menu main loop")
        return self.Run_Bool                # Return the Run boolean when the loop is closed
