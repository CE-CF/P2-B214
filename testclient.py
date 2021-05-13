from hive.communication import CONN_TYPE_TCP, CONN_TYPE_UDP
from hive.communication.client import Client


class TestClient(Client):
    def __init__(self):
        super().__init__(
            "192.168.1.29",
            "TestClient",
            mode=CONN_TYPE_TCP,
            tcp_port=8888,
            udp_port=6060,
        )

    def run(self, packet):
        pass


if __name__ == "__main__":
    client = TestClient()

    client.start()
