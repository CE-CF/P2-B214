from socket import *
from ..communication.packet import Packet, decode_packet, encode_packet
from ..exceptions.packet_exceptions import *
from abc import ABC, abstractmethod

import hashlib


class Server(ABC):
    # Attributes
    _srv_port_tcp = None
    _srv_port_udp = None
    _packet = None

    # Constructor
    def __init__(self, port):
        self.srv_port_tcp = port
        self.srv_socket = socket(AF_INET, SOCK_STREAM)
        self.srv_socket.bind(("", self.srv_port_tcp))

    # SERVER LOOP
    @abstractmethod
    def run(self, conn, addr):
        pass

    def _accept(self):
        return self.srv_socket.accept()

    def _start(self):
        print("Server started")
        self.srv_socket.listen(1)
        con, addr = self._accept()
        print(f"Received connection by: {addr}")
        while True:
            try:
                self.run(con, addr)
            except KeyboardInterrupt:
                print("Stopping server")
                self.srv_socket.close()
                break
            except DecodeErrorChecksum:
                pass

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
