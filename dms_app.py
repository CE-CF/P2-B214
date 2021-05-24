from hive.communication import CONN_TYPE_TCP, CONN_TYPE_UDP
from hive.communication.packet import HiveT, HiveU
from hive.communication.server import Server
from hive.dataBase.tableHandlers.route import Route
from hive.dataBase.tableHandlers.drone import Drone
from hive.dataBase.tableHandlers.getTable import fetchall
from time import sleep

class DmsServer(Server):
    def __init__(self):
        super().__init__(9000, 9241, srv_ip="192.168.137.1") #, srv_ip="192.168.137.1"
        self.seq_dic = {"cmd": 0, "state": 0, "video": 0}
        self.hotSpotIP = "192.168.137"  # First 3 octets of the hotspot IP
        self.forsøg = 0

    def data_parser_battery(self, data):
        """Parse incoming packet data for easier manipulation
        :param data:
        :type data: str
        :returns: Dictionary containing data
        """
        d = {}
        delim1 = ";"
        delim2 = ":"
        element = ""
        for _, v in enumerate(data):
            if v is not delim1:
                element += v
            else:
                arr = element.split(delim2)
                d[arr[0]] = arr[1]
                element = ""

        return d["bat"]

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
            droneTableList = fetchall('hive.drone')
            counter = 0
            
            for i in range (len(droneList)):
                for j in range (len(droneTableList)):
                 
                    if droneTableList[j]['droneID'] == droneIDList[i]:
                        counter +=1
                        
                if (counter > 0):
                    print("<<Drone exists>>")
                    drone = Drone(droneIDList[i], droneList[i], droneState, 0.000000, 0.000000)
                    drone.update()
                else:
                    print("<<Drone does not exist>>")
                    drone = Drone(droneIDList[i], droneList[i], droneState, 0.000000, 0.000000)
                    drone.insert()
        
        if cmd == "UPDATE_DRONE":
            droneList = [drone for drone, droneID in data.items()]
            droneIDList = [droneID for drone, droneID in data.items()]
            droneState = data['STATE']
            droneList = droneList[2:]
            droneIDList = droneIDList[2:]
            for i in range (len(droneList)):
                drone = Drone(droneIDList[i], droneList[i], droneState, 0.000000, 0.000000)
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
                """
                if (self.forsøg == 0):
                    dest = '192.168.137.15' #'192.168.137.171'
                    data = ["takeoff;land;"]
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
                if packet.seq > self.seq_dic["state"]:
                    self.seq_dic["state"] = packet.seq
                    sameBat = 0
                    statePacket = packet.decode()
                    droneID = self.hotSpotIP+":"+statePacket.identifier
                    droneBat = self.data_parser_battery(statePacket)
                    droneTableList = fetchall('hive.drone')
                    for i in range (len(droneTableList)):
                        if (droneTableList[i]['droneID'] == droneID) and (droneTableList[i]['battery'] == droneBat):
                            sameBat +=1
                            
                    if (sameBat == 0):
                        print("<<Battery has changed>>")
                        drone = Drone(droneID, bat=self.data_parser_battery(statePacket))
                        drone.update()

                    packet.dump()
                    #pass

            elif packet.ptype == 2:
                # VIDEO
                if packet.seq < self.seq_dic["video"]:
                    self.seq_dic["video"] = packet.seq
                    #pass

            else:
                # Wrong packet type
                pass
            pass


if __name__ == "__main__":
    server = DmsServer()
    server.start()
