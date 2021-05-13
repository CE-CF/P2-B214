# Full imports
import re
import logging
import threading

# Partial imports
from abc import ABC, abstractmethod
from datetime import datetime
from socket import (
    AF_INET,
    SHUT_RDWR,
    SO_REUSEADDR,
    SOCK_DGRAM,
    SOCK_STREAM,
    SOL_SOCKET,
    socket,
)
from typing import List

# Hive imports
from hive.communication import BUFFER_SIZE, CONN_TYPE_TCP, CONN_TYPE_UDP
from hive.exceptions.packet_exceptions import DecodeErrorChecksum

# Communication imports
from .packet import HiveT, HiveU, Packet

# ====================
# LOGGING RELATED
# Change logging level when done
logging.basicConfig(filename="server.log", level=logging.DEBUG)

# ========================================================
# ========================================================
# ████████ ██   ██ ██████  ███████  █████  ██████  ███████
#    ██    ██   ██ ██   ██ ██      ██   ██ ██   ██ ██
#    ██    ███████ ██████  █████   ███████ ██   ██ ███████
#    ██    ██   ██ ██   ██ ██      ██   ██ ██   ██      ██
#    ██    ██   ██ ██   ██ ███████ ██   ██ ██████  ███████
# ========================================================
# ========================================================
class UDPPacketHandler(threading.Thread):
    def __init__(
        self,
        thread_id: int,
        target,
        conn_sock,
    ):
        super().__init__()
        self.thread_id = thread_id
        self.target = target
        self.conn_sock = conn_sock

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

    def _accept_udp(self):
        bytes_addr = self.conn_sock.recvfrom(BUFFER_SIZE)
        return bytes_addr[0], bytes_addr[1]

    def run(self):
        self.log_info("STARTED")
        # msg = self.recvall()
        while True:
            msg, addr = self._accept_udp()
            packet = HiveU.decode(msg)
            self.log_info(
                f"""Connection Information:
\t\t\t\t\t\t\t- Client Address: {addr}"""
            )
            p_dump = packet.dump(to_stdout=False)
            log_string = ""
            for k in p_dump:
                log_string += f"[{k.upper()}]: {p_dump[k]}"
                log_string += "\n\t\t\t\t\t\t\t"

            self.log_info(
                "Packet received content:" + "\n\t\t\t\t\t\t\t" + log_string
            )
            self.target(packet, CONN_TYPE_UDP)
        self.log_info("ENDED")


