import DroneHandler as DH
from GameScreen import Game
from VideoSorter import VideoSorter

def main(OPC_UDP):
    VS = VideoSorter()
    VS.start()
    Handlers = [DH.DroneHandler(OPC_UDP, Tello_ID =222)]
    MainGame = Game(Handlers, VS)
    MainGame.Game_Loop()

"""
if __name__ == '__main__':
    VS = VideoSorter()
    VS.start()
    DH = [DH.DroneHandler(Tello_ID =222)]
    MainGame = Game(DH, VS)
    MainGame.Game_Loop()
"""
