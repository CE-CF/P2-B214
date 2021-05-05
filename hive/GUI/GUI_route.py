import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from PIL import ImageTk, Image
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
        canvas = tk.Canvas(self, height=640, width=640)
        canvas.grid(column=0, row=0)
        img = ImageTk.PhotoImage(Image.open("map.png"))
        canvas.create_image(300, 300, image=img)

        canvas.bind("<Button-1>", lambda x: GUI_functionality.limitPoint(x,canvas))


        tk.Button(self, text="Clear", command= lambda : GUI_functionality.clearCanvas(canvas)).grid(column=1, row=7)
        tk.Button(self, text="Delete last point", command= lambda : GUI_functionality.deleteLatestPoint(canvas)).grid(column=2, row=7)
        tk.Button(self, text="Estimate", command= lambda : GUI_functionality.estimate(canvas)).grid(column=3, row=7)
        tk.Button(self, text="NOT FREE", command= lambda : GUI_functionality.requestMap(canvas), bg="red").grid(column=1, row=9)
        tk.Button(self, text="+", command= lambda : GUI_functionality.zoomIn(canvas)).grid(column=2, row=9)
        tk.Button(self, text="-", command= lambda : GUI_functionality.zoomOut(canvas)).grid(column=3, row=9)
