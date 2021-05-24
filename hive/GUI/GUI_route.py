import tkinter as tk
from tkinter import ttk
from GUI.ImageHandler import Canvas
from GUI.ObjectHandler import *



class App(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.__create_widgets()

    def __create_widgets(self):
        # Canvas
        canvas = Canvas(self)
        canvas.update()

        # Map Prefrences
        tk.Button(self, text="+", command=lambda: SearchArea.ZoomIn(canvas)).grid(
            column=6, row=0
        )

        tk.Button(self, text="-", command=lambda: SearchArea.ZoomOut(canvas)).grid(
            column=6, row=1
        )

        tk.Button(self, text="Maptype", command=lambda: SearchArea.setMapType(canvas)).grid(
            column=6, row=2
        )

        tk.Button(self, text='Inputtype', command=lambda: canvas.ChangePointType()).grid(
            column=6, row=3
        )

        # Canvas Operators
        tk.Button(self, text="Clear", command=lambda: canvas.clearCanvas()).grid(
            column=1, row=12
        )

        tk.Button(self, text="Delete last point", command=lambda: canvas.deleteLatestPoint()).grid(
            column=2, row=12
        )

        tk.Button(self, text="Estimate", command=lambda: canvas.estimate()).grid(
            column=3, row=12
        )
