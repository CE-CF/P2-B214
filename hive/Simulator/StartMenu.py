import tkinter
import Global_Constants as GC

class StartMenu():

    def __init__(self):
        # The resolution values that can be chosen from
        self.Resolution_Values = [(640, 480), (1080, 640), (1600, 900), (1920, 1080)]
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
    def Change_FPS(self, FPS):
        try:
            GC.FPS = int(FPS)
            print(f'FPS changed to {GC.FPS}')
        except TypeError or ValueError:
            GC.FPS = 60
            print("Type or Value Error. FPS is now 60")
    #
    def Change_TelloMode(self):
        GC.TelloMode = self.TelloMode_Bool.get()
        print(f'Tello mode is: {GC.TelloMode}')
    # Changes the full screen boolean according the full screen tick box
    def Change_FullScreen(self):
        GC.FullScreen = self.FullScreen_Bool.get()
        print(f'Full screen is: {GC.FullScreen}')
    # Changes the speed according to the spinbox.
    # Initiated only when up or down arrow are used in the spinbox
    def Change_Speed(self):
        GC.Uniform_Drones_Speed = float(self.Speed_Spinbox.get())*10
        print(f'Speed is: {GC.Uniform_Drones_Speed}')
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
        self.FullScreen_Bool = tkinter.BooleanVar()
        self.FullScreen_Bool.set(False)
        self.Speed = tkinter.DoubleVar()
        self.Speed.set(1)
        self.Run_Bool = False

        TelloMode_Checkbox = tkinter.Checkbutton(Main_Frame, text = "Tello Mode", variable = self.TelloMode_Bool,
                                                 offvalue = False, onvalue = True, command = self.Change_TelloMode)
        FullScreen_Checkbox = tkinter.Checkbutton(Main_Frame, text = "Full Screen", variable = self.FullScreen_Bool,
                                                  offvalue = False, onvalue = True, command = self.Change_FullScreen)
        Resolution_Label = tkinter.Label(Resolution_Frame, text="Resolution")
        Resolution_Option = tkinter.OptionMenu(Resolution_Frame, Resolution, *self.Resolution_List,
                                               command = self.Change_Resolution)
        FPS_Label = tkinter.Label(FPS_Frame, text="Frames Per Second")
        FPS_Option = tkinter.OptionMenu(FPS_Frame, FPS, *self.FPS_Values, command = self.Change_FPS)
        Speed_Label = tkinter.Label(Speed_Frame, text="Drone's Speed")
        self.Speed_Spinbox = tkinter.Spinbox(Speed_Frame,text="Speed", from_=0, to=10, increment=0.1,
                                             width=5, command = self.Change_Speed)
        Run_Button = tkinter.Button(Main_Frame, text = "Run", command = self.Run_Game)
        # Following lines pack the frames and widgets
        Main_Frame.pack()
        Speed_Frame.pack()
        Speed_Label.pack(side=tkinter.LEFT)
        self.Speed_Spinbox.pack(side=tkinter.RIGHT)
        Resolution_Frame.pack()
        Resolution_Label.pack(side=tkinter.LEFT)
        Resolution_Option.pack(side=tkinter.RIGHT)
        FPS_Frame.pack()
        FPS_Label.pack(side=tkinter.LEFT)
        FPS_Option.pack(side=tkinter.RIGHT)
        TelloMode_Checkbox.pack()
        FullScreen_Checkbox.pack()
        Run_Button.pack()
        print("Entering menu main loop")
        self.root.mainloop()                # Start tkinter GUI loop
        print("Exiting menu main loop")
        return self.Run_Bool                # Return the Run boolean when the loop is closed
