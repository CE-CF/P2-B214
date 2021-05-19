from .dronecommands import instantiate, the_thread, correct_yaw, search_turns, yaw_reset, get_yaw

from routingpackage.distanceinmeters import DistanceInMeters
import math
import time
# from ..routingpackage.findroutefunctions import run
import numpy as np

drone_speed = 1


def get_to_route(path_limit_points, origo, relay_box_global_pos, path_functions, d_speed):
    print("GET TO ROUTE FUNCTION BEGINS")
    global drone_speed, relay_box_local_position
    if d_speed != 0:
        drone_speed = d_speed

    relay_box_local_position = [relay_box_global_pos[1] - origo[0], relay_box_global_pos[0] - origo[1]]
    route_starting_point = path_limit_points[0]
    # print(relay_box_local_position)
    # print([route_starting_point[1] + origo[1], route_starting_point[0] + origo[0]])
    '''
    route_starting_point[0] = x
    route_starting_point[1] = y
    '''
    instantiate()

    '''
    A third point is being created that has the same x-coordinate as the relay-box, 
    but larger in the y-coordinate. This creates a point straight north from the 
    relay-box.
    Let's call it mup (Made up point).
    '''
    mup = [relay_box_local_position[0], relay_box_local_position[1] + 1]
    '''
    Now these three points, will be translated to two vectors, from which
    it is possible to calculate angle.
    A vector from relay-box to first point is made first.
    '''
    rbfp = [route_starting_point[0] - relay_box_local_position[0],
            route_starting_point[1] - relay_box_local_position[1]]

    ''' 
    A second vector is made from relay-box to made up point.
    '''
    rbmup = [mup[0] - relay_box_local_position[0], mup[1] - relay_box_local_position[1]]
    '''
    Now the two vectors rbfp and rbmup are in place.
    Next step is to make two unit vectors, from the two vectors
    And then the dotproduct will reveal the angle to the first point
    '''
    unit_vector_1 = rbfp / np.linalg.norm(rbfp)
    unit_vector_2 = rbmup / np.linalg.norm(rbmup)
    angle_to_first_point = abs(np.degrees(np.arccos(np.dot(unit_vector_1, unit_vector_2))))
    '''
    Is the drone supposed to turn right or left?
    If the x-coordinate for the relay-box is greater  than that of the first point
    the drone will have to rotate left. If it is the opposite, the drone
    will rotate to the right.
    '''

    print("First rotation to get the right direction for the starting point")

    right = False
    left = False

    the_thread("stop")
    time.sleep(1)

    if relay_box_local_position[0] > route_starting_point[0]:
        # Rotate counterclockwise
        rotation_ccw = "ccw " + str(int(round(angle_to_first_point)))
        # print(rotation_ccw)
        left = True
        the_thread("stop")
        time.sleep(1)
        the_thread(rotation_ccw)
        time.sleep(3)

    elif relay_box_local_position[0] < route_starting_point[0]:
        # Rotate clockwise
        rotation_cw = "cw " + str(int(round(angle_to_first_point)))
        # print(rotation_cw)
        right = True
        the_thread("stop")
        time.sleep(1)
        the_thread(rotation_cw)
        time.sleep(3)

    else:
        # Fly straight up
        pass

    '''
    Now the drone should be in the right direction to just fly straight to
    the first point using the correct_yaw function.
    
    But first the newest yaw has to be set, to stay on this line
    '''

    # RESET YAW HERE !!!!!!!!!!!!!

    start_yaw = get_yaw()

    temp_arr = [[relay_box_local_position[1] + origo[1], relay_box_local_position[0] + origo[0]],
                [route_starting_point[1] + origo[1], route_starting_point[0] + origo[0]]]
    # print(temp_arr)
    distance_to_first_point = DistanceInMeters.calculate_distance(temp_arr[0], temp_arr[1])

    print("Flying straight with yaw=" + str(start_yaw) + " for " + str(distance_to_first_point) + " seconds")
    correct_yaw(start_yaw, distance_to_first_point)  # !!!!!!!!!!!!!!!!!!!! UNCOMMENT PLZ

    # Stop and hover at the first point
    the_thread("stop")
    '''
    To determine the angle between the y-axis and the first line,
    another made-up vector is being made, which goes straight north.
    Then a vector for the first line is being made afterwards.
    '''
    north_vector = [0, route_starting_point[1] + 1]
    first_line_vector = [path_limit_points[1][0] - path_limit_points[0][0],
                         path_limit_points[1][1] - path_limit_points[0][1]]
    # first_line_vector = [1, path_functions[0][0]]

    # Two unit vectors for the two vectors just created
    unit_vector_first_point_1 = north_vector / np.linalg.norm(north_vector)
    unit_vector_first_point_2 = first_line_vector / np.linalg.norm(first_line_vector)

    # Angle towards the second point
    angle_to_second_point = np.degrees(np.arccos(np.dot(unit_vector_first_point_1, unit_vector_first_point_2)))
    # print(path_limit_points[0][0])
    # print(path_limit_points[1][0])

    print("Second rotation to match path angle")
    print("unit_vector_first_point_1 ", unit_vector_first_point_1,
          "   unit_vector_first_point_2 ", unit_vector_first_point_2)
    print("angle to first point ", angle_to_first_point, "     angle to second point ", angle_to_second_point)

    # when the x-value at index=0 in the path_limit_points array is smaller than the x-value at index=1
    if path_limit_points[0][0] < path_limit_points[1][0]:
        # Rotate back the same amount as before plus the extra angle to align with the route
        if left == True:
            total_angle = angle_to_first_point + angle_to_second_point
            rotation_back_cw = "cw " + str(int(round(total_angle)))
            # print(rotation_back_cw)
            the_thread(rotation_back_cw)
        elif right == True:
            # back_to_north = - angle_to_first_point
            # total_angle = abs(-angle_to_first_point+angle_to_second_point)
            total_angle = angle_to_first_point - angle_to_second_point
            rotation_back_cw = "ccw " + str(int(round(total_angle)))
            # print(rotation_back_cw)
            the_thread(rotation_back_cw)
    else:
        # Rotate back the same amount as before plus the extra angle to align with the route
        if left == True:
            total_angle = angle_to_first_point - angle_to_second_point
            rotation_back_ccw = "cw " + str(int(round(total_angle)))
            # print(rotation_back_ccw)
            the_thread(rotation_back_ccw)
        elif right == True:
            total_angle = angle_to_first_point + angle_to_second_point
            rotation_back_ccw = "ccw " + str(int(round(total_angle)))
            # print(rotation_back_ccw)
            the_thread(rotation_back_ccw)
    time.sleep(1)
    the_thread("stop")
    time.sleep(2)
    # Now the drone should be ready to fly straight to the second point
    print("GET TO ROUTE FUNCTION DONE")


