import hashlib
import ipaddress
from abc import ABC, abstractmethod
from binascii import hexlify
from threading import Lock

from hive.exceptions.packet_exceptions import (
    DecodeErrorChecksum,
    EncodeErrorPacket,
    PacketTypeError,
)


class Packet(ABC):
    @abstractmethod
    def dump(self):
        pass


class HiveU(Packet):
    """
    This is the class for the UDP based packets in the Hive system.
    """

    def __init__(self, ident: int, ptype, seq: int, data: bytes):
        self.identifier = ident
        self.seq = seq
        self.ptype = ptype
        self.data = data

    # --------
    # Properties
    _identifier: int = 0
    _seq: int = 0
    _ptype: int = 0
    _data: bytes = bytes()

    # -------------------
    # Getters and setters
    @property
    def ptype(self):
        return self._ptype

    @ptype.setter
    def ptype(self, ptype):
        if type(ptype) is str:
            self._ptype = {
                "cmd": 0,
                "state": 1,
                "video": 2,
            }[ptype]
        elif type(ptype) is int and ptype in [0, 1, 2]:
            self._ptype = ptype
        else:
            raise PacketTypeError

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, ident: int):
        self._identifier = ident

    @property
    def seq(self):
        return self._seq

    @seq.setter
    def seq(self, seq: int):
        self._seq = seq

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data: bytes):
        self._data = data

    def dump(self, log=True, to_stdout=True):
        dump_data = {
            "identifier": self.identifier,
            "seq": self.seq,
            "type": self.ptype,
            "data": self.data,
        }
        if to_stdout:
            print("=====================================")
            print("|          HiveU content            |")
            print("=====================================")
            for k in dump_data:
                print(f"[{k.upper()}]: {dump_data[k]}")
            print("=====================================")

        if log:
            return dump_data

    def encode(self):
        packet_bytearray = bytearray()
        packet_bytearray.append(self.identifier)
        seq_bytes = self.seq.to_bytes(4, byteorder="big")
        packet_bytearray += seq_bytes
        packet_bytearray.append(self.ptype)
        packet_bytearray += bytearray(self.data)

        return bytes(packet_bytearray)

    # --------------
    # Static methods
    @staticmethod
    def decode(msg):
        ident = msg[0]  
        seq = msg[1:5]
        ptype = msg[5]
        data = msg[6:]
        seq_int = int.from_bytes(seq, byteorder="big")
        packet = HiveU(ident, ptype, seq_int, data)
        return packet


