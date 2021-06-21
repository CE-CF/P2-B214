import socket
from threading import Lock, Thread
from time import sleep

from hive.communication import CONN_TYPE_TCP, CONN_TYPE_UDP
from hive.communication.client import Client
from hive.relayBox.relayBoxUtilities.drone import Drone
from hive.relayBox.relayBoxUtilities.droneChecker import DroneChecker
from hive.relayBox.relayBoxUtilities.relayBoxState import (
    Active,
    Airborne,
    Inactive,
    Off,
    On,
)


class RbClientUDP(Client):
    def __init__(self):
        self.srv_ip = "192.168.137.1"
        #self.srv_ip = "127.0.0.1"
        super().__init__(
            self.srv_ip, name="Relaybox", mode=CONN_TYPE_UDP, udp_port=9241
        )
        self.state = Off()
        self.lock = Lock()
        self.UDPdroneObjectList = []
        self.UDPdroneThreadList = []
        self.runCounter = 0
        self.seq_dic = {"cmd": 0, "state": 0, "video": 0}
        self.hotSpotIP = "192.168.137"
        self.threadRunning = True
        self.firstRun = True

    def droneObjectSetter(self, droneObjectList):
        self.UDPdroneObjectList = droneObjectList

    def droneThreadSetter(self, droneThreadList):
        self.UDPdroneThreadList = droneThreadList

    def change(self, state):  # Used to change the state of the relayBox
        """ Change state """
        self.state.switch(state)

    def data_parser(self, data):
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

        return d["yaw"]

    def listener_state(self):
        """Creates a thread that listens and forwards tello state"""
        state_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        state_host = ""
        state_port = 8890
        state_address = (state_host, state_port)
        state_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        state_sock.bind(state_address)
        stateSequenceNum = 1

        while True:
            data, drone = state_sock.recvfrom(2048)
            if data == b"ok":
                print("ok")
            elif data == b"error":
                print("error")
            else:
                SplitIP = str(drone[0]).split(".")
                LastIP = int(SplitIP[-1])
                self.lock.acquire()
                self.send_udp(LastIP, 1, stateSequenceNum, data)
                stateSequenceNum += 1
                if len(self.UDPdroneObjectList) != 0:
                    for i in range (len(self.UDPdroneObjectList)):
                        if self.UDPdroneObjectList[i].getID() == str(drone[0]):
                            self.UDPdroneObjectList[-1].setYaw(self.data_parser(data.decode(encoding="utf-8"))
                    )
                self.lock.release()
        state_sock.close()
        print("Stopped listening for state")

    def listener_stream(self):
        """" Creates a thread that listens for video stream and forward frames """
        video_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        video_host = ""
        video_port = 11111
        video_address = (video_host, video_port)
        video_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        video_sock.bind(video_address)
        videoSequenceNum = 1

        while True:
            data, drone = video_sock.recvfrom(2048)
            if data == b"ok":
                print("ok")
            elif data == b"error":
                print("error")
            else:
                SplitIP = str(drone[0]).split(".")
                LastIP = int(SplitIP[-1])
                self.send_udp(LastIP, 2, videoSequenceNum, data)
                videoSequenceNum += 1
        video_sock.close()
        print("Stopped listening for stream")

    def run(self, packet):
        if self.firstRun:
            state_thread = Thread(target=self.listener_state)
            stream_thread = Thread(target=self.listener_stream)

            state_thread.start()
            stream_thread.start()

            state_thread.join()
            stream_thread.join()
            self.firstRun = False 

        if packet.ptype == 0:
            packet.dump()
            droneIP = self.hotSpotIP+":"+str(packet.identifier)
            print('The packet data: {0} is sent to: {1}'.format(packet.data, droneIP))
            if self.threadRunning:
                for i in range (len(self.UDPdroneThreadList)):
                    if self.UDPdroneObjectList[i].getID() == droneIP:
                        self.UDPdroneObjectList[i].stop()
                self.threadRunning = False
            if packet.seq > self.seq_dic["state"]:
                self.seq_dic["state"] = packet.seq
            
                #for i in range (len(self.UDPdroneObjectList)):
                    
                for i in range (len(self.UDPdroneThreadList)):
                    if self.UDPdroneObjectList[i].getID() == droneIP:
                        self.UDPdroneObjectList[i].uplink(str(packet.data))
                