class TCPClientHandler(threading.Thread):
    """Class used to handle TCP packets on another thread"""

    def __init__(
        self,
        thread_id: int,
        client_conn: socket,
        client_addr: tuple,
        target,
        router: _Router,
    ):
        super().__init__()
        self.thread_id = thread_id
        self.client_conn = client_conn
        self.client_addr = client_addr
        self.target = target
        self.router = router

    def recvall(self, conn):
        """Receive all of incoming packet

        :returns: Message in bytes

        """
        msg = b""
        while True:
            data_part = conn.recv(BUFFER_SIZE)
            msg += data_part
            if len(data_part) < BUFFER_SIZE:
                break
        return bytes(msg)

    def reply_heart(self, conn):
        packet = HiveT(p_data="OK")
        msg_bytes = HiveT.encode_packet(packet)
        conn.send(msg_bytes)

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

    def create_thread_server(self):
        new_server = socket(AF_INET, SOCK_STREAM)
        new_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        new_server.bind(("", 0))
        return new_server

    def forward(self, packet: HiveT):
        self.conn.send(HiveT.encode_packet(packet))

    @property
    def client_name(self):
        return self._client_name

    @client_name.setter
    def client_name(self, name):
        self._client_name = name

    def run(self):
        # log thread start
        self.log_info("STARTED")

        # log connection details
        self.log_info(
            f"""Connection Information:
\t\t\t\t\t\t\t- Client Address: {self.client_addr[0]}:{self.client_addr[1]}"""
        )

        # Receive initial heartbeat
        message = self.recvall(self.client_conn)
        packet = HiveT.decode_packet(message)

        if packet.p_type == 3:
            self.log_info("Received initial heartbeat")
        else:
            self.log_warning(
                "Initial packet not heartbeat, proceding anyway since"
                + " connection is there!"
            )

        # Create new server
        thread_server = self.create_thread_server()
        new_port = thread_server.getsockname()[1]

        # Send thread server info for client migration
        mig_data_str = "CMD:MIGRATE;P:{port};".format(port=new_port)
        mig_packet = HiveT(p_dest=self.client_addr[0], p_data=mig_data_str)
        self.client_conn.send(HiveT.encode_packet(mig_packet))

        # Begin transfer
        self.client_conn.shutdown(SHUT_RDWR)
        self.client_conn.close()
        self.log_info(f"TRANSFER {self.client_addr} -> {new_port}")

        thread_server.listen(1)
        self.conn, self.addr = thread_server.accept()

        msg = self.recvall(self.conn)
        packet = HiveT.decode_packet(msg)
        if packet.p_data == "OK":
            self.log_info("TRANSFER done!")
            connected = True
        else:
            self.log_warning("TRANSFER failed")
            connected = False

        # Start new thread server loop
        while connected:
            # Packet handling
            try:
                msg = self.recvall(self.conn)
                recv_packet = HiveT.decode_packet(msg)
                if type(recv_packet) is HiveT:

                    recv_packet.src = self.addr
                    p_dump = recv_packet.dump(to_stdout=False)
                    log_string = ""
                    for k in p_dump:
                        log_string += f"[{k.upper()}]: {p_dump[k]}"
                        log_string += "\n\t\t\t\t\t\t\t"

                    self.log_info(
                        "Packet received content:"
                        + "\n\t\t\t\t\t\t\t"
                        + log_string
                    )
                    if recv_packet.p_type == 3:
                        self.reply_heart(self.conn)
                    else:
                        self.target(recv_packet, self.conn, mode=CONN_TYPE_TCP)
                else:
                    connected = False

            except ConnectionResetError:
                self.conn.shutdown(SHUT_RDWR)
                self.conn.close()
                connected = False

        # log thread end
        self.log_info("ENDED")


class _Router:
    def __init__(self):
        self.populate_dest_table()

    def is_destination(self):
        if type(self.packet) == HiveT:
            if self.packet.p_dest == self.srv_sock:
                return True
            else:
                return False
        else:
            return False

    def add_client(self, client: TCPlientHandler):
        
        
    def populate_dest_table(self):
        self.dest_table = {}
        for x in self.client_handlers:
            self.dest_table[x.client_name] = {
                "address": x.addr[0],
                "port": x.addr[1],
                "handler": x,
            }

    def find_dest(self):  # returns destination handler
        for x in self.dest_table:
            if self.dest_table[x]["address"] == self.packet.p_dest.exploded:
                print(f"Destination found in client: {x}")
                return x

    def route(self, packet):
        """Routes the supplied packet to its final destination,
        based on the destination table

        :param packet: 
        :type packet: HiveT
        :returns: bool

        """
        self.packet = packet

        if self.is_destination():
            return True
        else:
            dest_key = self.find_dest()
            c_handler = self.dest_table[dest_key]["handler"]
            c_handler.forward(self.packet)
            return False


