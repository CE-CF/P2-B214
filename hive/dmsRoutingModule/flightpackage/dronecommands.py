import threading
import socket
import sys
import time

response_arr = []
start_yaw = None

sent = None
recvThread = None

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
state_host = ''
state_port = 8890
address = (state_host, state_port)
sock.bind(address)

# Create socket to send commands and receive their response
tello_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_host = '192.168.10.1'
tello_port = 8889
tello_address = (tello_host, tello_port)


def recv():
    global start_yaw
    count = 0
    while True:
        data, server = sock.recvfrom(2046)
        if data == b'ok':
            print("ok")
        elif data == b'error':
            print("error")
        else:
            response_arr.append(data_parser(data.decode(encoding="utf-8")))
            #print(response_arr[-1])
            if count == 0:
                start_yaw = response_arr[0]
                print("Start yaw is " + str(start_yaw))
        count = count + 1


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
    # print('cmd: ' + cmd)
    try:
        if 'end' in cmd:
            print('ending')
            tello_sock.close()
            tello_sock.shutdown(1)
            pass

        # Send data
        cmd = cmd.encode(encoding="utf-8")
        sent = tello_sock.sendto(cmd, tello_address)
        # print(response_arr[-1])               # make tello state work - array rn is empty
    except KeyboardInterrupt:
        print('\n . . .\n')

        cmd = "land".encode(encoding="utf-8")
        sent = tello_sock.sendto(cmd, tello_address)

        tello_sock.close()
        tello_sock.shutdown(1)


def correct_yaw(distance):
    global start_yaw
    delay = 1
    start_time = time.time()
    correct_yaw_start = int(response_arr[-1])                           # is defined only when function is called
    is_deviating = False
    new_yawk = None
    yaw_per_sec = 0
    while (time.time() - start_time) < distance:                        # if the drone flies at 1 m/s then this works
        print(str(distance - (time.time() - start_time)) + " seconds left before turning")
        newest_yaw_response = int(response_arr[-1])                     # is redefined after each loop
        # check yaw status
        if newest_yaw_response == int(start_yaw):                       # no deviation
            pass
        else:                                                           # deviation
            is_deviating = True

        # change yaw
        if is_deviating:
            #new_yawk = int(start_yaw) - newest_yaw_response
            #yaw_per_sec = (new_yawk / delay)
            if yaw_per_sec > 100:
                yaw_per_sec = 100
            elif yaw_per_sec < -100:
                yaw_per_sec = -100
            if start_yaw > 0:
                new_yawk = int(start_yaw) - newest_yaw_response
                yaw_per_sec = (new_yawk / delay)
            elif start_yaw < 0:
                new_yawk = int(start_yaw) + newest_yaw_response
                yaw_per_sec = (new_yawk / delay)
            is_deviating = False
            print(newest_yaw_response)
        else:
            new_yawk = 0

        rc_string = "rc 0 80 0 " + str(yaw_per_sec)
        # rc_string = "rc 0 10 0 0"

        print("new york: " + rc_string + "\t\told yaw: " + str(start_yaw))
        the_thread(rc_string)

        time.sleep(delay)


def search_turns(cmd, semi_circle, left_right):
    start_time = time.time()

    # semi circle is the
    # drone flies with 1 m/s which means that the value of semi_circle is the time it takes for the drone
    # to complete its turn
    # print(semi_circle)

    left_right_str = ""

    if left_right:
        left_right_str = "left"
    else:
        left_right_str = "right"

    while (time.time() - start_time) < semi_circle:
        the_thread(cmd)
        # print(str(semi_circle - (time.time() - start_time)) + " seconds left of this " + left_right_str + " turn")


def instantiate():
    global sent, recvThread, event
    # print('\r\n\r\nTello Python3 Demo.\r\n')
    # print('Tello: command takeoff land flip forward back left right \r\n       up down cw ccw speed speed?\r\n')

    # recvThread create
    recvThread = threading.Thread(target=recv)
    recvThread.start()

    # time.sleep(2)

    print("Instantiation commenced")

    cmd = "command".encode(encoding="utf-8")
    sent = tello_sock.sendto(cmd, tello_address)

    time.sleep(2)

    cmd = "rc 0 0 0 0".encode(encoding="utf-8")
    sent = tello_sock.sendto(cmd, tello_address)

    print("Drone's been initialized")
    print("Three seconds to takeoff!")
    time.sleep(1)
    print("Two seconds to takeoff!")
    time.sleep(1)
    print("One second to takeoff!")
    time.sleep(1)

    the_thread("takeoff")
    print("We are airborne!!!")
    time.sleep(3)