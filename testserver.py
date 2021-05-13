#!/usr/bin/env python3
from hive.communication.packet import HiveT, HiveU, Packet
from hive.communication.server_proto import Server


class TestServer(Server):
    def __init__(self):
        super().__init__(8888, 6060)

    def run(self, packet: Packet, conn, mode):
        packet.dump()
        print(self.router.dest_table)


if __name__ == "__main__":
    server = TestServer()

    server.start()
