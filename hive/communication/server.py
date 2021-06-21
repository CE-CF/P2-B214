import logging
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from socket import (
    AF_INET,
    SHUT_RDWR,
    SO_REUSEADDR,
    SOCK_DGRAM,
    SOCK_STREAM,
    SOL_SOCKET,
    socket,
)
from threading import Lock, Thread
from typing import List

from hive.communication import BUFFER_SIZE, CONN_TYPE_TCP, CONN_TYPE_UDP
from hive.exceptions.packet_exceptions import DecodeErrorChecksum

from .packet import HiveT, HiveU, Packet

logging.basicConfig(filename="server.log", level=logging.DEBUG)


class UDPPacketHandler(Thread):
    def __init__(self, thread_id: int, target, conn_sock, router):
        super().__init__()
        self.thread_id = thread_id
        self.target = target
        self.conn_sock = conn_sock
        self.router = router

    def log_info(self, msg: str):
        """Logging helper

        :param msg:
        :type msg: str

        """
        log_format = (
            f"[ THREAD-UDP {self.thread_id} | TIME {datetime.now()} ]: {msg}"
        )
        logging.info(log_format)

    def log_warning(self, msg: str):
        """Logging helper

        :param msg:
        :type msg: str

        """
        log_format = (
            f"[ THREAD-UDP {self.thread_id} | TIME {datetime.now()} ]: {msg}"
        )
        logging.warning(log_format)

    def recvall(self):
        """Receive all of incoming packet

        :returns: Message in bytes

        """
        msg = b""
        while True:
            data_part = self.conn_sock.recv(BUFFER_SIZE)
            msg += data_part
            if len(data_part) < BUFFER_SIZE:
                break
        return bytes(msg)

    def send(self, packet: HiveU, client_addr):
        self.conn_sock.sendto(packet.encode(), client_addr)

    def _accept_udp(self):
        bytes_addr = self.conn_sock.recvfrom(BUFFER_SIZE)
        return bytes_addr[0], bytes_addr[1]

    def run(self):
        self.log_info("STARTED")
        while True:
            msg, addr = self._accept_udp()
            packet = HiveU.decode(msg)
            self.router.broadcast_hiveu(packet)
            self.log_info(
                f"""Connection Information:
\t\t\t\t\t\t\t- Client Address: {addr}"""
            )
            """
            p_dump = packet.dump(to_stdout=False)
            log_string = ""
            for k in p_dump:
                log_string += f"[{k.upper()}]: {p_dump[k]}"
                log_string += "\n\t\t\t\t\t\t\t"

            self.log_info(
                "Packet received content:" + "\n\t\t\t\t\t\t\t" + log_string
            )
            """
            self.target(packet, self.conn_sock, CONN_TYPE_UDP)
        self.log_info("ENDED")