class HiveT(Packet):
    """
    This is the class for the TCP based packets in the Hive system, being sent
    between:
      - Operator PC
      - Data Management System
      - Relay box

    Attributes:
     p_type (int): (default: \"heart\")
           The packet type, can be assigned by either 0,1,2,3
           or by writing one of the strings \"wayp\", \"bound\", \"drone\" or
           \"heart\"
     p_checksum (bytes object):
           This attributes is calculated based on packet type, destination and
           data.
     p_dest (string): (default: '127.0.0.1')
           This is the packet destination, should only be used when
           communicating directly with a drone.
     p_data (string):
           This attribute holds the data that should be sent over the protocol

    Methods:
     dump() :: dumps packet information to console
    === static ===
     encode_packet(packet) :: Encode the packet into bytes
     decode_packet(packet_bytes: bytes) :: Decodes received data into a Packet
                                           object.
     calc_checksum(packet_type: bytes, packet_dest: bytes, packet_data: bytes)
         :: Calculates the packets checksum, useful for error checking
    """

    # Attributes
    _p_checksum = None
    _p_dest = None
    _p_type = None
    _p_data = None
    _src = None

    def __init__(self, p_type="sccmd", p_dest="127.0.0.1", p_data=""):
        self.p_type = p_type
        self.p_dest = p_dest
        self.p_data = p_data

        # Set checksum based on received information
        self.p_checksum = self.calc_checksum(
            bytes(self.p_type), self.p_dest.packed, self.p_data.encode()
        )

    @property
    def src(self):
        return self._src

    @src.setter
    def src(self, nsrc):
        self._src = nsrc

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
                "sccmd": 3,
            }[p_type]
        elif type(p_type) is int and p_type in [0, 1, 2, 3]:
            self._p_type = p_type
        else:
            raise PacketTypeError

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
                "Something is wrong with destination address."
                + f" Please make sure it is correct: {self.p_dest}"
            )

    @property
    def p_data(self):
        return self._p_data

    @p_data.setter
    def p_data(self, data: str):
        self._p_data = data

    def dump(self, log=True, to_stdout=True):
        """Dumps packet information to terminal

        :returns:

        """
        dump_data = {
            "type": self.p_type,
            "checksum": str(hexlify(self.p_checksum)),
            "dest": self.p_dest,
            "data": self.p_data,
        }

        if self.src is not None:
            dump_data["src"] = self.src

        if to_stdout:
            print("=====================================")
            print("|          HiveT content            |")
            print("=====================================")
            for k in dump_data:
                print(f"[{k.upper()}]: {dump_data[k]}")
            print("=====================================")
        if log:
            return dump_data

    def data_parser(self):
        """Parse incoming packet data for easier manipulation

        :param data:
        :type data: str
        :returns: Dictionary containing data

        """
        d = {}
        array = []
        delim1 = ";"
        delim2 = ":"
        element = ""
        for _, v in enumerate(self.p_data):
            if v is not delim1:
                element += v
            else:
                if self.p_type == 0 or self.p_type == 1:
                    tmp_arr = element.split(delim2)
                    tmp_arr2 = []
                    for x in tmp_arr:
                        nx = float(x)
                        tmp_arr2.append(nx)

                    array.append(tmp_arr2)
                    element = ""
                elif self.p_type == 2:
                    array.append(element)
                    element = ""
                elif self.p_type == 3:
                    arr = element.split(delim2)
                    d[arr[0]] = arr[1]
                    element = ""

        if self.p_type == 3:
            return d
        else:
            return array

    @staticmethod
    def encode_packet(packet):
        """Encode the packet object into bytes.

        :param packet:
        :type packet: Packet
        :returns: bytes

        """
        if type(packet) is not HiveT:  # Make sure argument is of type Packet
            raise EncodeErrorPacket(
                packet, f"Argument is not of type: {type(HiveT())} "
            )

        # Put everything into a bytearray
        packet_bytes_array = bytearray()
        packet_bytes_array += bytearray(packet.p_checksum)
        packet_bytes_array += bytearray(packet.p_dest.packed)
        packet_bytes_array.append(packet.p_type)
        packet_bytes_array += packet.p_data.encode()
        packet_bytes_array += bytearray(0x00)
        # Add null terminator not used atm but will be used to know when data is done

        # Return as bytes object ready for send off
        return bytes(packet_bytes_array)

    # @explain
    @staticmethod
    def decode_packet(packet_bytes: bytes):
        """Decodes bytes and tries to convert them into a packet

        In case of IndexError returns False

        :param packet_bytes:
        :type packet_bytes:
        :returns: HiveT

        """
        # Since the packet is designed to be more or less static
        # (except for data segment)
        # Each packet attribute can be assigned through indexing bytes object
        try:
            packet_checksum = packet_bytes[0:32]
            packet_dest = packet_bytes[32:36]
            packet_type = packet_bytes[36]
            packet_data = packet_bytes[37:]

            # Check if any errors occured
            lock = Lock()

            exp_check = HiveT.calc_checksum(
                bytes(packet_type), bytes(packet_dest), bytes(packet_data)
            )
            if exp_check != packet_checksum:
                raise DecodeErrorChecksum(packet_checksum, exp_check)
            else:
                return HiveT(packet_type, packet_dest, packet_data.decode())
        except IndexError:
            return False

    @staticmethod
    def calc_checksum(
        packet_type: bytes, packet_dest: bytes, packet_data: bytes
    ):
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
