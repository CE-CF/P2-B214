import hashlib
import ipaddress


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

    def __init__(self, m_type="heart", m_dest="127.0.0.1", m_data=""):
        self.p_type = m_type
        self.p_dest = m_dest
        self.p_data = m_data
        self._set_checksum()

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
            pass

    @property
    def p_checksum(self):
        return self._p_checksum

    # ---
    # Checksum should not be set from the outside,
    # it should be calculated based internal values
    # ---
    def _set_checksum(self):
        checksum = hashlib.sha256()
        type_bytes = bytes(self.p_type)
        dest_bytes = self.p_dest.packed  # TODO
        data_bytes = bytes(self.p_data.encode())

        checksum.update(type_bytes)
        checksum.update(dest_bytes)
        checksum.update(data_bytes)

        self._p_checksum = checksum.digest()

    @property
    def p_dest(self):
        return self._p_dest

    @p_dest.setter
    def p_dest(self, p_dest):
        self._p_dest = ipaddress.IPv4Address(p_dest)

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
