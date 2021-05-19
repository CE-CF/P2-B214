import DroneHandler as DH
from GameScreen import Game
from VideoSorter import VideoSorter

if __name__ == '__main__':
    VS = VideoSorter()
    VS.start()
    DH = [DH.DroneHandler(Tello_ID =222)]
    MainGame = Game(DH, VS)
    MainGame.Game_Loop()
