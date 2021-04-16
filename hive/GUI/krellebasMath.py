from math import acos, sqrt, radians, degrees
import SearchArea

x = [0 for x in range(3)]
y = [0 for x in range(3)]
Points = [[0 for x in range(2)] for y in range(3)]
Points[0][0] = 0.0
Points[0][1] = 4.0
Points[1][0] = 1.0
Points[1][1] = 6.0
Points[2][0] = 3.0
Points[2][1] = 5.0



def Point_Line_Distance(*coordinates):
    if (len(coordinates)==3):
        for i in range(len(coordinates)):
            for j in range(2):
                if (j==0):
                    x[i] = Points[coordinates[i]][j]
                else:
                    y[i] = Points[coordinates[i]][j]
        printString = 'x0: {0}, y0: {1} | x1: {2}, y1: {3} | x2: {4}, y2: {5}'.format(x[0],y[0],x[1],y[1],x[2],y[2])
        print(printString)
        a = (y[1]-y[0])/(x[1]-x[0])
        b = y[0]-(a*x[0])
        LigningString = 'Equation of line between ({0},{1}) and ({2},{3}): y = {4}x + {5}'.format(x[0],y[0],x[1],y[1],a,b)
        print(LigningString)
        d = ((a*x[2])+((-1)*y[2])+b)/sqrt(a**2+(-1)**2)
        distance = 'Distance to line from ({0},{1}): {2}'.format(x[2],y[2],d) # testet på https://www.mathportal.org/calculators/analytic-geometry/line-point-distance.php
        return print(distance)
    if (len(coordinates)<3):
        print("not enough points added for calculation")
    if (len(coordinates)>3):
        print("too many points added for calculation")
    
    

Point_Line_Distance(0, 1, 2)











