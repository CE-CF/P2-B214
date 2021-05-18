import threading
import socket
import ipaddress
from time import sleep
from hive.communication import CONN_TYPE_TCP, CONN_TYPE_UDP
from hive.communication.client import Client
from hive.relayBox.relayBoxUtilities.drone import Drone
from hive.relayBox.relayBoxUtilities.droneChecker import DroneChecker
from hive.relayBox.relayBoxUtilities.relayBoxState import Off, On, Inactive, Active

class RbClient(Client):
    def __init__(self):
        self.srv_ip = "127.0.0.1"
        super().__init__(self.srv_ip, tcp_port=9000, udp_port=9241)
        self.state = Off()
        self.hotSpotIP = "192.168.137" # First 3 octets of the hotspot IP
        self.connDrones = 1
        self.response_arr = []
    
    def threaded(fn):
        def wrapper(*args, **kwargs):
            threading.Thread(target=fn, args=args, kwargs=kwargs).start()
        return wrapper
    
    def data_parser(data):
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

        return d['yaw']

    @threaded
    def listener_state(self):
        state_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        state_host = ''
        state_port = 8890
        state_address = (state_host, state_port)
        state_sock.bind(state_address)
        sequenceNum = 0

        while True:
            data, server = state_sock.recvfrom(2046)
            if data == b'ok':
                print("ok")
            elif data == b'error':
                print("error")
            else:
                b_sender = ipaddress.IPv4Address(server[0]).packed
                self.send(b_sender[3], 1, sequenceNum, data)
                sequenceNum += 1
                self.response_arr.append(self.data_parser(data.decode(encoding="utf-8")))
    
    def lisetener_stream(self):

    def eval_cmd(self, cmd_dict: dict):
        cmd = cmd_dict["CMD"]
        args = {}

        for key in cmd_dict.keys():
            if key!= "CMD":
                args[key] = cmd_dict[key]
        
        if cmd == "ADD_DRONE":
            pass
        if cmd == "QOS":
            pass
    
    def change(self, state): # Used to change the state of the relayBox
        """ Change state """
        self.state.switch(state)

    def run(self, packet):

        if (type(self.state) is Active):
                     
            print("MODE: TCP")
            # TCP CODE HERE
            packet.dump()

            if packet.p_type == 0 or packet.p_type == 1:
                # Enter route code here
                data = packet.data_parser()
                b_dest = packet.p_dest.packed # Used to generate a port number for drone connection
                    
                drone_port = 8889
                rb_port = 9000+b_dest[3]
                
                drone = Drone(str(packet.p_dest), drone_port, rb_port)
                drone.send(data)
                drone.closeConnection()

            elif packet.p_type == 2:
                # Drone cmd code here
                pass
            elif packet.p_type == 3:
                # Server/client cmd code here
                cmd_dict = packet.data_parser()
                self.eval_cmd(cmd_dict)
                #pass
            else:
                # Wrong packet type
                pass


        # Husk at når der skal sendes data fra drone til dms, skal dataen wrappes
        # i en udp pakke, der skal være en sequence generator hver gang man modtager en pakke.
                
        if (type(self.state) is Inactive):
            print("State inactive if statement")
            DroneCheck = DroneChecker(self.hotSpotIP)
            
            while True:   
                activeDroneList = DroneCheck.ping()
                
                if (len(activeDroneList) == self.connDrones):
                    print('There are {} active drones'.format(len(activeDroneList))+"\n")
                    droneData = DroneCheck.activeDronePacket(activeDroneList)
                    print(droneData)
                    self.send_message(3, self.srv_ip, droneData) # Send active drone data to the DMS
                    self.change(Active)
                    break
                
                else:
                    print("There are no active drones")
                    sleep(2.5)

        

if __name__ == "__main__":
    client = RbClient()
    client.change(On)
    client.start()