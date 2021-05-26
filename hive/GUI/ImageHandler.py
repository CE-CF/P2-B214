# Library Imports
import time
import tkinter as tk
from math import acos, degrees, sqrt
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk

# Imports from files
from .ObjectHandler import *
from .SearchArea import LimitPoint

class Canvas:
    PointType = "boundary"
    dPointType = 1
    Counter = 0

    def __init__(self, root):
        Kort[0].requestMap()
        self.img = ImageTk.PhotoImage(Image.open("map.png"))
        self.canvas = tk.Canvas(root, height=620, width=620)
        self.image_container = self.canvas.create_image(0, 0, image=self.img)
        self.canvas.grid(column=0, row=0, columnspan=5, rowspan=5)
        self.canvas.bind("<Button-1>", self.addPoint)

        # Scale Label
        self.info = tk.Label(root, text="")
        self.info.grid(column=0, row=11, columnspan=5)
        self.UpdateInfo()

        # PointType Label
        self.gui_pointtype = tk.Label(root, text=str(self.PointType))
        self.gui_pointtype.grid(column=7, row=3)

    def addPoint(self, event):
        """Adds a point to the map"""
        if self.PointType == "boundary":
            if len(Points) >= 4:
                showinfo("Error", "Can't have more than 4 points")
                return 0

        Points.append(
            LimitPoint(
                self.NameSetter(),
                (event.x - 8),
                (event.x + 8),
                (event.y - 8),
                (event.y + 8),
            )
        )

        if self.PointType == "waypoint" and len(Points) == 1:
            Points[-1].drawPoint(self.canvas, "#3fc405")
        else:
            Points[-1].drawPoint(self.canvas)

        lat, long = Kort[0].CalculateCoordinates(event.x, event.y)
        Points[len(Points) - 1].setLongLat(lat, long)

    def update(self):
        self.img = ImageTk.PhotoImage(file="map.png")
        self.clearCanvas()

    def clearCanvas(self):
        self.canvas.delete("all")
        self.canvas.create_image(300, 300, image=self.img)
        Points.clear()
        self.Counter = 0

    def deleteLatestPoint(self):
        if len(Points) != 0:
            self.canvas.delete(Points[-1].Point)
            self.canvas.delete(Points[-1].text)
            del Points[-1]
            self.Counter -= 1
        else:
            showinfo("Error", "No points to delete")

    def AngleChecker(self):
        """
        Using Law of Cosines to calculate angles in triangel ABC and CDA
        anc checking that theese angles are not >= 180
        """
        threshold = 160

        AB = sqrt(
            (Points[1].trueX - Points[0].trueX) ** 2
            + (Points[1].trueY - Points[0].trueY) ** 2
        )
        BC = sqrt(
            (Points[2].trueX - Points[1].trueX) ** 2
            + (Points[2].trueY - Points[1].trueY) ** 2
        )
        CD = sqrt(
            (Points[3].trueX - Points[2].trueX) ** 2
            + (Points[3].trueY - Points[2].trueY) ** 2
        )
        DA = sqrt(
            (Points[0].trueX - Points[3].trueX) ** 2
            + (Points[0].trueY - Points[3].trueY) ** 2
        )

        # Diagonals
        AC = sqrt(
            (Points[0].trueX - Points[2].trueX) ** 2
            + (Points[0].trueY - Points[2].trueY) ** 2
        )
        BD = sqrt(
            (Points[1].trueX - Points[3].trueX) ** 2
            + (Points[1].trueY - Points[3].trueY) ** 2
        )

        ACangleA = degrees(
            acos((AB ** 2 + AC ** 2 - BC ** 2) / (2 * AB * AC))
        ) + degrees(acos((DA ** 2 + AC ** 2 - CD ** 2) / (2 * DA * AC)))

        ACangleB = degrees(
            acos((AB ** 2 + BC ** 2 - AC ** 2) / (2 * AB * BC))
        )

        ACangleC = degrees(
            acos((BC ** 2 + AC ** 2 - AB ** 2) / (2 * BC * AC))
        ) + degrees(acos((CD ** 2 + AC ** 2 - DA ** 2) / (2 * CD * AC)))

        ACangleD = degrees(
            acos((DA ** 2 + CD ** 2 - AC ** 2) / (2 * DA * CD))
        )

        BDangleA = degrees(
            acos((AB ** 2 + DA ** 2 - BD ** 2) / (2 * AB * DA))
        )

        BDangleB = degrees(
            acos((AB ** 2 + BD ** 2 - DA ** 2) / (2 * AB * BD))
        ) + degrees(acos((BC ** 2 + BD ** 2 - CD ** 2) / (2 * BC * BD)))

        BDangleC = degrees(
            acos((BC ** 2 + CD ** 2 - BD ** 2) / (2 * BC * CD))
        )

        BDangleD = degrees(
            acos((DA ** 2 + BD ** 2 - AB ** 2) / (2 * DA * BD))
        ) + degrees(acos((CD ** 2 + BD ** 2 - BC ** 2) / (2 * CD * BD)))

        AngleList = [ACangleA, ACangleB, ACangleC, ACangleD, BDangleA, BDangleB, BDangleC, BDangleD]

        for angle in AngleList:
            if angle > threshold:
                self.deleteLatestPoint()
                showinfo(
                    "Error",
                    "Sorry, one or more angles are greater than "
                    + str(threshold)
                    + " degrees",
                )
                return False

        return True

    def estimate(self, client):
        """Draws an estimated search area on the GUI and send coordinates"""
        if self.PointType == "boundary":
            if len(Points) == 4:
                if self.AngleChecker():
                    pass
                else:
                    return 0
            else:
                showinfo("Error", "Please make sure you have entered 4 points before estimation.")
                return 0

        for c in range(-1, len(Points) - 1):
            if c == -1 and self.PointType == "waypoint":
                self.canvas.create_line(
                    Points[c].trueX,
                    Points[c].trueY,
                    Points[c + 1].trueX,
                    Points[c + 1].trueY,
                    width=2,
                    dash=(5, 4)
                )
            else:
                self.canvas.create_line(
                    Points[c].trueX,
                    Points[c].trueY,
                    Points[c + 1].trueX,
                    Points[c + 1].trueY,
                    width=2,
                )
        self.SendRoute(client)

    def UpdateInfo(self):
        self.info["text"] = "Afstand fra kant til kant: " + str(Kort[0].calcScale()) + " m"

    def ChangePointType(self):
        if self.PointType == "boundary":
            self.PointType = "waypoint"
            self.dPointType = 0
        else:
            self.PointType = "boundary"
            self.dPointType = 1

        self.gui_pointtype["text"] = self.PointType
        self.clearCanvas()

    def NameSetter(self):
        Denominator = "{:01d}".format(self.Counter)
        self.Counter += 1
        return Denominator

    def SendRoute(self, client):
        RouteList = ""
        for point in Points:
            RouteList += "{}:{};".format(round(point.lat, 6), round(point.long, 6))
        client.send_message(self.dPointType, client.srv_ip, RouteList)

    def GetCoor(self, client):
        client.send_message(3, client.srv_ip, "CMD:GET_LOC;")



