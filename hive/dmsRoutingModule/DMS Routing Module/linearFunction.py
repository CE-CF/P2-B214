import numpy as num

''' This class can calculate the slope between two local coordinates
    and find the intersection between this slope and the local y-axis '''


class LinearFunction:
    first_point = num.array([])
    second_point = num.array([])
    ''' These two arrays include the coordinates for 
        the two points which linear function will be 
        found using the methods in this class '''

    # Constructor
    def __init__(self, first_p, second_p):
        self.first_point = first_p
        self.second_point = second_p

    ''' Calculates the difference between the two 
        points' latitude and longitude coordinates '''
    def calculate_difference(self):
        return num.array([self.first_point[0] - self.second_point[0],
                          self.first_point[1] - self.second_point[1]])

    # This method calculates the slope between two points
    def calculate_slope(self):
        self.calculate_difference()
        
        return (self.calculate_difference()[0] /
                self.calculate_difference()[1])

    # This method calculates the intersection between the slope and the local y-axis
    def calculate_intersection(self):
        return (self.first_point[0]
                - (self.calculate_slope() * self.first_point[1]))

    ''' The intersection formula:
        b = y1 - a * x1 '''

    ''' Vi skal lave nogle metoder til at finde arealet af firkanten, så vi 
    kan dele det op til n antal droner'''


