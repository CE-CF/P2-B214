import tkinter as tk
from tkinter.messagebox import showinfo
from PIL import ImageTk, Image
from math import acos, sqrt, radians, degrees
import SearchArea
import mapHandler

# Object Lists
Points = []
PointDenominator = ["A", "B", "C", "D"]
Map = []


def limitPoint(event):
    """Adds a point to the map, which limits the search area"""
    if len(Points) >= 4:
        showinfo("Error", "Can't have more than 4 points")
    else:
        Points.append(SearchArea.LimitPoint(PointDenominator[len(Points)], (event.x - 8), (event.x + 8), (event.y - 8),
                                            (event.y + 8)))
        Points[len(Points) - 1].drawPoint(canvas)


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
    anc checking that theese angles are not >= 180
    """
    treshold = 160

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

    if angleA >= treshold or angleB >= treshold or angleC >= treshold or angleD >= treshold:
        deleteLatestPoint()
        showinfo("Error", "Sorry, one or more angles are greater than " + str(treshold) +  " degrees")
    else:
        return True


def clearCanvas():
    canvas.delete("all")
    canvas.create_image(400, 400, image=img)
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


def requestMap():
    Map.append(mapHandler.Map())
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



root = tk.Tk()
root.state("zoomed")

img = ImageTk.PhotoImage(Image.open("map.png"))

canvas = tk.Canvas(root, height=640, width=640)
image_container = canvas.create_image(640, 640, image=img)
canvas.pack(side="top", anchor="nw")
canvas.bind("<Button-1>", limitPoint)


tk.Button(root, text="Clear", command=clearCanvas).pack(side="left", anchor="nw")
tk.Button(root, text="Delete last point", command=deleteLatestPoint).pack(side="left", anchor="nw")
tk.Button(root, text="Estimate", command=estimate).pack(side="left", anchor="nw")
tk.Button(root, text="NOT FREE", command=requestMap, bg="red").pack(side="left", anchor="nw")
tk.Button(root, text="+", command=zoomIn).pack(side="left", anchor="nw")
tk.Button(root, text="-", command=zoomOut).pack(side="left", anchor="nw")

root.mainloop()
