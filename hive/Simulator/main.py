#ScreenSize = ScreenHeight, ScreenWidth = 1080, 640

#import Camera
import Global_Constants as GC
import StartMenu
import MyGame

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#MainGame = MyGame.Game()

def main():
    #global MainGame
    Menu = StartMenu.StartMenu()
    Menu.setup()
    Run_Game = Menu.run()
    if Run_Game:
        #MyGame.Game.init(1920, 1080, True)
        MainGame = MyGame.Game(GC.ScreenWidth, GC.ScreenHeight, GC.FullScreen)
        MainGame.Game_Loop()
        #MyGame.Game.Game_Loop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