def search_route(path_width, path_limit_points, origo, path_functions):
    print("SEARCH ROUTE FUNCTION...")
    global drone_speed
    drone_yaw_1 = int(get_yaw())
    drone_yaw_2 = 0
    if drone_yaw_1 < 0:
        drone_yaw_2 = 180 + drone_yaw_1
    elif drone_yaw_1 > 0:
        drone_yaw_2 = drone_yaw_1 - 180
    else:
        drone_yaw_2 = 179

    print("drone_yaw_1: " + str(drone_yaw_1) + "  drone_yaw_2: " + str(drone_yaw_2))
    # print("yaaaaawww 1: ", drone_yaw_1, "yeehaaaw 2: ", drone_yaw_2)
    # print("yaw one way    ", drone_yaw_1)
    # print("yaw other way  ", drone_yaw_2)
    which_way = None  # true = left, false = right
    path_num = None
    for i in range(len(path_limit_points)):
        if i == 0:
            path_num = 1
        else:
            path_num = math.floor(i / 2) + 1

        print("path_num ", path_num)

        if (i % 2) == 0:  # when path_limit_point[i] is the point in the beginning of a straight flight
            # fly straight
            temp_arr = [[path_limit_points[i][1] + origo[1], path_limit_points[i][0] + origo[0]],
                        [path_limit_points[i + 1][1] + origo[1], path_limit_points[i + 1][0] + origo[0]]]
            # print(temp_arr)
            dist = DistanceInMeters.calculate_distance(temp_arr[0], temp_arr[1])

            # distance in meters divided by speed in meters per second = flight time in seconds
            flight_time = dist / drone_speed

            # correct_yaw(, flight_time)     # !!!!!!!!!!! uncomment this !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            if (path_num - 1) % 2:
                # print("straight ( yaw=" + str(drone_yaw_1) + ", flight_time=" + str(flight_time) + " )")
                print("Flying straight with yaw=" + str(drone_yaw_1) + " for "
                      + str(flight_time) + " seconds")
                correct_yaw(drone_yaw_2, flight_time)
            else:
                # print("straight ( yaw=" + str(drone_yaw_2) + ", flight_time=" + str(flight_time) + " )")
                print("Flying straight with yaw=" + str(drone_yaw_2) + " for "
                      + str(flight_time) + " seconds")
                correct_yaw(drone_yaw_1, flight_time)

            if not (i + 2) == len(
                    path_limit_points):  # if there is a point after the turn .... (i+2) because this only runs when i%2==0
                # figure out which way to turn next
                # print(math.floor(i / 2) + 1)
                if path_limit_points[i][0] < path_limit_points[i + 1][0]:  # if the x-value increases as the drone flies
                    # if the next path has a function with higher intersection value
                    if path_functions[math.floor(i / 2)][1] < path_functions[(math.floor(i / 2) + 1)][1]:
                        # print(str(path_functions[math.floor(i / 2)][1]) + " < " + str(path_functions[(math.floor(i / 2) + 1)][1]))
                        # print("Going on path number ", path_num, " turning left now")
                        # print("lefttt")
                        which_way = True
                    else:
                        # print("righttt")
                        which_way = False
                else:  # else if the x-value decreases as the drone flies
                    # if the next path has a function with lower intersection value
                    if path_functions[math.floor(i / 2)][1] < path_functions[(math.floor(i / 2) + 1)][1]:
                        # print("right")
                        which_way = False
                    else:
                        # print("left")
                        which_way = True
                # print(which_way)
            else:  # if there is no point after the turn then the drone should return home
                break

        else:  # when path_limit_point[i] is the point leading into a turn
            # the drone flies with 1 m/s which means that the value of semi_circle is the time it takes for the drone
            # to complete its turn
            semi_circle_dist = (path_width / 2) * math.pi

            # distance in meters divided by speed in meters per second = flight time in seconds
            flight_time = (semi_circle_dist / drone_speed)      # turns at half speed straight flying speed

            # 180 degrees divided by the time it takes to complete the 180-turn outputs the
            # yaw the drone should turn with each second ... the "yaw per second"
            degrees_pr_sec = int(round(180 / flight_time))

            if which_way:  # if which_way is set to true then turn left
                print("Turning left from path " + str(path_num) + " onto path " + str(path_num + 1)
                      + "... turning at " + str(degrees_pr_sec) + " deg/s for " + str(flight_time) + " seconds")
                search_turns(-degrees_pr_sec, flight_time)
            if not which_way:  # if which_way is set to false then turn right
                print("Turning right from path " + str(path_num) + " onto path " + str(path_num + 1)
                      + "... turning at " + str(degrees_pr_sec) + " deg/s for " + str(flight_time) + " seconds")
                search_turns(degrees_pr_sec, flight_time)
    print("SEARCH ROUTE FUNCTION DONE")
    the_thread("stop")
    time.sleep(2)


