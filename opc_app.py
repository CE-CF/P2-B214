from hive.communication import CONN_TYPE_TCP, CONN_TYPE_UDP
from hive.communication.client import Client
from hive.GUI.GUI_base import MainFrame


class OpcClientTCP(Client):
    def __init__(self):
        super().__init__("127.0.0.1", mode=CONN_TYPE_TCP, tcp_port=9000)

    def run(self, packet):
        pass


class OpcClientUDP(Client):
    def __init__(self):
        super().__init__("127.0.0.1", mode=CONN_TYPE_UDP, udp_port=9241)

    def run(self, packet):
        pass


def main():
    gui = MainFrame()
    gui.client = OpcClientTCP()
    gui.client.start()
    gui.mainloop()


if __name__ == "__main__":
    main()
