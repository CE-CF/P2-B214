import DroneHandler as DH
from GameScreen import Game
from VideoSorter import VideoSorter

if __name__ == '__main__':
    VS = VideoSorter()
    VS.start()
    DH = [DH.DroneHandler()]
    #DH = [DH.DroneHandler('192.168.0.177')]
    #DH = [DH.DroneHandler(Tello_IP ='192.168.137.52')]
    #DH = [DH.DroneHandler('192.168.137.115'), DH.DroneHandler('192.168.137.171')]
    print("Attempting DH1")
    #DH1 = DH.DroneHandler('192.168.137.103')
    print("Attempting DH2")
    #DH2 = DH.DroneHandler('192.168.137.223')
    print("Attempting DH3")
    #MainGame = Game([DH1, DH2])
    #MainGame = Game([DH1])
    MainGame = Game(DH, VS)
    #MainGame = Game(DH, 360, 240)
    MainGame.Game_Loop()
    #VS.Finish()
