import DroneHandler as DH
from GameScreen import Game

if __name__ == '__main__':
    DH = DH.DroneHandler()
    MainGame = Game(DH)
    MainGame.Game_Loop()
