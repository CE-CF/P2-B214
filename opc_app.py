import traceback, threading

from hive.communication import CONN_TYPE_TCP, CONN_TYPE_UDP
from hive.communication.client import Client
from hive.GUI.GUI_base import MainFrame

import hive.GUI_Camera_Module.DroneHandler as DH
from hive.GUI_Camera_Module.GameScreen import Game
from hive.communication.packet import HiveU


class OpcClientTCP(Client):
    def __init__(self, OPC_UDP):
        super().__init__("127.0.0.1", mode=CONN_TYPE_TCP, tcp_port=9000, other_client=OPC_UDP)

    def run(self, packet):
        pass


class OpcClientUDP(Client):
    def __init__(self):
        super().__init__("127.0.0.1", mode=CONN_TYPE_UDP, udp_port=9241)
        self.LastSequence = 0

    def run(self, packet: HiveU):

        try:
            if packet.ptype == 2:
                #RPThread = threading.Thread(target=self.Receive_Packet, args=(packet.seq, packet.identifier, packet.data,))
                #RPThread.start()
                self.Receive_Packet(packet.seq, packet.identifier, packet.data)
        except AttributeError:
            return

    def Receive_Packet(self, Sequence, ID, Data):
        if Sequence == self.LastSequence:
            return
        else:
            try:
                SendPort = int("22" + ID)
                self.client_sock.sendto(Data, ('127.0.0.1', SendPort))
                self.LastSequence = Sequence
            except OSError:
                print("OSError Caught")
                traceback.print_exc()
                return


def main():
    gui = MainFrame()
    OPC_UDP = OpcClientUDP()
    gui.client = OpcClientTCP(OPC_UDP)
    tcp_start_thread = threading.Thread(target=gui.client.start)
    tcp_start_thread.start()
    gui.mainloop()

    UDP_Start_Thread = threading.Thread(target=OPC_UDP.start)
    UDP_Start_Thread.start()
    Handlers = [DH.DroneHandler(OPC_UDP, Tello_ID =222), DH.DroneHandler(OPC_UDP, Tello_ID =122)]
    MainGame = Game(Handlers)
    MainGame.Game_Loop()




if __name__ == "__main__":
    main()
