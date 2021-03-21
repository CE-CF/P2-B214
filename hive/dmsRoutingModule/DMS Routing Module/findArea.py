import numpy as num


'''
The four global coordinates are in order from A - D.
To find the area, made from the four coordinates, a diagonal needs to be determined.
The diagonal is easy to find, when the order of the coordinates is known.
It will either go from A-C or B-D, in every single case.
So if the diagonal is A-C, the length is determined by sqrt(AB^2 * BC^2)
'''


class findArea:
    # The four different lengths in the quadrilateral
    AB = 0
    BC = 0
    CD = 0
    DA = 0
    numberDrones = 0

    def __init__(self, lenAB, lenBC, lenCD, lenDA):
        self.AB = lenAB
        self.BC = lenBC
        self.CD = lenCD
        self.DA = lenDA

    ''' Here the diagonal is being 
    calculated from A to C in the quadrilateral ABCD.'''
    def calculate_diagonal(self):
        return num.sqrt(self.AB ^ 2 * self.BC ^ 2)

    '''Using Heron's formula to calculate the area of ABCD, 
    the quadrilateral have to be separated into two triangles.
    Then the area of each triangle will be calculated and the two areas 
    will be added together to have the area of the whole quadrilateral.
    Here the first triangle is made of the points A, B and C.'''
    def area_of_quadrilateral(self):
        # s = the triangle's half circumference
        sABC = 1/2 * (self.AB + self.BC + self.calculate_diagonal())
        areaABC = num.sqrt(s * (s - self.AB) * (s - self.BC) * (s - self.calculate_diagonal()))

        '''The second triangle is made of A, C and D'''
        sACB = 1 / 2 * (self.calculate_diagonal() + self.CD + self.DA)
        areaACD = num.sqrt(s * (s - self.calculate_diagonal()) * (s - self.CD) * (s - self.DA))

        return areaABC + areaACD









