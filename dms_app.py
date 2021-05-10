from hive.communication import CONN_TYPE_TCP, CONN_TYPE_UDP
from hive.communication.server import Server
from hive.communication.packet import HiveU, HiveT
from hive.dataBase.tableHandlers.route import Route


class DmsServer(Server):
    def __init__(self):
        super().__init__(9000, 9241)

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

    def run(self, packet, conn, mode):
        if mode is CONN_TYPE_TCP:
            # TCP CODE HERE
            packet.dump()
            print("ved dump")
            if packet.p_type == 0 or packet.p_type == 1:
                print("før insert")
                # Waypoint code here
                data = packet.data_parser()
                route = Route(packet.p_dest, packet.p_type, data)
                route.insert()
<<<<<<< Updated upstream
                conn.send(b"Succes")
=======
                print("efter insert")
>>>>>>> Stashed changes
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
            print("udp")
            # UDP CODE HERE
            pass


if __name__ == "__main__":
    server = DmsServer()
    server.start()
