import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from PIL import ImageTk, Image
from math import acos, sqrt, degrees, cos, pi
import mapHandler
import SearchArea
import GUI_functionality



class App(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        # Layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=3)

        self.__create_widgets()

    def __create_widgets(self):
        # Canvas
        img = ImageTk.PhotoImage(Image.open("map.png"))

        canvas = tk.Canvas(self, height=640, width=640)
        image_container = canvas.create_image(300, 300, image=img)
        canvas.grid(column=0, row=0, sticky=tk.W)
        canvas.bind("<Button-1>", limitPoint)

        tk.Button(self, text="Clear", command=clearCanvas).grid(column=0, row=1)
        tk.Button(self, text="Delete last point", command=deleteLatestPoint).grid(column=0, row=2)
        tk.Button(self, text="Estimate", command=estimate).grid(column=0, row=3)
        tk.Button(self, text="NOT FREE", command=requestMap, bg="red").grid(column=1, row=1)
        tk.Button(self, text="+", command=zoomIn).grid(column=1, row=2)
        tk.Button(self, text="-", command=zoomOut).grid(column=1, row=3)