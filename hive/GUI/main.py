import tkinter as tk
from tkinter.messagebox import showinfo
from PIL import ImageTk, Image
from math import acos, sqrt, radians, degrees
import SearchArea


# Object Lists
Points = []
PointDenominator = ["A", "B", "C", "D"]


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
        for c in range(-1, 3):
            canvas.create_line(Points[c].trueX, Points[c].trueY, Points[c + 1].trueX, Points[c + 1].trueY, width=2)
        AngleChecker()
    else:
        showinfo("Error", "Please make sure you have entered 4 points before estimation.")


def AngleChecker():
    """
    Using Law of Cosines to calculate angles in triangel ABC and CDA
    anc checking that theese angles are not >= 180
    """
    AB = sqrt((Points[1].trueX - Points[0].trueX) ** 2 + (Points[1].trueY - Points[0].trueY) ** 2)
    BC = sqrt((Points[2].trueX - Points[1].trueX) ** 2 + (Points[2].trueY - Points[1].trueY) ** 2)
    AC = sqrt((Points[0].trueX - Points[2].trueX) ** 2 + (Points[0].trueY - Points[2].trueY) ** 2)
    CD = sqrt((Points[3].trueX - Points[2].trueX) ** 2 + (Points[3].trueY - Points[2].trueY) ** 2)
    DA = sqrt((Points[0].trueX - Points[3].trueX) ** 2 + (Points[0].trueY - Points[3].trueY) ** 2)

    angleA = degrees(acos((AB ** 2 + AC ** 2 - BC ** 2) / (2 * AB * AC))) + degrees(
        acos((DA ** 2 + AC ** 2 - CD ** 2) / (2 * DA * AC)))
    angleB = degrees(acos((AB ** 2 + BC ** 2 - AC ** 2) / (2 * AB * BC)))
    angleC = degrees(acos((BC ** 2 + AC ** 2 - AB ** 2) / (2 * BC * AC))) + degrees(
        acos((CD ** 2 + AC ** 2 - DA ** 2) / (2 * CD * AC)))
    angleD = degrees(acos((DA ** 2 + CD ** 2 - AC ** 2) / (2 * DA * AC)))

    if angleA >= 180 or angleB >= 180 or angleC >= 180 or angleD >= 180:
        showinfo("Error", "Sorry, one or more angles are greater than 180 degrees")


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


root = tk.Tk()

img = ImageTk.PhotoImage(Image.open("map.png"))

canvas = tk.Canvas(root, height=400, width=400)
canvas.create_image(400, 400, image=img)
canvas.pack()
canvas.bind("<Button-1>", limitPoint)

tk.Button(root, text="Clear", command=clearCanvas).pack()
tk.Button(root, text="Delete last point", command=deleteLatestPoint).pack()
tk.Button(root, text="Estimate", command=estimate).pack()

root.mainloop()