class TCPClientHandler(Thread):
    """The thread designed to handle TCP Clients"""

    _client_name = "test"

    @property
    def client_name(self):
        return self._client_name

    def __init__(
        self,
        thread_id: int,
        client_conn: socket,
        client_addr: tuple,
        target,
        router,
    ):
        super().__init__()
        self.thread_id = thread_id
        self.client_conn = client_conn
        self.client_addr = client_addr
        self.target = target
        self.router = router

        # Setup thread server
        self._thread_server = socket(AF_INET, SOCK_STREAM)
        self._thread_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._thread_server.bind(("", 0))

    def log_info(self, msg: str):
        """Logging helper

        :param msg:
        :type msg: str

        """
        log_format = (
            f"[ THREAD-TCP {self.thread_id} | TIME {datetime.now()} ]: {msg}"
        )
        logging.info(log_format)

    def log_warning(self, msg: str):
        """Logging helper

        :param msg:
        :type msg: str

        """
        log_format = (
            f"[ THREAD-TCP {self.thread_id} | TIME {datetime.now()} ]: {msg}"
        )
        logging.warning(log_format)

    def recvall(self):
        """Receive all of incoming packet

        :returns: Message in bytes

        """
        msg = b""
        while True:
            data_part = self.client_conn.recv(BUFFER_SIZE)
            msg += data_part
            if len(data_part) < BUFFER_SIZE:
                break
        return bytes(msg)

    def recvpacket(self):
        msg = self.recvall()
        return HiveT.decode_packet(msg)

    def forward(self, packet: HiveT):
        self.client_conn.send(HiveT.encode_packet(packet))

    def migrate(self):
        # Send migration information
        self.log_info("Starting migration")
        new_port = self._thread_server.getsockname()[1]
        mig_data_str = "CMD:MIGRATE;P:{port};".format(port=new_port)
        mig_packet = HiveT(p_dest=self.client_addr[0], p_data=mig_data_str)
        mig_packet.dump(log=False)
        self.client_conn.send(HiveT.encode_packet(mig_packet))

        # Close connection for original connection
        self.log_info("Shutting down original connection")
        self.client_conn.shutdown(SHUT_RDWR)
        self.client_conn.close()

        self.log_info("Listening for migrated connection")
        self._thread_server.listen(1)
        self.client_conn, self.client_addr = self._thread_server.accept()
        self.log_info("Migration accepted")
        self.log_info(f"New client information: {self.client_addr}")

    def run(self):
        self.log_info("STARTED")
        self.log_info(
            f"Client info: {self.client_addr[0]}:{self.client_addr[1]}"
        )

        packet = self.recvpacket()
        packet.dump()

        data = packet.data_parser()

        self._client_name = data["NAME"]
        self.log_info(f"Client name: {self.client_name}")

        self.migrate()
        self.log_info("Updating routers lookup table")
        self.router.update_table()
        if "UDP" in data:
            print("Adding udp info")
            self.router.add_udp_info(self.client_name, int(data["UDP"]))

        packet = self.recvpacket()
        p_dump = packet.dump(to_stdout=False)
        log_string = ""
        for k in p_dump:
            log_string += f"[{k.upper()}]: {p_dump[k]}"
            log_string += "\n\t\t\t\t\t\t\t"

        self.log_info(
            "Packet received content:" + "\n\t\t\t\t\t\t\t" + log_string
        )
        connected = False
        if packet.p_data == "OK":
            print("TRANSFER DONE!")
            packet = HiveT(3, self.client_addr[0], "DONE")
            self.client_conn.send(HiveT.encode_packet(packet))
            connected = True
        else:
            print("TRANSFER FAILED!")
            connected = False

        while connected:
            try:
                packet = self.recvpacket()
                if type(packet) is HiveT:
                    p_dump = packet.dump(to_stdout=False)
                    log_string = ""
                    for k in p_dump:
                        log_string += f"[{k.upper()}]: {p_dump[k]}"
                        log_string += "\n\t\t\t\t\t\t\t"

                    self.log_info(
                        "Packet received content:"
                        + "\n\t\t\t\t\t\t\t"
                        + log_string
                    )
                    # Catch packet by router here
                    routemsg = self.router.route(packet)
                    if routemsg is RoutingMSG.SELF_IS_DEST:
                        packet.src = self.client_addr
                        self.target(
                            packet, self.client_conn, mode=CONN_TYPE_TCP
                        )
                    elif routemsg is (
                        RoutingMSG.FORWARDED or RoutingMSG.DRONE_IS_DEST
                    ):
                        self.client_conn.send(
                            HiveT.encode_packet(
                                HiveT(3, self.client_addr[0], "MSG:FORWARDED;")
                            )
                        )
                    elif routemsg is RoutingMSG.DEST_NOT_FOUND:
                        self.client_conn.send(
                            HiveT.encode_packet(
                                HiveT(
                                    3,
                                    self.client_addr[0],
                                    "ERROR:404;",
                                )
                            )
                        )

                else:
                    connected = False
            except ConnectionRefusedError:
                self.client_conn.shutdown(SHUT_RDWR)
                self.client_conn.close()
                connected = False

        self.log_info("ENDED")


