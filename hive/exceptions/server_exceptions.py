from .error import Error


class EncodeError(Error):
    """Raised when the packet encoding failed"""

    pass


class EncodeErrorPacket(EncodeError):
    """Raised if the packet is not correct"""

    def __init__(self, packet, message="There was a problem with the supplied packet"):
        self.packet = packet
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return (
            f"Packet content: {self.packet}; Type:{type(self.packet)} -> {self.message}"
        )


class DecodeError(Error):
    """Raised when the packet decoding failed"""


class DecodeErrorChecksum(DecodeError):
    """Raiesd if the bytes cannot be decoded correctly"""

    def __init__(self, rcv_bytes, message="Error in packet, checksum error"):
        self.rcv_bytes = rcv_bytes
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"Bytes: {self.rcv_bytes} -> {self.message}"
