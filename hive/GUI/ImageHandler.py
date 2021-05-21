import tkinter as tk
from math import acos, degrees, sqrt
from tkinter import ttk
from tkinter.messagebox import showinfo

from PIL import Image, ImageTk

from .ObjectHandler import *
from .SearchArea import LimitPoint



class Canvas:
    def __init__(self, root):
        self.img = ImageTk.PhotoImage(Image.open("hive/GUI/map.png"))
        self.canvas = tk.Canvas(root, height=620, width=620)
        self.image_container = self.canvas.create_image(
            300, 300, image=self.img
        )
        self.canvas.grid(column=0, row=0, columnspan=5, rowspan=5)
        self.canvas.bind("<Button-1>", self.limitPoint)
        self.PointDenominator = ["A", "B", "C", "D"]

        self.info = tk.Label(root, text="Hello World")
        self.info.grid(column=0, row=6, columnspan=5)
        self.UpdateInfo()

    def limitPoint(self, event):
        """Adds a point to the map, which limits the search area"""
        if len(Points) >= 4:
            showinfo("Error", "Can't have more than 4 points")
        else:
            Points.append(
                LimitPoint(
                    self.PointDenominator[len(Points)],
                    (event.x - 8),
                    (event.x + 8),
                    (event.y - 8),
                    (event.y + 8),
                )
            )
            Points[len(Points) - 1].drawPoint(self.canvas)
            print(str(Map[0].CalculateCoordinates(event.x, event.y)))

    def update(self):
        self.img = ImageTk.PhotoImage(file="hive\GUI\map.png")
        self.canvas.itemconfig(self.image_container)
        self.clearCanvas()

    def clearCanvas(self):
        self.canvas.delete("all")
        self.canvas.create_image(300, 300, image=self.img)
        Points.clear()

    def deleteLatestPoint(self):
        if len(Points) < 1:
            showinfo("Error", "No points to delete")
        else:
            self.canvas.delete(Points[-1].Point)
            self.canvas.delete(Points[-1].text)
            del Points[-1]

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

        if AC < BD:
            angleA = degrees(
                acos((AB ** 2 + AC ** 2 - BC ** 2) / (2 * AB * AC))
            ) + degrees(acos((DA ** 2 + AC ** 2 - CD ** 2) / (2 * DA * AC)))
            angleB = degrees(
                acos((AB ** 2 + BC ** 2 - AC ** 2) / (2 * AB * BC))
            )
            angleC = degrees(
                acos((BC ** 2 + AC ** 2 - AB ** 2) / (2 * BC * AC))
            ) + degrees(acos((CD ** 2 + AC ** 2 - DA ** 2) / (2 * CD * AC)))
            angleD = degrees(
                acos((DA ** 2 + CD ** 2 - AC ** 2) / (2 * DA * CD))
            )

        else:
            angleA = degrees(
                acos((AB ** 2 + DA ** 2 - BD ** 2) / (2 * AB * DA))
            )
            angleB = degrees(
                acos((AB ** 2 + BD ** 2 - DA ** 2) / (2 * AB * BD))
            ) + degrees(acos((BC ** 2 + BD ** 2 - CD ** 2) / (2 * BC * BD)))
            angleC = degrees(
                acos((BC ** 2 + CD ** 2 - BD ** 2) / (2 * BC * CD))
            )
            angleD = degrees(
                acos((DA ** 2 + BD ** 2 - AB ** 2) / (2 * DA * BD))
            ) + degrees(acos((CD ** 2 + BD ** 2 - BC ** 2) / (2 * CD * BD)))

        if (
            angleA >= threshold
            or angleB >= threshold
            or angleC >= threshold
            or angleD >= threshold
        ):
            self.deleteLatestPoint()
            showinfo(
                "Error",
                "Sorry, one or more angles are greater than "
                + str(threshold)
                + " degrees",
            )
        else:
            return True

    def estimate(self):
        """Draws an estimated search area on the GUI"""
        if len(Points) == 4:
            if self.AngleChecker():
                for c in range(-1, 3):
                    self.canvas.create_line(
                        Points[c].trueX,
                        Points[c].trueY,
                        Points[c + 1].trueX,
                        Points[c + 1].trueY,
                        width=2,
                    )
        else:
            showinfo(
                "Error",
                "Please make sure you have entered 4 points before estimation.",
            )

    def UpdateInfo(self):
        self.info["text"] = "Afstand fra kant til kant: " + str(Map[0].calcScale()) + " m"
