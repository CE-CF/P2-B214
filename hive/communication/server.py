# Full imports
import logging
import threading

# Partial imports
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List
from socket import (
    AF_INET,
    SHUT_RDWR,
    SO_REUSEADDR,
    SOCK_DGRAM,
    SOCK_STREAM,
    SOL_SOCKET,
    socket,
)


# Hive imports
from hive.communication import BUFFER_SIZE
from hive.exceptions.packet_exceptions import DecodeErrorChecksum

# Communication imports
from .packet import Packet

# ====================
# LOGGING RELATED
# Change logging level when done
logging.basicConfig(filename="server.log", level=logging.DEBUG)

# ====================
# Global variabels


# ========================================================
# ========================================================
# ████████ ██   ██ ██████  ███████  █████  ██████  ███████
#    ██    ██   ██ ██   ██ ██      ██   ██ ██   ██ ██
#    ██    ███████ ██████  █████   ███████ ██   ██ ███████
#    ██    ██   ██ ██   ██ ██      ██   ██ ██   ██      ██
#    ██    ██   ██ ██   ██ ███████ ██   ██ ██████  ███████
# ========================================================
# ========================================================
class TCPClientHandler(threading.Thread):
    """Class used to handle TCP packets on another thread"""

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!██     ██    ██    ██████ !!!!!!!!!
    # !!!!!!!!!██     ██    ██    ██   ██!!!!!!!!!
    # !!!!!!!!!██  █  ██    ██    ██████ !!!!!!!!!
    # !!!!!!!!!██ ███ ██    ██    ██     !!!!!!!!!
    # !!!!!!!!! ███ ███  ██ ██ ██ ██ ██  !!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def __init__(
        self,
        thread_id: int,
        client_conn: socket,
        client_addr,
        target,
        max_conns,
    ):
        super().__init__()
        self.thread_id = thread_id
        self.client_conn = client_conn
        self.client_addr = client_addr
        self.target = target

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
        packet = Packet(p_data="OK")
        msg_bytes = Packet.encode_packet(packet)
        conn.send(msg_bytes)

    def log_info(self, msg: str):
        """Logging helper

        :param msg:
        :type msg: str

        """
        log_format = (
            f"[ THREAD {self.thread_id} | TIME {datetime.now()} ]: {msg}"
        )
        logging.info(log_format)

    def log_warning(self, msg: str):
        """Logging helper

        :param msg:
        :type msg: str

        """
        log_format = (
            f"[ THREAD {self.thread_id} | TIME {datetime.now()} ]: {msg}"
        )
        logging.warning(log_format)

    def create_thread_server(self):
        new_server = socket(AF_INET, SOCK_STREAM)
        new_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        new_server.bind(("", 0))
        return new_server

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
        packet = Packet.decode_packet(message)

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
        mig_packet = Packet(p_dest=self.client_addr[0], p_data=mig_data_str)
        self.client_conn.send(Packet.encode_packet(mig_packet))

        # Begin transfer
        self.client_conn.shutdown(SHUT_RDWR)
        self.client_conn.close()
        self.log_info(f"TRANSFER {self.client_addr} -> {new_port}")

        thread_server.listen(1)
        conn, addr = thread_server.accept()

        msg = self.recvall(conn)
        packet = Packet.decode_packet(msg)
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
                msg = self.recvall(conn)
                recv_packet = Packet.decode_packet(msg)
                if type(recv_packet) is Packet:
                    recv_packet.src = addr
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
                        self.reply_heart(conn)
                    else:
                        self.target(recv_packet)
                else:
                    connected = False

            except ConnectionResetError:
                conn.shutdown(SHUT_RDWR)
                conn.close()
                connected = False

        # log thread end
        self.log_info("ENDED")


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
    def __init__(self, tcp_port=1337, udp_port=None):
        self.srv_port_tcp = tcp_port
        self.srv_socket_tcp = socket(AF_INET, SOCK_STREAM)
        self.srv_socket_tcp.bind(("", self.srv_port_tcp))

        # UDP under construcion
        # !!!!!!!!!!!!!!!!!!!!!!
        # self.srv_port_udp = udp_port
        # self.srv_socket_udp = socket(AF_INET, SOCK_DGRAM)
        # self.srv_socket_udp.bind(("", self.srv_port_udp))
        # !!!!!!!!!!!!!!!!!!!!!!

    @abstractmethod
    def run(self, packet: Packet):
        """The \"loop\" function for the Server class. All necessary packet handling should be done in here.

        :param packet:
        :type packet: Packet
        :returns:

        """
        pass

    def _accept_tcp(self):
        return self.srv_socket_tcp.accept()

    def _accept_udp(self):
        return self.srv_socket_udp.accept()

    def start(self):
        """Starts the server and handles errors, executes the abstract run
        method.

        :returns:

        """

        try:
            while True:  # Server loop
                # Boilerplate server code
                # ---
                print("Server started")
                self.srv_socket_tcp.listen(1)
                conn_tcp, addr_tcp = self._accept_tcp()
                # ---

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

                # ---
                # recv_data = conn.recv(4096)  # receive data
                # packet = Packet.decode_packet(recv_data)  # decode into packet object
                # if packet.p_type != 3:  # check if heartbeat
                #     self.run(packet)
                # else:
                #     print("HEART BEAT RECEIVED")
                #     self.reply_heart(conn)

        # "Catch" exceptions
        except IndexError:
            print("Stopping server")
            self.srv_socket_tcp.shutdown(SHUT_RDWR)
            self.srv_socket_tcp.close()
        except KeyboardInterrupt:
            print("Stopping server")
            self.srv_socket_tcp.shutdown(SHUT_RDWR)
            self.srv_socket_tcp.close()
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
        self._srv_port_udp = socket

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
