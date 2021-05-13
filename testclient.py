from hive.communication import CONN_TYPE_TCP, CONN_TYPE_UDP
from hive.communication.client import Client


class TestClient(Client):
    def __init__(self):
        super().__init__(
            "192.168.1.29",
            mode=CONN_TYPE_TCP,
            tcp_port=8888,
            udp_port=6060,
        )

    def run(self, packet):
        buf = input("Write something: ")
        target = input("Target ip: ")
        self.send_message(0, target, buf)


if __name__ == "__main__":
    client = TestClient()

    client.start()