class RbClient(Client):
    def __init__(self, udp_client):
        self.srv_ip = "192.168.137.1"
        #self.srv_ip = "127.0.0.1"
        super().__init__(
            self.srv_ip,
            name="Relaybox",
            tcp_port=9000,
            other_client=udp_client,
        )
        self.state = Off()
        self.hotSpotIP = "192.168.137"  # First 3 octets of the hotspot IP
        self.connDrones = 2
        self.response_arr = []
        self.lock = Lock()
        self.activeDroneList = []
        self.drone_ip_range = [20, 25   ]
        self.DroneCheck = DroneChecker(self.hotSpotIP)
        self.TCPdroneObjectList = []
        self.threadCounter = 0
        self.airborneDroneThreads = []
        self.cmd_str = []
        self.droneIP = []
        self.rb_port = []
        self.rb_placement = [57.052711, 9.911936]

    # def threaded(fn):
    #     def wrapper(*args, **kwargs):
    #         threading.Thread(target=fn, args=args, kwargs=kwargs).start()

    #     return wrapper

    def eval_cmd(self, cmd_dict: dict):
        cmd = cmd_dict["CMD"]
        args = {}

        for key in cmd_dict.keys():
            if key != "CMD":
                args[key] = cmd_dict[key]

        if cmd == "ADD_DRONE":
            pass
        if cmd == "QOS":
            pass
    def splitDroneCMD(self, droneCMD):
        droneCMDlist = droneCMD.split("|")
        return droneCMDlist

    def data_parser_droneID(self, droneCMD):
        droneCMDlist = droneCMD.split(";")
        return droneCMDlist[0]

    def data_parser_droneCMD(self, droneCMD):
        """Parse incoming packet data for easier manipulation
        :param data:
        :type data: str
        :returns: Dictionary containing data
        """
        droneCMDlist = droneCMD.split(";")
        droneCMDlist.pop(0)
        cmd_str = ';'.join(['{}'.format(x) for x in droneCMDlist])
        cmd_str = cmd_str

        return cmd_str

    def change(self, state):  # Used to change the state of the relayBox
        """ Change state """
        self.state.switch(state)

    def run(self, packet):

        if type(self.state) is Active:
            packet.dump()

            if packet.p_type == 0 or packet.p_type == 1:
                # Enter route code here
                pass

            elif packet.p_type == 2:
                # Drone cmd code here
                droneData = self.DroneCheck.activeDronePacketUpdate(
                    self.activeDroneList, "airborne", self.rb_placement[0], self.rb_placement[1]
                )
                print("Ved skift fra active til airborne {}".format(droneData))
                self.send_message(
                    3, self.srv_ip, droneData
                )  # Send active drone data to the DMS
                self.change(Airborne)
            elif packet.p_type == 3:
                # Server/client cmd code here
                cmd_dict = packet.data_parser()
                self.run_cmd(cmd_dict)
                # pass
            else:
                # Wrong packet type
                pass

        # Husk at når der skal sendes data fra drone til dms, skal dataen wrappes
        # i en udp pakke, der skal være en sequence generator hver gang man modtager en pakke.
        if type(self.state) is Airborne:
             # Used to generate a port number for drone connection
            cmd_str_list = self.splitDroneCMD(packet.p_data)
            for i in range (len(cmd_str_list)):
                self.droneIP.append(self.data_parser_droneID(cmd_str_list[i]))
                self.cmd_str.append(self.data_parser_droneCMD(cmd_str_list[i]))
                SplitIP = str(self.droneIP[i]).split(".")
                LastIP = int(SplitIP[-1])
                self.rb_port.append(9000+LastIP)
                drone_port = 8889
                print(self.droneIP[i])
                print(self.rb_port[i])
                print(self.cmd_str[i])
                self.TCPdroneObjectList.append(Drone(str(self.droneIP[i]), drone_port, self.rb_port[i], self.cmd_str[i]))


            for i in range (len(self.TCPdroneObjectList)):
                self.TCPdroneObjectList[i].start()

            self.other_client.droneObjectSetter(self.TCPdroneObjectList)
            
            droneData = self.DroneCheck.activeDronePacketUpdate(
                self.activeDroneList, "active", self.rb_placement[0], self.rb_placement[1]
            )
            print("Ved skift fra airborne til active {}".format(droneData))
            """
            self.send_message(
                3, self.srv_ip, droneData
            )  # Send active drone data to the DMS
            """
            self.change(Active)

        if type(self.state) is Inactive:
            while True:
                self.activeDroneList = self.DroneCheck.ping(
                    self.drone_ip_range
                )

                if len(self.activeDroneList) == self.connDrones:
                    print(
                        "There are {} active drones".format(
                            len(self.activeDroneList)
                        )
                        + "\n"
                    )
                    droneData = self.DroneCheck.activeDronePacketAdd(
                        self.activeDroneList, "active", self.rb_placement[0], self.rb_placement[1]
                    )
                    print(
                        "Ved skift fra inactive til active {}".format(
                            droneData
                        )
                    )
                    self.send_message(
                        3, self.srv_ip, droneData
                    )  # Send active drone data to the DMS
                    self.change(Active)
                    break

                else:
                    print("There are no active drones")
                    sleep(2.5)


if __name__ == "__main__":
    client_udp = RbClientUDP()
    client_tcp = RbClient(client_udp)
    client_tcp.change(On)

    tcp_client_thread = Thread(target=client_tcp.start)
    udp_client_thread = Thread(target=client_udp.start)

    tcp_client_thread.daemon = True
    udp_client_thread.daemon = True

    udp_client_thread.start()
    tcp_client_thread.start()
    

    tcp_client_thread.join()
    udp_client_thread.join()
