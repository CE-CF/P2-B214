import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from PIL import ImageTk, Image
import ImageHandler
import mapHandler
import ObjectHandler

class App(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.__create_widgets()

    def __create_widgets(self):
        # Canvas
        canvas = ImageHandler.Canvas(self)
        canvas.update()


        tk.Button(self, text="Clear", command=lambda: canvas.clearCanvas()).grid(column=1, row=6)
        tk.Button(self, text="Delete last point", command=lambda: canvas.deleteLatestPoint()).grid(column=2, row=6)
        tk.Button(self, text="Estimate", command=lambda: canvas.estimate()).grid(column=3, row=6)
        tk.Button(self, text="NOT FREE", command=lambda: Map[0].requestMap(), bg="red").grid(column=1, row=7)
        tk.Button(self, text="+", command=lambda: Map[0].ZoomIn(canvas)).grid(column=2, row=7)
        tk.Button(self, text="-", command=lambda: Map[0].ZoomOut(canvas)).grid(column=3, row=7)
        