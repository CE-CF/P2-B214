from hive.communication import CONN_TYPE_TCP, CONN_TYPE_UDP
from hive.communication.packet import HiveT, HiveU
from hive.communication.server import Server
from hive.dataBase.tableHandlers.route import Route


class DmsServer(Server):
    def __init__(self):
        super().__init__(9000, 9241)
        self.seq_dic = {"cmd": 0, "state": 0, "video": 0}

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
            if packet.p_type == 0 or packet.p_type == 1:
                print("før insert")
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
                self.eval_cmd(cmd_dict)
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
