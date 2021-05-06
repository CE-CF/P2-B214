import threading
import socket
import sys
import time

response_arr = []

sent = None
recvThread = None

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
state_host = ''
state_port = 8890
address = (state_host, state_port)
sock.bind(address)

# Create socket to send commands and receive their response
cmd_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_host = '192.168.10.1'
tello_port = 8889
tello_address = (tello_host, tello_port)
cmd_sock.connect(tello_address)


def recv():
    while True:
        data, server = sock.recvfrom(2046)
        if data == b'ok':
            print("ok")
        elif data == b'error':
            print("error")
        else:
            #response_arr.append(data_parser(data.decode(encoding="utf-8")))
            print(data_parser(data.decode(encoding="utf-8")))


def data_parser(data):
    """Parse incoming packet data for easier manipulation

    :param data:
    :type data: str
    :returns: Dictionary containing data

    """

    d = {}
    delim1 = ";"
    delim2 = ":"
    element = ""
    for _, v in enumerate(data):
        if v is not delim1:
            element += v
        else:
            arr = element.split(delim2)
            d[arr[0]] = arr[1]
            element = ""

    return d['yaw']


def the_thread(cmd):
    global sent, event
    try:
        if 'end' in cmd:
            print('ending')
            sock.close()
            pass

        # Send data
        cmd = cmd.encode(encoding="utf-8")
        sent = sock.sendto(cmd, tello_address)
        # print(response_arr[-1])               # make tello state work - array rn is empty
    except KeyboardInterrupt:
        print('\n . . .\n')

        cmd = "land".encode(encoding="utf-8")
        sent = sock.sendto(cmd, tello_address)

        sock.close()
        sock.shutdown(1)


def instantiate():
    global sent, recvThread, event
    print('\r\n\r\nTello Python3 Demo.\r\n')
    print('Tello: command takeoff land flip forward back left right \r\n       up down cw ccw speed speed?\r\n')

    # recvThread create
    recvThread = threading.Thread(target=recv)
    recvThread.start()

    time.sleep(2)

    cmd = "command".encode(encoding="utf-8")
    sent = sock.sendto(cmd, tello_address)

    print("Drone's been initialized")

    time.sleep(2)

    # cmd = "takeoff".encode(encoding="utf-8")
    # sent = sock.sendto(cmd, tello_address)

    # print("Drone has taken off")
