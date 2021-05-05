import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from PIL import ImageTk, Image
import GUI_functionality


class App(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.__create_widgets()

    def __create_widgets(self):
        # Canvas
        self.img = ImageTk.PhotoImage(Image.open("map.png"))

        canvas = tk.Canvas(self, height=640, width=640)
        image_container = canvas.create_image(0, 0, anchor=tk.NW, image=self.img)
        canvas.grid(column=0, row=0, columnspan=5, rowspan=5)
        canvas.bind("<Button-1>", lambda x: GUI_functionality.limitPoint(x, canvas))

        tk.Button(self, text="Clear", command=lambda: GUI_functionality.clearCanvas(canvas, image_container)).grid(column=1, row=6)
        tk.Button(self, text="Delete last point", command=lambda: GUI_functionality.deleteLatestPoint(canvas)).grid(column=2, row=6)
        tk.Button(self, text="Estimate", command=lambda: GUI_functionality.estimate(canvas)).grid(column=3, row=6)
        tk.Button(self, text="NOT FREE", command=lambda: GUI_functionality.requestMap(canvas, image_container), bg="red").grid(column=1, row=7)
        tk.Button(self, text="+", command=lambda: GUI_functionality.update(canvas, image_container)).grid(column=2, row=7)
        tk.Button(self, text="-", command=lambda: GUI_functionality.zoomOut(canvas, image_container)).grid(column=3, row=7)
