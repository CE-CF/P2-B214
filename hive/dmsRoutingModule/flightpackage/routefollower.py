from .dronecommands import instantiate, the_thread, correct_yaw
from routingpackage.distanceinmeters import DistanceInMeters
import numpy as np


angle_from_north = 0

def get_to_next_point(waypoint_bool, waypoint_arr):
    global angle_from_north
    
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
            angle_sum = (int(round(angle_to_next_point)) * (-1)) + angle_from_north
            print("angle sum   " + str(angle_sum))
            rotation_ccw = "ccw " + str(int(round(angle_to_next_point)))
            left = True
            the_thread(rotation_ccw)

        elif x1 < x2:
            # Rotate clockwise
            angle_sum = int(round(angle_to_next_point)) + angle_from_north
            print("angle sum   " + str(angle_sum))
            rotation_cw = "cw " + str(int(round(angle_to_next_point)))
            right = True
            the_thread(rotation_cw)

        # Now the drone should point towards the next point
        distance_to_next_point = DistanceInMeters.calculate_distance(waypoint_arr[i], waypoint_arr[i + 1])

        # correct_yaw(distance_to_next_point) !!!!!!!!!!!!!!!!!!!!!!UNCOMMENT!!!!!!!!!!!!!!!!!!!!!!!!

        # Stop and hover
        the_thread("stop")

        # Turn again to face north
        if left:
            angle_from_north = int(round(angle_to_next_point))
            rotate_back_cw = "cw " + str(int(round(angle_to_next_point)))
            the_thread(rotate_back_cw)
        elif right:
            angle_from_north = int(round(angle_to_next_point)) * (-1)
            rotate_back_ccw = "ccw " + str(int(round(angle_to_next_point)))
            the_thread(rotate_back_ccw)

    # Now it should point straight north again

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

    right = False
    left = False
    if waypoint_arr[-1][1] > waypoint_arr[0][1]:
        # Rotate counterclockwise
        rotation_ccw = "ccw " + str(int(round(angle_first_point_last_point)))
        left = True
        the_thread(rotation_ccw)

    elif waypoint_arr[-1][1] < waypoint_arr[0][1]:
        # Rotate clockwise
        rotation_cw = "cw " + str(int(round(angle_first_point_last_point)))
        right = True
        the_thread(rotation_cw)

    # Now fly to the first point
    distance_last_point_first_point = DistanceInMeters.calculate_distance(waypoint_arr[-1], waypoint_arr[0])
    # correct_yaw(distance_last_point_first_point) !!!!!!!!!!!11 UNCOMMETN!!!!!!!!!!
    the_thread("stop")