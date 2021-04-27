import mapHandler
import SearchArea
from math import acos, sqrt, degrees, cos, pi


# Object Lists
Points = []
PointDenominator = ["A", "B", "C", "D"]
Map = []


def getCornerPoints(x,y):
    pixel_degree_x = 360 / 2**(Map[0].zoom + 8)
    pixel_degree_y = 360 / 2**(Map[0].zoom + 8) * cos(Map[0].lat * pi / 180)
    point_lat = Map[0].lat - pixel_degree_y * (y - Map[0].size / 2)
    point_long = Map[0].long + pixel_degree_x * (x - Map[0].size / 2)

    return point_lat, point_long

def limitPoint(event):
    """Adds a point to the map, which limits the search area"""
    if len(Points) >= 4:
        showinfo("Error", "Can't have more than 4 points")
    else:
        Points.append(SearchArea.LimitPoint(PointDenominator[len(Points)], (event.x - 8), (event.x + 8), (event.y - 8),
                                            (event.y + 8)))
        Points[len(Points) - 1].drawPoint(canvas)
        print(str(getCornerPoints(event.x, event.y)))


def estimate():
    """Draws an estimated search area on the GUI"""
    if len(Points) == 4:
        if AngleChecker():
            for c in range(-1, 3):
                canvas.create_line(Points[c].trueX, Points[c].trueY, Points[c + 1].trueX, Points[c + 1].trueY, width=2)
    else:
        showinfo("Error", "Please make sure you have entered 4 points before estimation.")


def AngleChecker():
    """
    Using Law of Cosines to calculate angles in triangel ABC and CDA
    and checking that theese angles are not >= treshold
    """
    threshold = 160

    AB = sqrt((Points[1].trueX - Points[0].trueX) ** 2 + (Points[1].trueY - Points[0].trueY) ** 2)
    BC = sqrt((Points[2].trueX - Points[1].trueX) ** 2 + (Points[2].trueY - Points[1].trueY) ** 2)
    CD = sqrt((Points[3].trueX - Points[2].trueX) ** 2 + (Points[3].trueY - Points[2].trueY) ** 2)
    DA = sqrt((Points[0].trueX - Points[3].trueX) ** 2 + (Points[0].trueY - Points[3].trueY) ** 2)

    # Diagonals
    AC = sqrt((Points[0].trueX - Points[2].trueX) ** 2 + (Points[0].trueY - Points[2].trueY) ** 2)
    BD = sqrt((Points[1].trueX - Points[3].trueX) ** 2 + (Points[1].trueY - Points[3].trueY) ** 2)

    if AC < BD:
        angleA = degrees(acos((AB ** 2 + AC ** 2 - BC ** 2) / (2 * AB * AC))) + degrees(
            acos((DA ** 2 + AC ** 2 - CD ** 2) / (2 * DA * AC)))
        angleB = degrees(acos((AB ** 2 + BC ** 2 - AC ** 2) / (2 * AB * BC)))
        angleC = degrees(acos((BC ** 2 + AC ** 2 - AB ** 2) / (2 * BC * AC))) + degrees(
            acos((CD ** 2 + AC ** 2 - DA ** 2) / (2 * CD * AC)))
        angleD = degrees(acos((DA ** 2 + CD ** 2 - AC ** 2) / (2 * DA * CD)))

    else:
        angleA = degrees(acos((AB ** 2 + DA ** 2 - BD ** 2) / (2 * AB * DA)))
        angleB = degrees(acos((AB ** 2 + BD ** 2 - DA ** 2) / (2 * AB * BD))) + degrees(
            acos((BC ** 2 + BD ** 2 - CD ** 2) / (2 * BC * BD)))
        angleC = degrees(acos((BC ** 2 + CD ** 2 - BD ** 2) / (2 * BC * CD)))
        angleD = degrees(acos((DA ** 2 + BD ** 2 - AB ** 2) / (2 * DA * BD))) + degrees(
            acos((CD ** 2 + BD ** 2 - BC ** 2) / (2 * CD * BD)))

    if angleA >= threshold or angleB >= threshold or angleC >= threshold or angleD >= threshold:
        deleteLatestPoint()
        showinfo("Error", "Sorry, one or more angles are greater than " + str(threshold) +  " degrees")
    else:
        return True


def clearCanvas():
    canvas.delete("all")
    canvas.create_image(300, 300, image=img)
    Points.clear()


def deleteLatestPoint():
    if len(Points) < 1:
        showinfo("Error", "No points to delete")
    else:
        canvas.delete(Points[-1].Point)
        canvas.delete(Points[-1].text)
        del Points[-1]


def update():
    global img
    img = ImageTk.PhotoImage(file="map.png")
    canvas.itemconfig(image_container)
    clearCanvas()

    # print("CE: " + str(Map[0].lat) + ", " + str(Map[0].long))
    # print("NE: " + str(getCornerPoints(Map[0].size, 0)))
    # print("SW: " + str(getCornerPoints(0, Map[0].size)))
    # print("NW: " + str(getCornerPoints(0, 0)))
    # print("SE: " + str(getCornerPoints(Map[0].size, Map[0].size)))s


def requestMap():
    if len(Map) == 0:
        Map.append(mapHandler.Map())
    if lat.get() != "Lattitude" and long.get() != "Longtitude":
        try:
            Map[0].setCoordinates(float(lat.get()), float(long.get()))
        except ValueError:
            print("Error")
    if zoomValue.get != "zoom":
        Map[0].zoom = int(zoomValue.get())

    Map[0].requestMap()
    update()



def zoomIn():
    if len(Map) == 0:
        Map.append(mapHandler.Map())
        Map[0].requestMap()
        update()
    else:
        Map[0].zoom += 1
        Map[0].requestMap()
        update()

def zoomOut():
    if len(Map) == 0:
        Map.append(mapHandler.Map())
        Map[0].requestMap()
        update()
    else:
        Map[0].zoom -= 1
        Map[0].requestMap()
        update()