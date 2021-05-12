from .dronecommands import instantiate, the_thread, correct_yaw, search_turns
from dmsRoutingModule.routingpackage.distanceinmeters import DistanceInMeters
import math
# from ..routingpackage.findroutefunctions import run
import numpy as np


def get_to_route(path_limit_points, origo, relay_box_global_pos, path_functions):
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
    rbfp = [route_starting_point[0]-relay_box_local_position[0],
            route_starting_point[1]-relay_box_local_position[1]]
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
    angle_to_first_point = np.degrees(np.arccos(np.dot(unit_vector_1, unit_vector_2)))
    '''
    Is the drone supposed to turn right or left?
    If the x-coordinate for the relay-box is greater  than that of the first point
    the drone will have to rotate left. If it is the opposite, the drone
    will rotate to the right.
    '''
    right = False
    left = False
    if relay_box_local_position[0] > route_starting_point[0]:
        # Rotate counterclockwise
        rotation_ccw = "ccw " + str(int(round(angle_to_first_point)))
        left = True
        the_thread(rotation_ccw)

    elif relay_box_local_position[0] < route_starting_point[0]:
        # Rotate clockwise
        rotation_cw = "cw " + str(int(round(angle_to_first_point)))
        right = True
        the_thread(rotation_cw)

    else:
        # Fly straight up
        pass

    '''
    Now the drone should be in the right direction to just fly straight to
    the first point using the correct_yaw function.
    '''
    temp_arr = [[relay_box_local_position[1] + origo[1], relay_box_local_position[0] + origo[0]],
                [route_starting_point[1] + origo[1], route_starting_point[0] + origo[0]]]
    # print(temp_arr)
    distance_to_first_point = DistanceInMeters.calculate_distance(temp_arr[0], temp_arr[1])
    # print(distance_to_first_point)
    # the_thread(correct_yaw(distance_to_first_point)) !!!!!!!!!!!!!!!!!!!! UNCOMMENT PLZ

    # Stop and hover at the first point
    the_thread("stop")
    '''
    To determine the angle between the y-axis and the first line,
    another made-up vector is being made, which goes straight north.
    Then a vector for the first line is being made afterwards.
    '''
    north_vector = [0, route_starting_point[1] + 1]
    first_line_vector = [1, path_functions[0][0]]

    # Two unit vectors for the two vectors just created
    unit_vector_first_point_1 = north_vector / np.linalg.norm(north_vector)
    unit_vector_first_point_2 = first_line_vector / np.linalg.norm(first_line_vector)

    # Angle towards the second point
    angle_to_second_point = np.degrees(np.arccos(np.dot(unit_vector_first_point_1, unit_vector_first_point_2)))

    if path_limit_points[0][0] < path_limit_points[1][0]:
        # Rotate back the same amount as before plus the extra angle to align with the route
        if left == True:
            total_angle = angle_to_first_point + angle_to_second_point
            rotation_back_cw = "cw " + str(int(round(total_angle)))
            the_thread(rotation_back_cw)
        elif right == True:
            total_angle = angle_to_first_point - angle_to_second_point
            rotation_back_cw = "cw " + str(int(round(total_angle)))
            the_thread(rotation_back_cw)
    else:
        # Rotate back the same amount as before plus the extra angle to align with the route
        if left == True:
            total_angle = angle_to_first_point - angle_to_second_point
            rotation_back_ccw = "ccw " + str(int(round(total_angle)))
            the_thread(rotation_back_ccw)
        elif right == True:
            total_angle = angle_to_first_point + angle_to_second_point
            rotation_back_ccw = "ccw " + str(int(round(total_angle)))
            the_thread(rotation_back_ccw)

# Now the drone should be ready to fly straight to the second point


def search_route(path_width, path_limit_points, origo, path_functions):
    which_way = None  # true = left, false = right
    for i in range(len(path_limit_points)):

        if (i % 2) == 0:  # when path_limit_point[i] is the point in the beginning of a straight flight
            # fly straight
            temp_arr = [[path_limit_points[i][1] + origo[1], path_limit_points[i][0] + origo[0]],
                        [path_limit_points[i + 1][1] + origo[1], path_limit_points[i + 1][0] + origo[0]]]
            print(temp_arr)
            dist = DistanceInMeters.calculate_distance(temp_arr[0], temp_arr[1])

            # dist = DistanceInMeters.calculate_distance(path_limit_points[i], path_limit_points[i + 1])
            # correct_yaw(dist)     # !!!!!!!!!!! uncomment this !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            if path_functions[(math.floor(i / 2) + 1)][1]:      # if there is a point after the turn
                # figure out which way to turn next
                if path_limit_points[i] < path_limit_points[i + 1]:  # if the x-value increases as the drone flies
                    # if the next path has a function with lower intersection value
                    if path_functions[math.floor(i / 2)][1] < path_functions[(math.floor(i / 2) + 1)][1]:
                        which_way = False
                    else:
                        which_way = True
                else:  # else if the x-value decreases as the drone flies
                    # if the next path has a function with lower intersection value
                    if path_functions[math.floor(i / 2)][1] < path_functions[(math.floor(i / 2) + 1)][1]:
                        which_way = True
                    else:
                        which_way = False
            else:                       # if there is no point after the turn then the drone should return home
                break

        else:  # when path_limit_point[i] is the point leading into a turn

            # the drone flies with 1 m/s which means that the value of semi_circle is the time it takes for the drone
            # to complete its turn
            semi_circle = (path_width / 2) * math.pi

            degrees_pr_sec = str(int(round(180 / semi_circle)))

            if which_way:  # if which_way is set to true then turn left
                search_turns("rc 0 100 0 -" + degrees_pr_sec, semi_circle)
            if not which_way:  # if which_way is set to false then turn right
                search_turns("rc 0 100 0 " + degrees_pr_sec, semi_circle)

    # if (index % 2) == 0:              # if we
    #   # find distance between x path_limit_point[i] and path_limit_point[i+1] in meters
    #   # (the drone flies at 1 m/s so...:)
    #   # fly straight for x seconds with correct_yaw()
    #
    #   # if path_limit_points[i] < path_limit_points[i+1]:
    #   #   # if path_functions[floor(i/2)][1] < path_functions[floor(i/2) + 1][1]:
    #   #   #   # which_way = false
    #   #   # else:
    #   #   #   # which_way = true
    #   # else:
    #   #   # if path_functions[floor(i/2)][1] < path_functions[floor(i/2) + 1][1]:
    #   #   #   # which_way = true
    #   #   # else:
    #   #   #   # which_way = false
    # else:
    #   # if which_way:                   # if which_way is set to true then turn left
    #   #   # turn left
    #   if not which_way:                   # if which_way is set to false then turn right
    #   #   # turn right


def go_home():
    pass
