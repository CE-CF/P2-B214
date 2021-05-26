from hive.communication import CONN_TYPE_TCP, CONN_TYPE_UDP
from hive.communication.client import Client
from time import time


class TestClient(Client):
    def __init__(self):
        super().__init__(
            "192.168.1.29",
            mode=CONN_TYPE_UDP,
            tcp_port=9000,
            udp_port=9241,
        )

    def qos_dms(self):
        self.send_message(3, self.srv_ip, f"CMD:QOS;SENT:{time()}")

    def qos_rb(self):
        self.send_message(3, "" , f"CMD:QOS;SENT:{time()}")
        

    def run(self, packet):
        


if __name__ == "__main__":
    client = TestClient()

    client.start()
