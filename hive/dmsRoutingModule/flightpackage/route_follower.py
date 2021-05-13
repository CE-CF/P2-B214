from .dronecommands import instantiate, the_thread, correct_yaw
from dmsRoutingModule.routingpackage.distanceinmeters import DistanceInMeters
import numpy as np


def get_to_next_point(waypoint_bool, current_point, next_point, number_of_total_points):
    if not waypoint_bool:
        return 0
    i = 0
    while i <= number_of_total_points:
        x1 = current_point[1]
        y1 = current_point[0]
        x2 = next_point[1]
        y2 = next_point[0]

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
            rotation_ccw = "ccw " + str(int(round(angle_to_next_point)))
            left = True
            the_thread(rotation_ccw)

        elif x1 < x2:
            # Rotate clockwise
            rotation_cw = "cw " + str(int(round(angle_to_next_point)))
            right = True
            the_thread(rotation_cw)

        # Now the drone should point towards the next point
        distance_to_next_point = DistanceInMeters.calculate_distance(current_point, next_point)

        # the_thread(correct_yaw(distance_to_next_point)) !!!!!!!!!!!!!!!!!!!!!!UNCOMMENT!!!!!!!!!!!!!!!!!!!!!!!!

        # Stop and hover
        the_thread("stop")