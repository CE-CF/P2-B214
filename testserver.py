#!/usr/bin/env python3
from typing import ForwardRef
from hive.communication.packet import HiveT, HiveU, Packet
from hive.communication.server import Server
from hive.dataBase.tableHandlers.getTable import fetchall
from time import sleep


class TestServer(Server):
    def __init__(self):
        super().__init__(9000, 9241, srv_ip="192.168.137.1")
        self.dest = '192.168.137.59'
        
    def run(self, packet: Packet, conn, mode):
        packet.dump()
        print(self.router.dest_table)
        droneTableList = fetchall('hive.drone')
        getDroneStr = "CMD:GET_DRONE;"
        for x in range (len(droneTableList)):
            print(droneTableList[x]['drone'])
            print(droneTableList[x]['droneID'])
        getDroneStr += droneTableList[x]['drone']+":"+droneTableList[x]['droneID']+";"
        message = HiveT.encode_packet(HiveT("sccmd", self.dest, getDroneStr))
        conn.send(message)
        
        
if __name__ == "__main__":
    server = TestServer()

    server.start()
