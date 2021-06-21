from .dronecommands import instantiate, the_thread, correct_yaw
from routingpackage.distanceinmeters import DistanceInMeters
import numpy as np

angle_from_north = 0
cmd_string = ""


def run_the_route(waypoint_bool, waypoint_arr):
    global angle_from_north, cmd_string
    cmd_string = cmd_string + "init;"
    if not waypoint_bool:
        return 0
    i = 0
    while i < len(waypoint_arr):
        if (i + 1) == len(waypoint_arr):
            break
        x1 = waypoint_arr[i][1]
        y1 = waypoint_arr[i][0]
        x2 = waypoint_arr[i + 1][1]
        y2 = waypoint_arr[i + 1][0]

        # A point north from the current point is being created (mup)
        mup = [x1, y1 + 1]

        # A vector from current point to mup (cpmup)
        cpmup = [mup[0] - x1, mup[1] - y1]

        # A vector from current point to next point (cpnp)
        cpnp = [x2 - x1, y2 - y1]

        # A unit vector for both vectors
        unit_vector_1 = cpmup / np.linalg.norm(cpmup)
        unit_vector_2 = cpnp / np.linalg.norm(cpnp)
        angle_to_next_point = np.degrees(np.arccos(np.dot(unit_vector_1, unit_vector_2)))

        # Is the angle left or right?
        right = False
        left = False
        if x1 > x2:
            # Rotate counterclockwise
            angle_sum = abs((int(round(angle_to_next_point)) * (-1)) + angle_from_north)
            left = True
            cmd_string = cmd_string + "rotate:-" + str(angle_sum) + ";"

        elif x1 < x2:
            # Rotate clockwise
            angle_sum = abs(int(round(angle_to_next_point)) + angle_from_north)
            right = True
            cmd_string = cmd_string + "rotate:" + str(angle_sum) + ";"

        cmd_string = cmd_string + "wait:2;"
        # Now the drone should point towards the next point
        distance_to_next_point = DistanceInMeters.calculate_distance(waypoint_arr[i], waypoint_arr[i + 1])
        cmd_string = cmd_string + "getyaw;"
        cmd_string = cmd_string + "straight:yaw:" + str(distance_to_next_point) + ";"

        # Stop and hover
        # the_thread("stop")
        cmd_string = cmd_string + "stop;"

        # Update the angle_from_north variable
        if left:
            angle_from_north = int(round(angle_to_next_point))
            rotate_back_cw = "cw " + str(int(round(angle_to_next_point)))

        elif right:
            angle_from_north = int(round(angle_to_next_point)) * (-1)
            rotate_back_ccw = "ccw " + str(int(round(angle_to_next_point)))

        i = i + 1

    # Now it should go back home from the last point to the first point
    # A point north from the last point
    mup_2 = [waypoint_arr[-1][1], waypoint_arr[-1][0] + 1]

    # A vector from last point to the made up point
    lpmup = [mup_2[0] - waypoint_arr[-1][1], mup_2[1] - waypoint_arr[-1][0]]

    # A vector from last point to first point
    lpfp = [waypoint_arr[0][1] - waypoint_arr[-1][1], waypoint_arr[0][0] - waypoint_arr[-1][0]]

    unit_vector_last_1 = lpmup / np.linalg.norm(lpmup)
    unit_vector_last_2 = lpfp / np.linalg.norm(lpfp)
    angle_first_point_last_point = np.degrees(np.arccos(np.dot(unit_vector_last_1, unit_vector_last_2)))

    if waypoint_arr[-1][1] > waypoint_arr[0][1]:
        # Rotate clockwise
        newer_angle = abs(360 - (angle_from_north + int(round(angle_first_point_last_point))))
        # print("Newer angle", newer_angle)
        # new_angle = abs(360 - (180 + int(round(angle_first_point_last_point))))
        rotation_cw = "cw:" + str(newer_angle)
        # the_thread(rotation_cw)
        cmd_string = cmd_string + "rotate:" + str(newer_angle) + ";"

    elif waypoint_arr[-1][1] < waypoint_arr[0][1]:
        # Rotate counterclockwise
        newer_angle = abs(360 - (angle_from_north + int(round(angle_first_point_last_point))))
        # new_angle = abs(360 - (180 + int(round(angle_first_point_last_point))))
        # print("Newer angle ccw", newer_angle)
        rotation_ccw = "ccw:" + str(newer_angle)
        # the_thread(rotation_ccw)
        cmd_string = cmd_string + "rotate:-" + str(newer_angle) + ";"

    cmd_string = cmd_string + "wait:2;"
    # Now fly to the first point
    distance_last_point_first_point = DistanceInMeters.calculate_distance(waypoint_arr[-1], waypoint_arr[0])
    cmd_string = cmd_string + "getyaw;"
    cmd_string = cmd_string + "straight:yaw:" + str(distance_last_point_first_point) + ";"

    cmd_string = cmd_string + "stop;"
    cmd_string = cmd_string + "land;"
    print(cmd_string)
    return cmd_string
