from hive.communication import CONN_TYPE_TCP, CONN_TYPE_UDP
from hive.communication.packet import HiveT, HiveU
from hive.communication.server import Server
from hive.dataBase.tableHandlers.route import Route
from hive.dataBase.tableHandlers.drone import Drone
from hive.dataBase.tableHandlers.getTable import fetchall, fetchallBat
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

    def eval_cmd(self, data, cmd_dict: dict, connection =None):
        cmd = cmd_dict["CMD"]
        args = {}
        self.conn = connection

        for key in cmd_dict.keys():
            if key != "CMD":
                args[key] = cmd_dict[key]

        if cmd == "ADD_DRONE":
            # pass
            droneList = [drone for drone, droneID in data.items()]
            droneIDList = [droneID for drone, droneID in data.items()]
<<<<<<< HEAD
            droneState = data["STATE"]
            droneList = droneList[2:]
            droneIDList = droneIDList[2:]
            droneTableList = fetchall("hive.drone")
=======
            droneState = data['STATE']
            droneLat = data['LAT']
            droneLong = data['LONG']
            droneList = droneList[4:]
            droneIDList = droneIDList[4:]
            droneTableList = fetchall('hive.drone')
>>>>>>> 670bbbbba33ebcdcb6819792b2fb1cfbdc86022d
            counter = 0

            for i in range(len(droneList)):
                for j in range(len(droneTableList)):

                    if droneTableList[j]["droneID"] == droneIDList[i]:
                        counter += 1

                if counter > 0:
                    print("<<Drone exists>>")
<<<<<<< HEAD
                    drone = Drone(
                        droneIDList[i],
                        droneList[i],
                        droneState,
                        0.000000,
                        0.000000,
                    )
                    drone.update()
                else:
                    print("<<Drone does not exist>>")
                    drone = Drone(
                        droneIDList[i],
                        droneList[i],
                        droneState,
                        0.000000,
                        0.000000,
                    )
=======
                    drone = Drone(droneIDList[i], droneList[i], droneState, droneLat, droneLong)
                    drone.update()
                else:
                    print("<<Drone does not exist>>")
                    drone = Drone(droneIDList[i], droneList[i], droneState, droneLat, droneLong)
>>>>>>> 670bbbbba33ebcdcb6819792b2fb1cfbdc86022d
                    drone.insert()

        if cmd == "UPDATE_DRONE":
            droneList = [drone for drone, droneID in data.items()]
            droneIDList = [droneID for drone, droneID in data.items()]
<<<<<<< HEAD
            droneState = data["STATE"]
            droneList = droneList[2:]
            droneIDList = droneIDList[2:]
            for i in range(len(droneList)):
                drone = Drone(
                    droneIDList[i],
                    droneList[i],
                    droneState,
                    0.000000,
                    0.000000,
                )
=======
            droneState = data['STATE']
            droneLat = data['LAT']
            droneLong = data['LONG']
            droneList = droneList[4:]
            droneIDList = droneIDList[4:]
            for i in range (len(droneList)):
                drone = Drone(droneIDList[i], droneList[i], droneState, droneLat, droneLong)
>>>>>>> 670bbbbba33ebcdcb6819792b2fb1cfbdc86022d
                drone.update()

        if cmd == "QOS":
            ltime = time()
            rtime = float(args["SENT"])
            delay = ltime - rtime
            print(delay)

        if cmd == "GET_DRONE":

            test1 = fetchall("hive.drone")

            OPCstring = "CMD:GET_DRONE;"
<<<<<<< HEAD
            for x in range(len(test1)):
                OPCstring += (
                    test1[x]["drone"] + ":" + test1[x]["droneID"] + ";"
                )
            dest = "192.168.137.36"  # OPC IP
=======
            for x in range (len(test1)):
                OPCstring += test1[x]['drone']+":"+test1[x]['droneID']+";"
            dest = '192.168.137.55' # OPC IP
>>>>>>> 670bbbbba33ebcdcb6819792b2fb1cfbdc86022d

            message = HiveT(3, dest, OPCstring)
            message = HiveT.encode_packet(message)
            print(message)
            self.conn.send(message)
<<<<<<< HEAD
            # pass
=======
            #pass
        
        if cmd == "GET_LOC":
            test1 = fetchall('hive.drone')

            OPCstring = "CMD:GET_LOC;"
            for x in range (len(test1)):
                OPCstring += "LAT"+":"+str(test1[x]['latitude'])+";""LONG"+":"+str(test1[x]['longitude'])+";"
            dest = '192.168.137.55' # OPC IP

            message = HiveT(3, dest, OPCstring)
            message = HiveT.encode_packet(message)
            print(message)
            self.conn.send(message)

>>>>>>> 670bbbbba33ebcdcb6819792b2fb1cfbdc86022d

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
                self.eval_cmd(data, cmd_dict, connection=conn)
                
                if (self.forsøg == 0):

                    dest1 = "192.168.137.1" #'192.168.137.171'
                    drone1 = "192.168.137.180"
                    drone2 = "192.168.137.193"
                    #cmd1 = "init;stop;wait:100;stop;land;"
                    cmd1 = "init;stop;wait:180;stop;land;"
                    cmd2 = "init;stop;wait:180;stop;land;"
                    data = drone1+";"+cmd1+"|"+drone2+";"+cmd2
                    message1 = HiveT("drone", dest1, data)
                    message1 = HiveT.encode_packet(message1)
                    
                    self.forsøg += 1
                    conn.send(message1)




                    

                
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
                    #packet.dump()
                    if packet.seq %100 == 0:
                        state = str(packet.data)
                        droneID = self.hotSpotIP+"."+str(packet.identifier)
                        droneBat = str(self.data_parser_battery(state))
                        sameBat = 0
                        droneTableList = fetchallBat('hive.drone')
                        if len(droneTableList) != 0:    
                            for i in range (len(droneTableList)):
                                if (droneTableList[i]['droneID'] == droneID) and (droneTableList[i]['battery'] == droneBat):
                                    sameBat +=1
                                    
                            if (sameBat == 0):
                                print("<<Battery has changed>>")
                                drone = Drone(droneID, bat=self.data_parser_battery(state))
                                drone.update()

                    #pass

            elif packet.ptype == 2:
                # VIDEO
                if packet.seq < self.seq_dic["video"]:
                    self.seq_dic["video"] = packet.seq
                    pass

            else:
                # Wrong packet type
                pass
            pass


if __name__ == "__main__":
    server = DmsServer()
    server.start()
