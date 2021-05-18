import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from PIL import ImageTk, Image
from math import sqrt, degrees, acos
import mapHandler
import SearchArea
import ObjectHandler


class Canvas:
    def __init__(self, root):
        self.img = ImageTk.PhotoImage(Image.open("map.png"))
        self.canvas = tk.Canvas(root, height=620, width=620)
        self.image_container = self.canvas.create_image(300, 300, image=self.img)
        self.canvas.grid(column=0, row=0, columnspan=5, rowspan=5)
        self.canvas.bind("<Button-1>", self.limitPoint)
        self.PointDenominator = ["A", "B", "C", "D"]
        
    def limitPoint(self, event):
        """Adds a point to the map, which limits the search area"""
        if len(ObjectHandler.Points) >= 4:
            showinfo("Error", "Can't have more than 4 points")
        else:
            ObjectHandler.Points.append(SearchArea.LimitPoint(self.PointDenominator[len(ObjectHandler.Points)], (event.x - 8), (event.x + 8), (event.y - 8),
                                                (event.y + 8)))
            ObjectHandler.Points[len(ObjectHandler.Points) - 1].drawPoint(self.canvas)
            print(str(mapHandler.Map.CalculateCoordinates(event.x, event.y)))

    def update(self):
        self.img = ImageTk.PhotoImage(file="map.png")
        self.canvas.itemconfig(self.image_container)
        self.clearCanvas()

    def clearCanvas(self):
        self.canvas.delete("all")
        self.canvas.create_image(300, 300, image=self.img)
        ObjectHandler.Points.clear()

    def deleteLatestPoint(self):
        if len(ObjectHandler.Points) < 1:
            showinfo("Error", "No points to delete")
        else:
            self.canvas.delete(ObjectHandler.Points[-1].Point)
            self.canvas.delete(ObjectHandler.Points[-1].text)
            del ObjectHandler.Points[-1]

    def AngleChecker(self):
        """
        Using Law of Cosines to calculate angles in triangel ABC and CDA
        anc checking that theese angles are not >= 180
        """
        threshold = 160

        AB = sqrt((ObjectHandler.Points[1].trueX - ObjectHandler.Points[0].trueX) ** 2 + (ObjectHandler.Points[1].trueY - ObjectHandler.Points[0].trueY) ** 2)
        BC = sqrt((ObjectHandler.Points[2].trueX - ObjectHandler.Points[1].trueX) ** 2 + (ObjectHandler.Points[2].trueY - ObjectHandler.Points[1].trueY) ** 2)
        CD = sqrt((ObjectHandler.Points[3].trueX - ObjectHandler.Points[2].trueX) ** 2 + (ObjectHandler.Points[3].trueY - ObjectHandler.Points[2].trueY) ** 2)
        DA = sqrt((ObjectHandler.Points[0].trueX - ObjectHandler.Points[3].trueX) ** 2 + (ObjectHandler.Points[0].trueY - ObjectHandler.Points[3].trueY) ** 2)

        # Diagonals
        AC = sqrt((ObjectHandler.Points[0].trueX - ObjectHandler.Points[2].trueX) ** 2 + (ObjectHandler.Points[0].trueY - ObjectHandler.Points[2].trueY) ** 2)
        BD = sqrt((ObjectHandler.Points[1].trueX - ObjectHandler.Points[3].trueX) ** 2 + (ObjectHandler.Points[1].trueY - ObjectHandler.Points[3].trueY) ** 2)

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
            self.deleteLatestPoint()
            showinfo("Error", "Sorry, one or more angles are greater than " + str(threshold) +  " degrees")
        else:
            return True

    def estimate(self):
        """Draws an estimated search area on the GUI"""
        if len(ObjectHandler.Points) == 4:
            if self.AngleChecker():
                for c in range(-1, 3):
                    self.canvas.create_line(ObjectHandler.Points[c].trueX, ObjectHandler.Points[c].trueY, ObjectHandler.Points[c + 1].trueX, ObjectHandler.Points[c + 1].trueY, width=2)
                
        else:
            showinfo("Error", "Please make sure you have entered 4 points before estimation.")