class RoutingMSG(Enum):
    FORWARDED = 1
    DEST_NOT_FOUND = 2
    SELF_IS_DEST = 3
    DRONE_IS_DEST = 4


class Router:
    @property
    def clientlist(self):
        return self._clientlist

    def __init__(self, srv_ip):
        self._clientlist: List[TCPClientHandler] = []
        self.udp_handler: UDPPacketHandler = None
        self.lock = Lock()
        self.srv_ip = srv_ip
        self.dest_table = {}

    def is_destination(self):
        if type(self.packet) == HiveT:
            if self.packet.p_dest.exploded == self.srv_ip:
                return True
            else:
                return False
        else:
            return False

    def update_table(self):
        self.log_info("Updating lookup table")
        self.lock.acquire()
        for x in self.clientlist:
            if x.client_name not in self.dest_table:
                self.dest_table[x.client_name] = {
                    "address": x.client_addr[0],
                    "handler": x,
                }
        log_string = ""
        for x in self.dest_table:
            log_string += "\n=============================================\n"
            log_string += f"\t\t\tClient: {x}\n"
            log_string += f"\t\t\tAddress: {self.dest_table[x]['address']}\n"
            log_string += (
                "\t\t\tThread-ID:"
                + f"{self.dest_table[x]['handler'].thread_id}\n"
            )
            if "udp_port" in self.dest_table[x]:
                log_string += (
                    f"\t\t\tudp_port: {self.dest_table[x]['udp_port']}"
                )

            log_string += "\n=============================================\n"
        self.log_info(log_string)
        print(log_string)
        self.lock.release()

    def log_info(self, msg: str):
        """Logging helper

        :param msg:
        :type msg: str

        """
        log_format = f"[ ROUTER | TIME {datetime.now()} ]: {msg}"
        logging.info(log_format)

    def log_warning(self, msg: str):
        """Logging helper

        :param msg:
        :type msg: str

        """
        log_format = f"[ ROUTER | TIME {datetime.now()} ]: {msg}"
        logging.warning(log_format)

    def add_client(self, client: TCPClientHandler):
        self._clientlist.append(client)

    def add_handler(self, handler: UDPPacketHandler):
        self.udp_handler = handler

    def add_udp_info(self, name, udp_port: int):
        self.lock.acquire()
        self.dest_table[name]["udp_port"] = udp_port
        log_string = ""
        for x in self.dest_table:
            log_string += "\n=============================================\n"
            log_string += f"\t\t\tClient: {x}\n"
            log_string += f"\t\t\tAddress: {self.dest_table[x]['address']}\n"
            log_string += (
                "\t\t\tThread-ID:"
                + f"{self.dest_table[x]['handler'].thread_id}\n"
            )
            if "udp_port" in self.dest_table[x]:
                log_string += (
                    f"\t\t\tudp_port: {self.dest_table[x]['udp_port']}"
                )

            log_string += "\n=============================================\n"

        print(log_string)
        self.lock.release()

    def find_dest(self):
        """Finds the destination for packet in destination table

        :returns: client key in destination table

        """
        for x in self.dest_table:
            if self.dest_table[x]["address"] == self.packet.p_dest.exploded:
                self.log_info(f"Destination found in client: {x}")
                return x

    def broadcast_hiveu(self, packet: HiveU):
        if packet.ptype == 2:
            self.lock.acquire()
            for x in self.dest_table:
                if "OPC" in x and "udp_port" in self.dest_table[x]:
                    self.log_info(
                        f"Found {x} with port {self.dest_table[x]['udp_port']}"
                    )
                    packet.dump(to_stdout=False)
                    self.udp_handler.send(
                        packet,
                        (
                            self.dest_table[x]["address"],
                            self.dest_table[x]["udp_port"],
                        ),
                    )
            self.lock.release()

        if packet.ptype == 0:
            self.lock.acquire()
            for x in self.dest_table:
                if "Relaybox" in x and "udp_port" in self.dest_table[x]:
                    self.log_info(
                        f"Found {x} with port {self.dest_table[x]['udp_port']}"
                    )
                    print(
                        f"Found {x} with port {self.dest_table[x]['udp_port']}"
                    )
                    packet.dump(to_stdout=False)
                    self.udp_handler.send(
                        packet,
                        (
                            self.dest_table[x]["address"],
                            self.dest_table[x]["udp_port"],
                        ),
                    )
            self.lock.release()

    def route(self, packet):
        """Routes the supplied packet to its final destination,
        based on the destination table

        :param packet:
        :type packet: HiveT
        :returns: bool

        """
        self.packet = packet
        self.log_info(
            f"Received packet with destination: {self.packet.p_dest.exploded}"
        )
        self.lock.acquire()
        dest_key = self.find_dest()
        if self.is_destination():
            self.log_info("Server is destination of packet")
            self.lock.release()
            return RoutingMSG.SELF_IS_DEST
        elif dest_key is None:
            self.log_info("Destination not found")
            self.lock.release
            return RoutingMSG.DEST_NOT_FOUND
        else:
            self.log_info(f"Forwarding packet to destination: {dest_key} ")
            c_handler = self.dest_table[dest_key]["handler"]
            c_handler.forward(self.packet)
            self.lock.release()
            return RoutingMSG.FORWARDED


