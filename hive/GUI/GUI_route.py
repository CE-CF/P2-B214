import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

from PIL import Image, ImageTk

from .ImageHandler import Canvas
from .mapHandler import Map
from .ObjectHandler import *


class App(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.__create_widgets()

    def __create_widgets(self):
        # Canvas
        canvas = Canvas(self)
        canvas.update()

        # Map Prefrences
        tk.Button(self, text="+", command=lambda: Map[0].ZoomIn(canvas)).grid(
            column=6, row=0
        )
        tk.Button(self, text="-", command=lambda: Map[0].ZoomOut(canvas)).grid(
            column=6, row=1
        )
        tk.Button(
            self,
            text="Maptype",
            command=lambda: Map[0].setMapType(canvas),
        ).grid(column=6, row=2)

        # Canvas Operators
        tk.Button(
            self, text="Clear", command=lambda: canvas.clearCanvas()
        ).grid(column=1, row=12)
        tk.Button(
            self,
            text="Delete last point",
            command=lambda: canvas.deleteLatestPoint(),
        ).grid(column=2, row=12)
        tk.Button(
            self, text="Estimate", command=lambda: canvas.estimate()
        ).grid(column=3, row=12)

