import DroneHandler as DH
from GameScreen import Game

if __name__ == '__main__':
    DH = DH.DroneHandler()
    #DH = DH.DroneHandler(False, '192.168.0.33')
    MainGame = Game(DH)
    MainGame.Game_Loop()
