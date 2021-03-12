from socket import *
from ..communication.packet import Packet
from ..exceptions.server_exceptions import *

import hashlib


class Server:
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
    def run(self):
        print("Server started")
        self.srv_socket.listen(1)
        while True:
            client_con, client_addr = self.srv_socket.accept()
            print(f"Accepted client: {client_addr}")

            recv_bytes = client_con.recv(4096)
            recv_packet = self.decode_packet(recv_bytes)

            recv_packet.dump()

            del recv_packet
            del recv_bytes

    def encode_packet(self, packet):
        """Encodes the supplied packet into a bytes object

        Arguments:
          - packet (Packet):
                  The packet to be encoded

        Returns:
          - packet_bytes (bytes)"""
        if type(packet) is not Packet:
            raise EncodeErrorPacket(
                packet, f"Argument is not of type: {type(Packet())} "
            )
        packet_bytes_array = bytearray()
        packet_bytes_array.append(packet.p_type)
        packet_bytes_array += bytearray(packet.p_checksum)
        packet_bytes_array += bytearray(packet.p_dest.packed)
        packet_bytes_array += packet.p_data.encode()
        packet_bytes = bytes(packet_bytes_array)
        return packet_bytes

    def decode_packet(self, packet_bytes):
        packet_type = packet_bytes[0]
        packet_checksum = packet_bytes[1:33]
        packet_dest = packet_bytes[33:37]
        packet_data = packet_bytes[37:]

        if (
            self._calc_checksum(
                bytes(packet_type), bytes(packet_dest), bytes(packet_data)
            )
            != packet_checksum
        ):
            raise DecodeErrorChecksum(packet_bytes)
        else:
            packet = Packet(packet_type, packet_dest, packet_data.decode())
            return packet

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

    def _calc_checksum(self, packet_type, packet_dest, packet_data):
        checksum = hashlib.sha256()
        type_bytes = packet_type
        dest_bytes = packet_dest
        data_bytes = packet_data

        checksum.update(type_bytes)
        checksum.update(dest_bytes)
        checksum.update(data_bytes)

        return checksum.digest()
