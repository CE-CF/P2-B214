import hashlib


class Packet:
    # Attributes
    _p_type = None
    _p_checksum = None
    _p_dest = None
    _p_data = None

    def __init__(self, m_type="heart", m_dest=None, m_data=None):
        self.p_type = m_type
        self.p_dest = m_dest
        self.p_data = m_data
        self._set_checksum()

    @property
    def p_type(self):
        return self._p_type

    @p_type.setter
    def p_type(self, p_type):
        self._p_type = {
            "wayp": 0,
            "bound": 1,
            "drone": 2,
            "heart": 3,
        }[p_type]

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
        dest_bytes = bytes(self.p_dest)
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
        self._p_dest = p_dest

    @property
    def p_data(self):
        return self._p_data

    @p_data.setter
    def p_data(self, p_data):
        self._p_data = p_data