def go_home(path_limit_points, relay_box_global_pos, origo):
    relay_box_local_position = [relay_box_global_pos[1] - origo[0], relay_box_global_pos[0] - origo[1]]
    # A made up point north from the last path_limit_point (x,y)
    mupsi = [path_limit_points[-1][0], path_limit_points[-1][1]+1]

    # A vector from the last point to the relay box
    lprb = [relay_box_local_position[0]-path_limit_points[-1][0],
            relay_box_local_position[1]-path_limit_points[-1][1]]
    # A vector from the last point to the made up point north from the last point (mupsi)
    lpmupsi = [mupsi[0]-path_limit_points[-1][0],
               mupsi[1]-path_limit_points[-1][1]]
    # The angle between last point's north vector and relay_box
    unit_vector_last_1 = lpmupsi / np.linalg.norm(lpmupsi)
    unit_vector_last_2 = lprb / np.linalg.norm(lprb)
    angle_relay_to_last_point = np.degrees(np.arccos(np.dot(unit_vector_last_1, unit_vector_last_2)))
    print("Angle last point relay box: ", angle_relay_to_last_point)
    the_thread("rc 0 0 0 0")
    the_thread("stop")
    time.sleep(2)
    right = False
    left = False
    if path_limit_points[-1][0] > relay_box_local_position[0]:
        # Rotate clockwise
        new_angle = 360 - (180 + int(round(angle_relay_to_last_point)))
        rotation_ccw = "cw " + str(new_angle)
        print("cw ", new_angle)
        the_thread(rotation_ccw)

    elif path_limit_points[-1][0] < relay_box_local_position[0]:
        # Rotate counterclockwise
        new_angle = 360 - (180 + int(round(angle_relay_to_last_point)))
        print("ccw ", new_angle)
        rotation_cw = "ccw " + str(new_angle)
        the_thread(rotation_cw)

    time.sleep(2)
    # Now fly to the relay box
    start_yaw = get_yaw()
    distance_last_point_first_point = DistanceInMeters.calculate_distance(path_limit_points[-1], relay_box_global_pos)
    print("Flying straight with yaw=" + str(start_yaw) + " for " + str(distance_last_point_first_point) + " seconds")
    correct_yaw(start_yaw, distance_last_point_first_point)
    the_thread("stop")