from hive.communication.server import Server
from hive.communication import CONN_TYPE_TCP, CONN_TYPE_UDP


class DmsServer(Server):
    def __init__(self):
        super().__init__(1337, 9241)

    def run(self, packet, mode):
        packet.dump()


if __name__ == "__main__":
    server = DmsServer()
    server.start()
