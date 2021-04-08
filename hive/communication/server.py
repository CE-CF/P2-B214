from socket import *
from ..communication.packet import Packet
from ..exceptions.packet_exceptions import *
from abc import ABC, abstractmethod
import hashlib
import datetime
import threading


class UDPHandler(threading.Thread):
    """Inner class used to handle UDP packets on another thread"""

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!██     ██    ██    ██████ !!!!!!!!!
    # !!!!!!!!!██     ██    ██    ██   ██!!!!!!!!!
    # !!!!!!!!!██  █  ██    ██    ██████ !!!!!!!!!
    # !!!!!!!!!██ ███ ██    ██    ██     !!!!!!!!!
    # !!!!!!!!! ███ ███  ██ ██ ██ ██ ██  !!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    def __init__(self, thread_id, func, client_msg, client_addr, args=()):
        super().__init__(self)
        self.msg = client_msg
        self.func = func
        self.addr = client_addr
        self.thread_id = thread_id
        self.args = args

    def run(self):
        print(
            "[STARTED] ID: {t_id} | TIME: {start_time}".format(
                t_id=self.thread_id, start_time=datetime.datetime.now()
            )
        )
        self.func(self.args)
        print(
            "[STOPPED] ID: {t_id} | TIME: {stop_time}".format(
                t_id=self.thread_id, stop_time=datetime.datetime.now()
            )
        )


class TCPHandler(threading.Thread):
    """Inner class used to handle TCP packets on another thread"""

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!██     ██    ██    ██████ !!!!!!!!!
    # !!!!!!!!!██     ██    ██    ██   ██!!!!!!!!!
    # !!!!!!!!!██  █  ██    ██    ██████ !!!!!!!!!
    # !!!!!!!!!██ ███ ██    ██    ██     !!!!!!!!!
    # !!!!!!!!! ███ ███  ██ ██ ██ ██ ██  !!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


    def __init__(self):
        pass


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
    _srv_port_tcp = None
    _srv_port_udp = None
    _srv_socket_tcp = None
    _srv_socket_udp = None

    # Constructor
    def __init__(self, tcp_port, udp_port=None):
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
        """Starts the server and handles errors, executes the abstract run method.

        :returns: 

        """

        try:
            # Boilerplate server code
            # ---
            print("Server started")
            self.srv_socket_tcp.listen(1)
            conn_tcp, addr_tcp = self._accept_tcp()
            print(f"Received connection by[TCP]: {addr_tcp[0]}:{addr_tcp[1]}")
            print(f"Received connection by[UDP]: {addr_udp[0]}:{addr_udp[1]}")
            # ---
            while True: # Server loop
                recv_data = conn.recv(4096) # receive data
                packet = Packet.decode_packet(recv_data) # decode into packet object
                if packet.p_type != 3: # check if heartbeat
                    self.run(packet)
                else:
                    print("HEART BEAT RECEIVED")
                    self.reply_heart(conn)

        # "Catch" exceptions
        except IndexError:
            print("Stopping server")
            self.srv_socket.close()
        except KeyboardInterrupt:
            print("Stopping server")
            self.srv_socket.close()
        except DecodeErrorChecksum:
            pass

    def reply_heart(self, conn):
        packet = Packet(p_data="OK")
        msg_bytes = Packet.encode_packet(packet)
        conn.send(msg_bytes)

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
