from .error import Error


class EncodeError(Error):
    """Raised when the packet encoding failed"""

    pass


class EncodeErrorPacket(EncodeError):
    """Raised if the packet is not correct"""

    def __init__(
        self, packet, message="There was a problem with the supplied packet"
    ):
        self.packet = packet
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"Packet content: {self.packet}; Type:{type(self.packet)} -> {self.message}"


class DecodeError(Error):
    """Raised when the packet decoding failed"""


class DecodeErrorChecksum(DecodeError):
    """Raiesd if the bytes cannot be decoded correctly"""

    def __init__(
        self, checksum, expected, message="Error in packet, checksum error"
    ):
        self.checksum = checksum
        self.expected = expected
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"Expected checksum: {self.expected}\nReceived checksum: {self.checksum}"


class PacketTypeError(Error):
    """Raised if the Packet type is wrong"""
