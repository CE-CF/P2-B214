import threading
import socket
import sys
import time

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
state_host = ''
state_port = 8891   # 8890
address = (state_host, state_port)
sock.bind(address)

# Create socket to send commands and receive their response
tello_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_host = '192.168.10.1'
tello_port = 8888   # 8889
tello_address = (tello_host, tello_port)

yaw_response = []
yaw = 0
oppo_yaw = 0


# # # GETTER # # #

def get_yaw_response():
    return int(yaw_response[-1])


# # # UPLINK AND DOWNLINK # # #

def downlink():
    count = 0
    while True:
        data, server = sock.recvfrom(2046)
        if data == b'ok':
            print("ok")
        elif data == b'error':
            print("error")
        else:
            yaw_response.append(parser(data.decode(encoding="utf-8")))


def uplink(cmd):
    try:
        if 'end' in cmd:
            print('ending')
            tello_sock.close()
            tello_sock.shutdown(1)
            pass
        cmd = cmd.encode(encoding="utf-8")
        tello_sock.sendto(cmd, tello_address)
    except KeyboardInterrupt:
        print('\nKeyboardInterrupt\n')
        cmd = "land".encode(encoding="utf-8")
        tello_sock.sendto(cmd, tello_address)
        tello_sock.close()
        tello_sock.shutdown(1)


# # # PATH FOLLOWING

def straight(straight_yaw, flight_time):
    drone_speed = 100
    delay = 1
    is_deviating = False

    start_time = time.time()

    while (time.time() - start_time) < float(flight_time):              # if the drone flies at 1 m/s then this works
        if float(flight_time) - (time.time() - start_time) < 2:
            print()
            drone_speed = 40

        newest_yaw_response = get_yaw_response()                        # is redefined after each loop
        newest_yaw_response = int(newest_yaw_response)                  # for some reason it doesn't work in one line..

        if newest_yaw_response == int(straight_yaw):                             # no deviation
            pass
        else:                                                           # if there is deviation...
            is_deviating = True                                         # <-- this is set to true

        if is_deviating:
            from_yaw = newest_yaw_response + 180
            to_yaw = int(straight_yaw) + 180

            if from_yaw < to_yaw:                                       # checking if the drone should turn cw or ccw
                diff = to_yaw - from_yaw
                if diff < 180:
                    yaw_per_sec = abs(diff / delay)                     # these lines of code calculate
                else:                                                   # the angle between the current drone
                    yaw_per_sec = -abs((360-diff) / delay)              # yaw and the correct drone yaw
            else:
                diff = from_yaw - to_yaw                                # the code also takes the overflowing
                if diff < 180:                                          # yaw values from -180 to 180 into account
                    yaw_per_sec = -abs(diff / delay)                    # so that the shortest angle is always found
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
        uplink(rc_string)
        time.sleep(delay)


# # # COMMANDS # # #

def base_commands(cmd):
    global yaw_response, yaw, oppo_yaw

    if cmd == "init":
        print(cmd)
        downlink_thread = threading.Thread(target=downlink)
        downlink_thread.start()
        uplink("command")
        time.sleep(2)
        uplink("rc 0 0 0 0")
        time.sleep(2)
        uplink("takeoff")
        time.sleep(5)

    elif cmd == "rc0":
        print(cmd)
        uplink("rc 0 0 0 0")

    elif cmd == "stop":
        print(cmd)
        uplink(cmd)

    elif cmd == "land":

        print(cmd)
        uplink(cmd)

    elif cmd == "getyaw":
        print(cmd)
        if len(yaw_response) != 0:            # if array is empty ... this is due to no tello states coming in
            yaw = yaw_response[-1]
        else:
            yaw_response.append(0)
            print("yaw has been set to 0 - use this for test purposes")

    elif cmd == "getoppoyaw":
        print(cmd)
        if yaw < 0:
            oppo_yaw = 180 + yaw
        elif yaw > 0:
            oppo_yaw = yaw - 180
        else:
            oppo_yaw = 179


def param_commands(cmd, value):
    if cmd == "rotate":
        if int(float(value)) < 0:
            pass
            print("ccw ", abs(int(float(value))))
            uplink("ccw " + str(abs(int(float(value)))))
        elif int(float(value)) > 0:
            pass
            print("cw ", abs(int(float(value))))
            uplink("cw " + str(abs(int(float(value)))))
        else:
            pass                                        # don't rotate

    if cmd == "wait":
        print(cmd, value)
        time.sleep(int(value))

    if cmd == "straight":
        print(cmd, value[0], value[1])
        if value[0] == "yaw":
            straight(yaw, flight_time=value[1])
        elif value[0] == "oppoyaw":
            straight(oppo_yaw, flight_time=value[1])
        else:
            straight(int(value[0]), flight_time=value[1])               # if it already has a value

    if cmd == "turn":
        print(cmd, value[0], value[1])
        start_time = time.time()
        cmd = "rc 0 50 0 " + str(value[0])
        while (time.time() - start_time) < float(value[1]):
            uplink(cmd)


def parser(cmd_str):
    d = {}
    delim1 = ";"
    delim2 = ":"
    element = ""
    print(cmd_str)
    for _, v in enumerate(cmd_str):
        if v is not delim1:
            element += v
        else:
            arr = element.split(delim2)
            #print("HEEEEEEEY   ", arr, len(arr))
            if len(arr) == 1:
                base_commands(arr[0])
            elif len(arr) == 2:
                if arr[0] == "yaw":                 # downlink() needs to parse yaw
                    return arr[1]
                param_commands(arr[0], arr[1])
            elif len(arr) == 3:
                # print("boooooo   ", arr, len(arr))
                #print("boooooo  ", arr[0], [arr[1], arr[2]])
                param_commands(arr[0], [arr[1], arr[2]])
            element = ""
    #print(d)