import logging
import threading
from abc import ABC, abstractmethod
from datetime import datetime
from socket import (
    AF_INET,
    SHUT_RDWR,
    SOCK_DGRAM,
    SOCK_STREAM,
    gethostname,
    socket,
    timeout,
)
from time import sleep

from hive.communication import BUFFER_SIZE, CONN_TYPE_TCP, CONN_TYPE_UDP
from hive.exceptions.packet_exceptions import DecodeErrorChecksum
from hive.utils.decorators import setInterval

from .packet import HiveT, HiveU, Packet

# =====================
# LOGGING RELATED
# Change logging level when done
logging.basicConfig(filename="client.log", level=logging.DEBUG)


class Client(ABC):
    """Base class for hive clients

    Attributes:
     srv_port_tcp: Integer :: Server port for TCP connection
     srv_port_udp: Integer :: Server port for UDP connection
     srv_ip: String :: Server IP address ex: \"127.0.0.1\"
     client_sock: socket object :: Client socket object
     pulse: Boolean :: If there is a \"pulse\"

    Methods:
     connect(mode=CON_TYPE_TCP) :: Connect to server
     send_message(mtype, mdest, mdata) :: Send packet with message to server
     send_heartbeat() :: Sends a heartbeat packet to server
                         | decorator: @setInterval
     start() :: Starts the client and executes the run method
     run(packet: Packet) :: Abstract method used to handle packets
                            Override this
    """

    # Attributes
    _srv_port_tcp = None
    _srv_port_udp = None
    _srv_ip = None
    _client_sock = None
    _pulse = False
    _mode = None

    # Constructor
    def __init__(
        self,
        srv_ip,
        name="Client",
        mode=CONN_TYPE_TCP,
        tcp_port=None,
        udp_port=None,
        other_client=None,
    ):
        """Constructor for hive Client objects

        :param srv_ip:
        :type srv_ip: String
        :param tcp_port:
        :type tcp_port: Integer
        :param udp_port:
        :type udp_port: Integer
        :returns:

        """
        self.srv_ip = srv_ip
        self.name = name
        self.mode = mode
        self.other_client = other_client

        if mode is CONN_TYPE_TCP:
            self.srv_port_tcp = tcp_port
            self.client_sock = socket(AF_INET, SOCK_STREAM)
        else:
            self.srv_port_udp = udp_port
            self.client_sock = socket(AF_INET, SOCK_DGRAM)
            #self.client_sock.settimeout(1)
            self.client_sock.bind(("", 0))

    def log_info(self, msg: str):
        """Logging helper

        :param msg:
        :type msg: str

        """
        log_format = f"[ TIME {datetime.now()} ]: {msg}"
        logging.info(log_format)

    def log_warning(self, msg: str):
        """Logging helper

        :param msg:
        :type msg: str

        """
        log_format = f"[ TIME {datetime.now()} ]: {msg}"
        logging.warning(log_format)

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        self._mode = mode

    @property
    def srv_port_tcp(self):
        return self._srv_port_tcp

    @srv_port_tcp.setter
    def srv_port_tcp(self, port: int):
        self._srv_port_tcp = port

    @property
    def srv_port_udp(self):
        return self._srv_port_udp

    @srv_port_udp.setter
    def srv_port_udp(self, port: int):
        """Setter for the server udp port

        :param port:
        :type port: int
        :returns:

        """
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

    @property
    def pulse(self):
        """Pulse getter

        :returns: bool

        """
        return self._pulse

    @pulse.setter
    def pulse(self, pulse: bool):
        """Pulse setter

        :param pulse:
        :type pulse: bool
        :returns:

        """
        self._pulse = pulse

    def connect(self):
        """Connection wrapper function

        :param mode:
        :type mode: bool
        :returns:

        """
        if self.mode is CONN_TYPE_TCP:  # True == TCP | False == UDP
            self.client_sock.connect((self.srv_ip, self.srv_port_tcp))
        else:
            self.client_sock.connect((self.srv_ip, self.srv_port_udp))

    def send_udp(self, ident, ptype, seq, data):
        packet = HiveU(ident, ptype, seq, data)
        #print(f'Sending packet: {packet.ptype}, {packet.identifier}, {packet.seq}, {packet.data}')
        self.client_sock.send(packet.encode())

    def send_message(self, mtype, mdest, mdata):
        """Create and send packet with data

        :param mtype:
        :type mtype:
        :param mdest:
        :type mdest:
        :param mdata:
        :type mdata:
        :returns:

        """
        packet = HiveT(mtype, mdest, mdata)
        msg_bytes = HiveT.encode_packet(packet)
        self.client_sock.send(msg_bytes)

    def recvall(self):
        """Receive all of incoming packet

        :returns: Message in bytes

        """
        msg = b""
        while True:
            try:
                data_part = self.client_sock.recv(BUFFER_SIZE)
                msg += data_part
                if len(data_part) < BUFFER_SIZE:
                    break
            except timeout:
                print(f"recvall in client timed out")
                continue
            except ConnectionResetError:
                print(f"recvall in client Connection Reset Error")
                break
        return bytes(msg)

    @setInterval(5)
    def send_heartbeat(self):
        """Send a heartbeat packet to server

        @setInterval(5) :: repeats in thread call once

        :returns:

        """
        packet = HiveT(p_data="Pulsecheck")
        msg_bytes = HiveT.encode_packet(packet)
        self.client_sock.send(msg_bytes)
        print("==HEARTBEAT SENT==")

    @abstractmethod
    def run(self, packet: Packet):
        """The \"loop\" function of the Client class. All necessary packet
        handling should be done in here. The function is run as long as there
        is a pulse.

        :param packet:
        :type packet: Packet

        """
        pass

    def _set_pulse(self, packet: HiveT):
        if packet.p_type == 3:
            self.pulse = True

    def run_cmd(self, cmd_dict: dict):
        cmd = cmd_dict["CMD"]
        args = {}
        # Parse cmd args from dict
        for key in cmd_dict.keys():
            if key != "CMD":
                args[key] = cmd_dict[key]

        # Run the commands
        if cmd == "MIGRATE":
            new_port = int(args["P"])
            self.client_sock.shutdown(SHUT_RDWR)
            self.client_sock.close()
            self.client_sock = socket(AF_INET, SOCK_STREAM)
            self.client_sock.connect((self.srv_ip, new_port))
            print("Migration completed")

    def tcp_flow(self):
        self.pulse = False

        # Send initial information
        if self.other_client is not None:
            self.send_message(
                "sccmd",
                self.srv_ip,
                f"CMD:ADD_CLIENT;NAME:{self.name};"
                + f"UDP:{self.other_client.client_sock.getsockname()[1]};",
            )
        else:
            self.send_message(
                "sccmd", self.srv_ip, f"CMD:ADD_CLIENT;NAME:{self.name};"
            )

        # Receive transfer info
        mig_msg = self.recvall()
        mig_packet = HiveT.decode_packet(mig_msg)

        mig_data = mig_packet.data_parser()

        if mig_data["CMD"] is not None:
            port = mig_data["P"]
            self.log_info(f"Received migration info: {port}")
            self.run_cmd(mig_data)

        self.log_info("Sending OK to new connection")
        self.send_message("sccmd", "127.0.0.1", "OK")

        while True:
            # Receive msg
            msg = self.recvall()
            packet = HiveT.decode_packet(msg)
            if packet == False:
                continue
            # Log client info
            # ---
            p_dump = packet.dump(to_stdout=False)
            log_string = ""
            for k in p_dump:
                log_string += f"[{k.upper()}]: {p_dump[k]}"
                log_string += "\n\t\t\t\t\t\t\t"

            self.log_info(
                "Packet received content:" + "\n\t\t\t\t\t\t\t" + log_string
            )
            self.log_info(f"PULSE: {self.pulse}")
            # ---
            self.run(packet)

    def recv_udp(self):
        try:
            bytes_addr = self.client_sock.recvfrom(BUFFER_SIZE)
            return bytes_addr[0], bytes_addr[1]
        except timeout:
            print(f"recv_udp in client timed out")
            return False, False
        except ConnectionResetError:
            #print(f"recv_udp in client Connection Reset Error")
            return False, False

    def udp_flow(self):
        self.run(packet=None)
        while True:
            # Receive msg
            msg, addr = self.recv_udp()
            if type(msg) == type(False) or type(addr)  == type(False):
                continue
            packet = HiveU.decode(msg)

            # Log client info
            # ---
            p_dump = packet.dump(to_stdout=False)
            log_string = ""
            for k in p_dump:
                log_string += f"[{k.upper()}]: {p_dump[k]}"
                log_string += "\n\t\t\t\t\t\t\t"

            self.log_info(
                "Packet received content:" + "\n\t\t\t\t\t\t\t" + log_string
            )
            self.run(packet)

    def start(self):
        """Start the client and execute the abstract run method

        :returns:

        """
        try:
            # Client boilerplate code
            self.connect()
            print("Client started")
            self.log_info("STARTED")
            if self.mode is CONN_TYPE_TCP:
                print("MODE: TCP")
                self.tcp_flow()
            elif self.mode is CONN_TYPE_UDP:
                print("MODE: UDP")
                self.udp_flow()
        # "Catch" some exceptions
        except DecodeErrorChecksum:
            self.log_warning("CHECKSUM ERROR")
        except KeyboardInterrupt:
            print("Stopping client")
            self.log_info("STOPPED")
            self.client_sock.shutdown(SHUT_RDWR)
            self.client_sock.close()
        except ConnectionRefusedError:
            # Server not available, try again in 5.. 4.. 3.. 2.. 1..
            retry_int = 5
            self.log_warning(f"Connection refused retrying in {retry_int}")
            print("Connection refused:")
            print(
                "Please make sure that the server is running,"
                + " and that settings are correct"
            )
            print("[ CLIENT SETTINGS ]")
            print(f"SERVER IP: {self.srv_ip}")
            print(f"SERVER PORT(tcp): {self.srv_port_tcp}")
            print(f"SERVER PORT(udp): {self.srv_port_udp}")
            print()
            print(f"Trying again in {retry_int} seconds")
            sleep(retry_int)
            self.start()
