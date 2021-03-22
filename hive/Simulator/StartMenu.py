import tkinter
import Global_Constants as GC

class StartMenu():

    def __init__(self):
        self.Resolution_Values = [(640, 480), (1080, 640), (1600, 900), (1920, 1080)]

    def Creat_Resolution_Lists(self, Resolution_Values):
        Resolution_List = []
        Resolution_Dict = {}
        for i in range(len(Resolution_Values)):
            Resolution_List.append(f'{Resolution_Values[i][0]} x {Resolution_Values[i][1]}')
            Resolution_Dict[Resolution_List[i]] = Resolution_Values[i]
        return Resolution_List, Resolution_Dict

    def setup(self):

        self.Resolution_List, self.Resolution_Dict = self.Creat_Resolution_Lists(self.Resolution_Values)
        print(self.Resolution_List)
        print(self.Resolution_Dict)


    def Change_Resolution(self, Resolution):
            print(f'Resolution is: {Resolution}')
            print(self.Resolution_Dict.get(Resolution))
            GC.ScreenSize = GC.ScreenWidth, GC.ScreenHeight = self.Resolution_Dict.get(Resolution)

            print(f'ScreenSize is: {GC.ScreenSize}')
            print(f'ScreenWidth is: {GC.ScreenWidth}')
            print(f'ScreenHeight is: {GC.ScreenHeight}')

    def Change_FullScreen(self):
        GC.FullScreen = self.FullScreen_Bool.get()
        print(f'Full screen is: {GC.FullScreen}')

    def Run_Game(self):
        print("Run button has been pressed")
        self.Run_Bool = True
        self.root.destroy()


    def run(self):
        self.root = tkinter.Tk()
        Main_Frame = tkinter.Frame(self.root)

        Resolution = tkinter.StringVar(Main_Frame)
        Resolution.set(self.Resolution_List[0])
        self.FullScreen_Bool = tkinter.BooleanVar()
        self.FullScreen_Bool.set(False)
        self.Run_Bool = False

        FullScreen_Checkbox = tkinter.Checkbutton(Main_Frame, text = "Full Screen", variable = self.FullScreen_Bool,
                                                  offvalue = False, onvalue = True, command = self.Change_FullScreen)
        Resolution_Option = tkinter.OptionMenu(Main_Frame, Resolution, *self.Resolution_List, command = self.Change_Resolution)

        Run_Button = tkinter.Button(Main_Frame, text = "Run", command = self.Run_Game)

        Main_Frame.pack()
        Resolution_Option.pack()
        FullScreen_Checkbox.pack()
        Run_Button.pack()
        print("Entering menu main loop")
        self.root.mainloop()
        print("Exiting menu main loop")
        return self.Run_Bool
