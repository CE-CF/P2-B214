#!/usr/bin/env python3
from hive.communication.packet import HiveT, HiveU, Packet
from hive.communication.server import Server
from time import sleep


class TestServer(Server):
    def __init__(self):
        super().__init__(9000, 9241)
        self.dest = '192.168.137.103'
        self.data = 'forward 50; turn r;'
        self.data2 = 'Spis ild; Tobias;'


    def run(self, packet: Packet, conn, mode):
        packet.dump()
        print(self.router.dest_table)
        sleep(10)
        message = HiveT("drone", self.dest, self.data)
        message = HiveT.encode_packet(message)
        conn.send(message)
        sleep(5)
        message2 = HiveT("drone", self.dest, self.data2)
        message2 = HiveT.encode_packet(message2)
        conn.send(message2)
        
if __name__ == "__main__":
    server = TestServer()

    server.start()
