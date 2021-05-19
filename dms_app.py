from hive.communication import CONN_TYPE_TCP, CONN_TYPE_UDP
from hive.communication.packet import HiveT, HiveU
from hive.communication.server import Server
from hive.dataBase.tableHandlers.route import Route
from hive.dataBase.tableHandlers.drone import Drone
from hive.dataBase.tableHandlers.getTable import fetchall
from time import sleep

class DmsServer(Server):
    def __init__(self):
        super().__init__(9000, 9241)
        self.seq_dic = {"cmd": 0, "state": 0, "video": 0}
        self.forsøg = 0

    def getKeysByValue(dictOfElements, valueToFind):
        listOfKeys = list()
        listOfItems = dictOfElements.items()
        for item  in listOfItems:
            if item[1] == valueToFind:
                listOfKeys.append(item[0])
        return  listOfKeys

    def eval_cmd(self, data, cmd_dict: dict):
        cmd = cmd_dict["CMD"]
        args = {}

        for key in cmd_dict.keys():
            if key != "CMD":
                args[key] = cmd_dict[key]

        if cmd == "ADD_DRONE":
            #pass
            droneList = [drone for drone, droneID in data.items()]
            droneIDList = [droneID for drone, droneID in data.items()]
            droneState = data['STATE']
            droneList = droneList[2:]
            droneIDList = droneIDList[2:]

            print(droneList)
            print(droneIDList)
            droneTableList = fetchall('hive.drone')
            counter = 0
            
            for i in range (len(droneList)):
                for j in range (len(droneTableList)):
                 
                    if droneTableList[j]['droneID'] == droneIDList[i]:
                        counter +=1
                        
                if (counter > 0):
                    print("<<Drone exists>>")
                    drone = Drone(droneList[i], droneIDList[i], droneState, 0.000000, 0.000000)
                    drone.update()
                else:
                    print("<<Drone does not exist>>")
                    drone = Drone(droneList[i], droneIDList[i], droneState, 0.000000, 0.000000)
                    drone.insert()
        
        if cmd == "UPDATE_DRONE":
            droneList = [drone for drone, droneID in data.items()]
            droneIDList = [droneID for drone, droneID in data.items()]
            droneState = data['STATE']
            droneList = droneList[2:]
            droneIDList = droneIDList[2:]
            for i in range (len(droneList)):
                drone = Drone(droneList[i], droneIDList[i], droneState, 0.000000, 0.000000)
                drone.update()
        if cmd == "QOS":
            pass
        if cmd == "GET_DRONE":
            pass

    def run(self, packet, conn, mode):
        if mode is CONN_TYPE_TCP:
            # TCP CODE HERE
            packet.dump()
            if packet.p_type == 0 or packet.p_type == 1:
                # Waypoint code here
                data = packet.data_parser()
                route = Route(packet.p_dest, packet.p_type, data)
                route.insert()
                conn.send(b"Succes")
            elif packet.p_type == 2:
                # Drone cmd code here
                pass
            elif packet.p_type == 3:
                # Server/client cmd code here
                cmd_dict = packet.data_parser()
                data = packet.data_parser()
                self.eval_cmd(data, cmd_dict)
                if (self.forsøg == 0):
                    dest = '192.168.137.171'
                    data = ["takeoff;land;"]
                    message = HiveT("drone", dest, data[self.forsøg])
                    message = HiveT.encode_packet(message)
                    print('Er det her det sker? forsøg {}'.format(self.forsøg))
                    self.forsøg += 1
                    print(message)
                    conn.send(message)
                """
                dest = '192.168.137.178'
                data = ["forsøg;1;","forsøg;2;","forsøg;3;","forsøg;4;"]
                message = HiveT("drone", dest, data[self.forsøg])
                message = HiveT.encode_packet(message)
                print('Er det her det sker? forsøg {}'.format(self.forsøg))
                self.forsøg += 1
                print(message)
                conn.send(message)
                """
            else:
                # Wrong packet type
                pass
        elif mode is CONN_TYPE_UDP:
            # UDP CODE HERE
            if packet.ptype == 0:
                # DRONE CMD
                if packet.seq < self.seq_dic["cmd"]:
                    pass

            elif packet.ptype == 1:
                # STATE STRING
                if packet.seq < self.seq_dic["state"]:
                    pass

            elif packet.ptype == 2:
                # VIDEO
                if packet.seq < self.seq_dic["video"]:
                    pass

            else:
                # Wrong packet type
                pass
            pass


if __name__ == "__main__":
    server = DmsServer()
    server.start()
