import traceback, threading

from hive.communication import CONN_TYPE_TCP, CONN_TYPE_UDP
from hive.communication.client import Client
from hive.GUI.GUI_base import MainFrame

import hive.GUI_Camera_Module.DroneHandler as DH
from hive.GUI_Camera_Module.GameScreen import Game
from hive.communication.packet import HiveU

class OpcClientTCP(Client):
    def __init__(self, OPC_UDP):
        super().__init__("192.168.137.1", mode=CONN_TYPE_TCP, tcp_port=9000, other_client=OPC_UDP, name="OPC")
        #super().__init__("192.168.137.1", mode=CONN_TYPE_TCP, tcp_port=9000)

    def eval_cmd(self, cmd_dict: dict):
        print(f'eval_cmd: Command Dict is: {cmd_dict}')
        try:
            cmd = cmd_dict["CMD"]
            args = {}
        except KeyError:
            return

        for key in cmd_dict.keys():
            if key != "CMD":
                args[key] = cmd_dict[key]
        if cmd == "ADD_DRONE":
            pass
        if cmd == "QOS":
            pass
        if cmd == "GET_DRONE":
            print("I RECEIVED SOME DRONES")


    def run(self, packet: HiveU):
        packet.dump()

        if packet.p_type == 0 or packet.p_type == 1:
            # Enter route code here
                pass

        elif packet.p_type == 2:
                # Drone cmd code here
                pass
        elif packet.p_type == 3:
                # Server/client cmd code here
                print("\tGoing through data parser")
                cmd_dict = packet.data_parser()
                print(f'\tParsed dict is: {cmd_dict}')
                print("\tGone through data parser")
                #data = packet.data_parser()
                self.eval_cmd(cmd_dict)
                # pass
        else:
                # Wrong packet type
                pass
        #pass


class OpcClientUDP(Client):
    def __init__(self):
        super().__init__("192.168.137.1", mode=CONN_TYPE_UDP, udp_port=9241, name="OPC")
        self.LastSequence = 0

    def run(self, packet: HiveU):

        try:
            print(f'\t\tRun dump: {packet.ptype}, {packet.seq}, {packet.identifier}, {packet.data}')
            if packet.ptype == 2:
                #RPThread = threading.Thread(target=self.Receive_Packet, args=(packet.seq, packet.identifier, packet.data,))
                #RPThread.start()
                self.Receive_Packet(packet.seq, packet.identifier, packet.data)
        except AttributeError:
            return

    def Receive_Packet(self, Sequence, ID, Data):
        #print(f'Dumpy thingy from receive packet: {Sequence}, {ID}, {Data}')
        if Sequence <= self.LastSequence:
            return
        else:
            try:
                SendPort = int("22" + str(ID))
                self.client_sock.sendto(Data, ('127.0.0.1', SendPort))
                self.LastSequence = Sequence
            except OSError:
                print("OSError Caught")
                traceback.print_exc()
                return


def main():
    gui = MainFrame()
    OPC_UDP = OpcClientUDP()
    UDP_Start_Thread = threading.Thread(target=OPC_UDP.start)
    UDP_Start_Thread.start()
    OPC_TCP = OpcClientTCP(OPC_UDP)
    tcp_start_thread = threading.Thread(target=OPC_TCP.start)
    tcp_start_thread.start()
    gui.client = OPC_TCP
    gui.mainloop()

    OPC_TCP.send_message(3,"192.168.137.1", "CMD:GET_DRONE;")
    #UDP_Start_Thread = threading.Thread(target=OPC_UDP.start)
    #UDP_Start_Thread.start()
    #Handlers = [DH.DroneHandler(OPC_UDP, Tello_ID =36), DH.DroneHandler(OPC_UDP, Tello_ID =122)]
    Handlers = [DH.DroneHandler(OPC_UDP, Tello_ID=36)]
    MainGame = Game(Handlers)
    MainGame.Game_Loop()




if __name__ == "__main__":
    main()
