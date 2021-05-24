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
# sock.bind(address)

# Create socket to send commands and receive their response
tello_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_host = '192.168.10.1'
tello_port = 8889
tello_address = (tello_host, tello_port)


def get_yaw():
    return response_arr[-1]


def recv():
    count = 0
    while True:
        data, server = sock.recvfrom(2046)
        if data == b'ok':
            print("ok")
        elif data == b'error':
            print("error")
        else:
            response_arr.append(data_parser(data.decode(encoding="utf-8")))
            # print(response_arr[-1])   sometimes response array dont append if this is not uncommented??

        if count == 0:
            print("drone yaw at takeoff", response_arr[0])
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
    print('cmd: ', cmd)
    try:
        if 'end' in cmd:
            print('ending')
            tello_sock.close()
            tello_sock.shutdown(1)
            pass

        cmd = cmd.encode(encoding="utf-8")
        sent = tello_sock.sendto(cmd, tello_address)

    except KeyboardInterrupt:
        print('\n . . .\n')

        cmd = "land".encode(encoding="utf-8")
        sent = tello_sock.sendto(cmd, tello_address)

        tello_sock.close()
        tello_sock.shutdown(1)


def correct_yaw(yaw, flight_time):
    yaw = int(yaw)
    drone_speed = 100
    delay = 1
    start_time = time.time()
    correct_yaw_start = int(response_arr[-1])                           # is defined only when function is called
    is_deviating = False
    new_yawk = None
    yaw_per_sec = 0
    while (time.time() - start_time) < flight_time:                     # if the drone flies at 1 m/s then this works
        if flight_time - (time.time() - start_time) < 2:
            print()
            drone_speed = 40

        newest_yaw_response = int(response_arr[-1])                     # is redefined after each loop

        # check yaw status
        if newest_yaw_response == int(yaw):                             # no deviation
            pass
        else:                                                           # deviation
            is_deviating = True

        newest_yaw_response = int(newest_yaw_response)

        # change yaw
        if is_deviating:
            from_yaw = newest_yaw_response + 180
            to_yaw = yaw + 180

            if from_yaw < to_yaw:
                diff = to_yaw - from_yaw
                if diff < 180:
                    yaw_per_sec = abs(diff / delay)
                else:
                    yaw_per_sec = -abs((360-diff) / delay)
            else:
                diff = from_yaw - to_yaw
                if diff < 180:
                    yaw_per_sec = -abs(diff / delay)
                else:
                    yaw_per_sec = abs((360 - diff) / delay)

            if yaw_per_sec < -100:
                yaw_per_sec = -100
            elif yaw_per_sec > 100:
                yaw_per_sec = 100

            is_deviating = False
        else:
            yaw_per_sec = 0

        rc_string = "rc 0 " + str(drone_speed) + " 0 " + str(yaw_per_sec)
        the_thread(rc_string)

        time.sleep(delay)


def search_turns(degrees_pr_sec, flight_time):
    start_time = time.time()

    cmd = "rc 0 50 0 "
    cmd = cmd + str(degrees_pr_sec)

    while (time.time() - start_time) < flight_time:
        the_thread(cmd)


def instantiate():
    global sent, recvThread, event

    recvThread = threading.Thread(target=recv)
    recvThread.start()

    print("Instantiation commenced")

    cmd = "command".encode(encoding="utf-8")
    sent = tello_sock.sendto(cmd, tello_address)
    time.sleep(2)

    cmd = "rc 0 0 0 0".encode(encoding="utf-8")
    sent = tello_sock.sendto(cmd, tello_address)
    time.sleep(2)

    print("Drone's been initialized")
    time.sleep(1)
    print("Three seconds to takeoff!")
    time.sleep(1)
    print("Two seconds to takeoff!")
    time.sleep(1)
    print("One second to takeoff!")
    time.sleep(1)

    the_thread("takeoff")
    print("We are airborne!!!")
    time.sleep(5)



