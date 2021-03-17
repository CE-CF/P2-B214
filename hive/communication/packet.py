import hashlib
import ipaddress
from ..exceptions.packet_exceptions import *


def encode_packet(packet: Packet):
    """Encode the packet object into bytes.

    :param packet:
    :type packet: Packet
    :returns: bytes

    """
    if type(packet) is not Packet:
        raise EncodeErrorPacket(packet, f"Argument is not of type: {type(Packet())} ")

    packet_bytes_array = bytearray()
    packet_bytes_array.append(packet.p_type)
    packet_bytes_array += bytearray(packet.p_checksum)
    packet_bytes_array += bytearray(packet.p_dest.packed)
    packet_bytes_array += packet.p_data.encode()
    packet_bytes_array += bytearray(0x00)
    packet_bytes = bytes(packet_bytes_array)
    return packet_bytes


def decode_packet(packet_bytes: bytes):
    """Decodes bytes and tries to convert them into a packet

    :param packet_bytes:
    :type packet_bytes:
    :returns: Packet

    """
    packet_type = packet_bytes[0]
    packet_checksum = packet_bytes[1:33]
    packet_dest = packet_bytes[33:37]
    packet_data = packet_bytes[37:]

    if (
        _calc_checksum(bytes(packet_type), bytes(packet_dest), bytes(packet_data))
        != packet_checksum
    ):
        raise DecodeErrorChecksum(packet_bytes)
    else:
        packet = Packet(packet_type, packet_dest, packet_data.decode())
        return packet


def _calc_checksum(packet_type: bytes, packet_dest: bytes, packet_data: bytes):
    """Calculates the checksum for a Packet

    :param packet_type:
    :type packet_type: bytes
    :param packet_dest:
    :type packet_dest: bytes
    :param packet_data:
    :type packet_data: bytes
    :returns: bytes

    """
    checksum = hashlib.sha256()
    type_bytes = packet_type
    dest_bytes = packet_dest
    data_bytes = packet_data

    checksum.update(type_bytes)
    checksum.update(dest_bytes)
    checksum.update(data_bytes)

    return checksum.digest()


class Packet:
    """
    This is a class for the packets, in the Hive system, being sent between:
      - Operator PC
      - Data Management System
      - Relay box

    Attributes:
      - p_type (int): (default: \"heart\")
              The packet type, can be assigned by either 0,1,2,3
              or by writing one of the strings \"wayp\", \"bound\", \"drone\" or \"heart\"
      - p_checksum (bytes object):
              This attributes is calculated based on packet type, destination and data.
      - p_dest (string): (default: '127.0.0.1')
              This is the packet destination, should only be used when communicating directly with a drone.
      - p_data (string):
              This attribute holds the data that should be sent over the protocol
    """

    # Attributes
    _p_type = None
    _p_checksum = None
    _p_dest = None
    _p_data = None

    def __init__(self, p_type="heart", p_dest="127.0.0.1", p_data=""):
        self.p_type = p_type
        self.p_dest = p_dest
        self.p_data = p_data
        self.p_checksum = _calc_checksum(
            bytes(self.p_type), self.p_dest.packed, self.p_data.encode()
        )

    @property
    def p_type(self):
        return self._p_type

    @p_type.setter
    def p_type(self, p_type):
        if type(p_type) is str:
            self._p_type = {
                "wayp": 0,
                "bound": 1,
                "drone": 2,
                "heart": 3,
            }[p_type]
        elif type(p_type) is int and p_type in [0, 1, 2, 3]:
            self._p_type = p_type
        else:
            raise PacketTypeException

    @property
    def p_checksum(self):
        return self._p_checksum

    @p_checksum.setter
    def p_checksum(self, checksum: bytes):
        self._p_checksum = checksum

    @property
    def p_dest(self):
        return self._p_dest

    @p_dest.setter
    def p_dest(self, p_dest):
        try:
            self._p_dest = ipaddress.IPv4Address(p_dest)
        except:
            print(
                f"""Something is wrong with destination address. Please make sure it is correct:
{p_dest}"""
            )

    @property
    def p_data(self):
        return self._p_data

    @p_data.setter
    def p_data(self, p_data):
        self._p_data = p_data

    def dump(self):
        """Prints all of the content of the packet"""
        print("=====================================")
        print("|          Packet content           |")
        print("=====================================")
        print(f"[TYPE]: {self.p_type}")
        print(f"[CHECKSUM]: {self.p_checksum}")
        print(f"[DESTINATION]: {self.p_dest}")
        print(f"[DATA]: {self.p_data}")
        print("=====================================")