# ================================
# ================================
#  ██████  ██████  ██████  ███████
# ██      ██    ██ ██   ██ ██
# ██      ██    ██ ██   ██ █████
# ██      ██    ██ ██   ██ ██
#  ██████  ██████  ██████  ███████
# ================================
# ================================
class Server(ABC):
    """Base class for hive servers

    Attributes:
     srv_port_tcp: Integer :: TCP socket port
     srv_port_udp: Integer :: UDP socket port
     srv_socket_tcp: socket object :: Socket object for the TCP connection
     srv_socket_udp: socket object :: Socket object for the UDP connection

    Methods:
     reply_heart(conn) :: Sends a heartbleead reply
     start() :: Starts the server and executes the run method
     run(packet: Packet) :: Abstract method used to handle the received packets
                            Override this in subclass

    """

    # Attributes
    # ===
    # UDP
    # ---
    _srv_port_udp = None
    _srv_socket_udp = None

    # TCP
    # ---
    _srv_port_tcp = None
    _srv_socket_tcp = None
    _max_clients_tcp = 2
    _conns_counter_tcp = 0

    # Constructor
    def __init__(self, tcp_port=1337, udp_port=6969):
        self.srv_port_tcp = tcp_port
        self.srv_socket_tcp = socket(AF_INET, SOCK_STREAM)
        self.srv_socket_tcp.bind(("", self.srv_port_tcp))

        self.srv_port_udp = udp_port
        self.srv_socket_udp = socket(AF_INET, SOCK_DGRAM)
        self.srv_socket_udp.bind(("", self.srv_port_udp))

    @abstractmethod
    def run(self, packet: Packet, conn, mode: bool):
        """The \"loop\" function for the Server class. All necessary packet
        handling should be done in here.
        *Note* A check should be implemented to differentiate between UDP based
        and TCP based protocol packet.

        :param packet:
        :type packet: Packet
        :returns:

        """
        pass

    def _accept_tcp(self):
        return self.srv_socket_tcp.accept()

    def start_tcp(self):
        log_string = f"TCP Listener on port: {self.srv_port_tcp}"
        print(log_string)
        logging.info(log_string)
        while True:
            self.srv_socket_tcp.listen(1)
            conn_tcp, addr_tcp = self._accept_tcp()
            # Begin multithreading TCP
            # ---
            self.conns_counter_tcp += 1
            tcpthread = TCPClientHandler(
                self.conns_counter_tcp,
                conn_tcp,
                addr_tcp,
                self.run,
                self.max_clients_tcp,
            )
            tcpthread.start()

    def start(self):
        """Starts the server and handles errors, executes the abstract run
        method.

        :returns:

        """

        try:
            # Boilerplate server code
            # ---
            print("Server started")
            # Start tcp main thread
            tcpmain = threading.Thread(target=self.start_tcp)
            tcpmain.daemon = True
            tcpmain.start()

            # Begin multithreading UDP
            # ---
            print(f"UDP Listener on port: {self.srv_port_udp}")
            udpthread = UDPPacketHandler(1, self.run, self.srv_socket_udp)
            udpthread.start()

            tcpmain.join()
            udpthread.join()
        # "Catch" exceptions
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
        except DecodeErrorChecksum:
            pass

    @property
    def max_clients_tcp(self):
        return self._max_clients_tcp

    @max_clients_tcp.setter
    def max_clients_tcp(self, cmax: int = 2):
        self._max_clients_tcp = cmax

    @property
    def conns_counter_tcp(self):
        return self._conns_counter_tcp

    @conns_counter_tcp.setter
    def conns_counter_tcp(self, i: int):
        self._conns_counter_tcp = i

    @property
    def srv_socket_tcp(self):
        return self._srv_socket_tcp

    @srv_socket_tcp.setter
    def srv_socket_tcp(self, sock: socket):
        self._srv_socket_tcp = sock

    @property
    def srv_socket_udp(self):
        return self._srv_socket_udp

    @srv_socket_udp.setter
    def srv_socket_udp(self, socket: socket):
        self._srv_socket_udp = socket

    @property
    def srv_port_tcp(self):
        return self._srv_port_tcp

    @srv_port_tcp.setter
    def srv_port_tcp(self, server_port):
        self._srv_port_tcp = server_port

    @property
    def srv_port_udp(self):
        return self._srv_port_udp

    @srv_port_udp.setter
    def srv_port_udp(self, server_port):
        self._srv_port_udp = server_port