class Server(ABC):
    def __init__(self, tcp_port=1337, udp_port=6969, srv_ip="127.0.0.1"):
        self.srv_port_tcp = tcp_port
        self.srv_socket_tcp = socket(AF_INET, SOCK_STREAM)
        self.srv_socket_tcp.bind(("", self.srv_port_tcp))

        self.srv_port_udp = udp_port
        self.srv_socket_udp = socket(AF_INET, SOCK_DGRAM)
        self.srv_socket_udp.bind(("", self.srv_port_udp))
        self.conn_counter_tcp = 0

        self.router = Router(srv_ip)

    @abstractmethod
    def run(self, packet: Packet, conn: socket, mode: bool):
        """The \"loop\" function for the Server class. All necessary packet
        handling should be done in here.
        *Note* A check should be implemented to differentiate between UDP based
        and TCP based protocol packet.

        :param packet:
        :type packet: Packet
        :returns:

        """
        pass

    def start_tcp(self):
        while True:
            self.srv_socket_tcp.listen(1)
            conn, addr = self.srv_socket_tcp.accept()
            self.conn_counter_tcp += 1
            tcpthread = TCPClientHandler(
                self.conn_counter_tcp, conn, addr, self.run, self.router
            )
            self.router.add_client(tcpthread)
            self.router.update_table()
            tcpthread.start()

    def start(self):
        try:
            print("Starting server")
            # Start main tcp thread here
            print(f"TCP Listener on port: {self.srv_port_tcp}")
            tcpmain = Thread(target=self.start_tcp)
            tcpmain.daemon = True
            tcpmain.start()

            # Start UDP thread
            print(f"UDP Listener on port: {self.srv_port_udp}")
            udpthread = UDPPacketHandler(
                1, self.run, self.srv_socket_udp, self.router
            )
            self.router.add_handler(udpthread)
            udpthread.start()

            tcpmain.join()
            udpthread.join()
        except IndexError:
            print("Stopping server")
            self.srv_socket_tcp.shutdown(SHUT_RDWR)
            self.srv_socket_tcp.close()
            self.srv_socket_udp.shutdown(SHUT_RDWR)
            self.srv_socket_udp.close()
        except KeyboardInterrupt:
            print("Stopping server")
            self.srv_socket_tcp.shutdown(SHUT_RDWR)
            self.srv_socket_tcp.close()
            self.srv_socket_udp.shutdown(SHUT_RDWR)
            self.srv_socket_udp.close()
