from hive.communication import CONN_TYPE_TCP, CONN_TYPE_UDP
from hive.communication.client import Client
from hive.communication.packet import HiveU, HiveT
from hive.relayBox.relayBoxUtilities.drone import Drone

class RbClient(Client):
    def __init__(self):
        super().__init__("Server IP", 9000, 9241)

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

    def run(self, packet, conn, mode):
        if mode is CONN_TYPE_TCP:
            print("MODE: TCP")
            # TCP CODE HERE
            packet.dump()

            if packet.p_type == 0 or packet.p_type == 1:
                # Enter route code here
                data = packet.data_parser()
                b_dest = packet.p_dest.packed
                
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
            else:
                # Wrong packet type
                pass
        elif mode is CONN_TYPE_UDP:
            print("MODE: UDP")
            # UDP CODE HERE
            pass


        # Husk at når der skal sendes data fra drone til dms, skal dataen wrappes
        # i en udp pakke, der skal være en sequence generator hver gang man modtager en pakke.
        