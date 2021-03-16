from .packet import Packet, encode_packet, decode_packet
from ..exceptions.packet_exceptions import *
from ..utils.decorators import *
from socket import *
from abc import ABC, abstractmethod
import threading
from time import sleep

CON_TYPE_TCP = True


class Client(ABC):

    # Attributes
    _srv_port_tcp = None
    _srv_port_udp = None
    _srv_ip = None
    _client_sock = None

    # Constructor
    def __init__(self, srv_ip, tcp_port=None, udp_port=None):
        self.srv_ip = srv_ip
        if tcp_port is not None:
            self.srv_port_tcp = tcp_port
        if udp_port is not None:
            self.srv_port_udp = udp_port

    @property
    def heartbeat_int(self):
        return self._heartbeat_int

    @heartbeat_int.setter
    def heartbeat_int(self, interval: float):
        self._heartbeat_int = interval

    @property
    def srv_port_tcp(self):
        return self._srv_port_tcp

    @srv_port_tcp.setter
    def srv_port_tcp(self, port):
        self._srv_port_tcp = port

    @property
    def srv_port_udp(self):
        return self._srv_port_udp

    @srv_port_udp.setter
    def srv_port_udp(self, port):
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

    def connect(self, mode=CON_TYPE_TCP):
        if mode:
            self.client_sock.connect((self.srv_ip, self.srv_port_tcp))
        else:
            self.client_sock.connect((self.srv_ip, self.srv_port_udp))

    def send_message(self, mtype, mdest, mdata):
        packet = Packet(mtype, mdest, mdata)
        msg_bytes = encode_packet(packet)
        self.client_sock.send(msg_bytes)

    @setInterval(5)
    def send_heartbeat(self):
        packet = Packet(p_data="HEARTBEAT")
        msg_bytes = encode_packet(packet)
        self.client_sock.send(msg_bytes)
        print("==HEARTBEAT SENT==")

    @abstractmethod
    def run(self):
        pass

    def _start(self):
        try:
            self.client_sock = socket(AF_INET, SOCK_STREAM)
            self.connect()
            print("Client started")
            self.send_heartbeat()
            while True:
                self.run()
        except KeyboardInterrupt:
            print("Stopping client")
            self.client_sock.close()
        except DecodeErrorChecksum:
            pass
        except ConnectionRefusedError:
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
            self._start()
