import hashlib
import ipaddress
from ..exceptions.packet_exceptions import *


class Packet:
    """
    This is a class for the packets, in the Hive system, being sent between:
      - Operator PC
      - Data Management System
      - Relay box

    Attributes:
     p_type (int): (default: \"heart\")
           The packet type, can be assigned by either 0,1,2,3
           or by writing one of the strings \"wayp\", \"bound\", \"drone\" or \"heart\"
     p_checksum (bytes object):
           This attributes is calculated based on packet type, destination and data.
     p_dest (string): (default: '127.0.0.1')
           This is the packet destination, should only be used when communicating directly with a drone.
     p_data (string):
           This attribute holds the data that should be sent over the protocol

    Methods:
     dump() :: dumps packet information to console
    === static ===
     encode_packet(packet) :: Encode the packet into bytes
     decode_packet(packet_bytes: bytes) :: Decodes received data into a Packet object
     calc_checksum(packet_type: bytes, packet_dest: bytes, packet_data: bytes)
         :: Calculates the packets checksum, useful for error checking
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

        # Set checksum based on received information
        self.p_checksum = self.calc_checksum(
            bytes(self.p_type), self.p_dest.packed, self.p_data.encode()
        )

    @property
    def p_type(self):
        return self._p_type

    @p_type.setter
    def p_type(self, p_type):
        """A setter for the p_type

        :param p_type:
        :type p_type:
        :returns:

        """
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
    def p_dest(self, dest):
        try:
            self._p_dest = ipaddress.IPv4Address(dest)
        except:
            print(
                f"""Something is wrong with destination address. Please make sure it is correct:
{p_dest}"""
            )

    @property
    def p_data(self):
        return self._p_data

    @p_data.setter
    def p_data(self, data: str):
        self._p_data = data

    def dump(self):
        """ Dumps packet information to terminal

        :returns: 

        """
        print("=====================================")
        print("|          Packet content           |")
        print("=====================================")
        print(f"[TYPE]: {self.p_type}")
        print(f"[CHECKSUM]: {self.p_checksum}")
        print(f"[DESTINATION]: {self.p_dest}")
        print(f"[DATA]: {self.p_data}")
        print("=====================================")

    @staticmethod
    def encode_packet(packet):
        """Encode the packet object into bytes.

        :param packet:
        :type packet: Packet
        :returns: bytes

        """
        if type(packet) is not Packet: # Make sure argument is of type Packet
            raise EncodeErrorPacket(
                packet, f"Argument is not of type: {type(Packet())} "
            )

        # Put everything into a bytearray
        packet_bytes_array = bytearray()
        packet_bytes_array.append(packet.p_type)
        packet_bytes_array += bytearray(packet.p_checksum)
        packet_bytes_array += bytearray(packet.p_dest.packed)
        packet_bytes_array += packet.p_data.encode()
        packet_bytes_array += bytearray(0x00) # Add null terminator not used atm but will be used to know when data is done

        # Return as bytes object ready for send off
        return bytes(packet_bytes_array)
        

    # @explain
    @staticmethod
    def decode_packet(packet_bytes: bytes):
        """Decodes bytes and tries to convert them into a packet

        :param packet_bytes:
        :type packet_bytes:
        :returns: Packet

        """
        # Since the packet is designed to be more or less static(except for data segment)
        # Each packet attribute can be assigned through indexing bytes object :)
        packet_type = packet_bytes[0]
        packet_checksum = packet_bytes[1:33]
        packet_dest = packet_bytes[33:37]
        packet_data = packet_bytes[37:]

        # Chech if any errors occured 
        if (
            self.calc_checksum(
                bytes(packet_type), bytes(packet_dest), bytes(packet_data)
            )
            != packet_checksum
        ):
            raise DecodeErrorChecksum(packet_bytes)
        else:
            return Packet(packet_type, packet_dest, packet_data.decode())
             

    @staticmethod
    def calc_checksum(packet_type: bytes, packet_dest: bytes, packet_data: bytes):
        """Calculates the checksum for a Packet

        :param packet_type:
        :type packet_type: bytes
        :param packet_dest:
        :type packet_dest: bytes
        :param packet_data:
        :type packet_data: bytes
        :returns: bytes

        """
        # Create hash object
        checksum = hashlib.sha256()

        # Throw everything into object
        checksum.update(packet_type)
        checksum.update(packet_dest)
        checksum.update(packet_data)

        # Return bytes object of checksum
        return checksum.digest()
