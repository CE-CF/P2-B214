from .packet import Packet
from ..exceptions.packet_exceptions import *
from ..utils.decorators import *
from socket import *
from abc import ABC, abstractmethod
import threading
from time import sleep

CON_TYPE_TCP = True


class Client(ABC):
    """Base class for hive clients

    Attributes:
     srv_port_tcp: Integer :: Server port for TCP connection
     srv_port_udp: Integer :: Server port for UDP connection
     srv_ip: String :: Server IP address ex: \"127.0.0.1\"
     client_sock: socket object :: Client socket object
     pulse: Boolean :: If there is a \"pulse\" 

    Methods:
     connect(mode=CON_TYPE_TCP) :: Connect to server
     send_message(mtype, mdest, mdata) :: Send packet with message to server
     send_heartbeat() :: Sends a heartbeat packet to server | deco: @setInterval
     start() :: Starts the client and executes the run method
     run(packet: Packet) :: Abstract method used to handle packets
                            Override this"""

    # Attributes
    _srv_port_tcp = None
    _srv_port_udp = None
    _srv_ip = None
    _client_sock = None
    _pulse = False

    # Constructor
    def __init__(self, srv_ip, tcp_port=None, udp_port=None):
        """Constructor for hive Client objects

        :param srv_ip: 
        :type srv_ip: String
        :param tcp_port: 
        :type tcp_port: Integer
        :param udp_port: 
        :type udp_port: Integer
        :returns: 

        """
        self.srv_ip = srv_ip
        if tcp_port is not None:
            self.srv_port_tcp = tcp_port
        if udp_port is not None:
            self.srv_port_udp = udp_port

    # NOT USED
    # @property
    # def heartbeat_int(self):
    #     return self._heartbeat_int

    # NOT USED
    # @heartbeat_int.setter
    # def heartbeat_int(self, interval: float):
    #     self._heartbeat_int = interval

    @property
    def srv_port_tcp(self):
        return self._srv_port_tcp

    @srv_port_tcp.setter
    def srv_port_tcp(self, port: int):
        self._srv_port_tcp = port

    @property
    def srv_port_udp(self):
        return self._srv_port_udp

    @srv_port_udp.setter
    def srv_port_udp(self, port: int):
        """Setter for the server udp port

        :param port: 
        :type port: int
        :returns: 

        """
        self._srv_port_udp = port

    @property
    def srv_ip(self):
        return self._srv_ip

    @srv_ip.setter
    def srv_ip(self, ip):
        self._srv_ip = ip

    @property
    def client_sock(self):
        return self._client_sock

    @client_sock.setter
    def client_sock(self, sock: socket):
        self._client_sock = sock

    @property
    def pulse(self):
        """Pulse getter

        :returns: bool

        """
        return self._pulse

    @pulse.setter
    def pulse(self, pulse: bool):
        """Pulse setter

        :param pulse:
        :type pulse: bool
        :returns:

        """
        self._pulse = pulse

    def connect(self, mode=CON_TYPE_TCP):
        """Connection wrapper function

        :param mode: 
        :type mode: bool
        :returns: 

        """
        if mode: # True == TCP | False == UDP
            self.client_sock.connect((self.srv_ip, self.srv_port_tcp))
        else:
            self.client_sock.connect((self.srv_ip, self.srv_port_udp))

    def send_message(self, mtype, mdest, mdata):
        """Create and send packet with data

        :param mtype: 
        :type mtype: 
        :param mdest: 
        :type mdest: 
        :param mdata: 
        :type mdata: 
        :returns: 

        """
        packet = Packet(mtype, mdest, mdata) 
        msg_bytes = Packet.encode_packet(packet)
        self.client_sock.send(msg_bytes)

    @setInterval(5)
    def send_heartbeat(self):
        """Send a heartbeat packet to server
        
        @setInterval(5) :: repeats in thread call once

        :returns: 

        """
        packet = Packet(p_data="Pulsecheck")
        msg_bytes = Packet.encode_packet(packet)
        self.client_sock.send(msg_bytes)
        print("==HEARTBEAT SENT==")

    @abstractmethod
    def run(self, packet: Packet):
        """The \"loop\" function of the Client class. All necessary packet handling should be done in here. The function is run as long as there is a pulse.

        :param packet:
        :type packet: Packet

        """
        pass

    def _set_pulse(self, packet: Packet):
        if packet.p_type == 3:
            self.pulse = True

    def start(self):
        """Start the client and execute the abstract run method

        :returns: 

        """
        try:
            self.pulse = False

            # Client boilerplate code
            self.client_sock = socket(AF_INET, SOCK_STREAM)
            self.connect()
            print("Client started")
            print(f"PULSE: {self.pulse}")

            # Start the heartbeat
            self.send_heartbeat()

            # Receive msg
            msg = self.client_sock.recv(4096)
            packet = Packet.decode_packet(msg)

            # Throw that packet into another thread and check pulse
            heartbeat_handler = threading.Thread(
                target=self._set_pulse, args=(packet,), daemon=True
            )
            if heartbeat_handler.is_alive() == False:
                heartbeat_handler.start()

            # If there is life (funny i know) execute run method
            while self.pulse:
                print(f"PULSE: {self.pulse}")
                self.run(packet)

            print("Stopping client")
            self.client_sock.close()

        # "Catch" some exceptions
        except DecodeErrorChecksum:
            pass
        except ConnectionRefusedError: # Server not available, try again in 5.. 4.. 3.. 2.. 1..
            retry_int = 5 
            print("Connection refused:")
            print(
                "Please make sure that the server is running, and that settings are correct"
            )
            print("[ CLIENT SETTINGS ]")
            print(f"SERVER IP: {self.srv_ip}")
            print(f"SERVER PORT(tcp): {self.srv_port_tcp}")
            print(f"SERVER PORT(udp): {self.srv_port_udp}")
            print()
            print(f"Trying again in {retry_int} seconds")
            sleep(retry_int)
            self.start()
