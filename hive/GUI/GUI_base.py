import tkinter as tk
#from .GUI_route import App
#from tkinter import ttk
from .ImageHandler import Canvas
from .ObjectHandler import *

class MainFrame(tk.Tk):
    def __init__(self):
        """Initialize root window"""
        super().__init__()

        # Configuration of window
        self.title("DroneHive")
        self.state("zoomed") # Maximized window

        self.__create_widgets()

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, client):
        self._client = client

    @staticmethod
    def punkt(lat, long):
        Kort[0].setCoordinates(float(lat), float(long))


    def __create_widgets(self):
        # Create input frame
        # GUI_Route = App(self)
        # GUI_Route.pack()

        canvas = Canvas(self)
        canvas.update()

        tk.Button(self, text="LSOS", command=lambda: canvas.GetCoor(self.client)).grid(
            column=8, row=0
        )
        # Map Prefrences
        tk.Button(self, text="+", command=lambda: Kort[0].ZoomIn(canvas)).grid(
            column=6, row=0
        )

        tk.Button(self, text="-", command=lambda: Kort[0].ZoomOut(canvas)).grid(
            column=6, row=1
        )

        tk.Button(self, text="Maptype", command=lambda: Kort[0].setMapType(canvas)).grid(
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

        tk.Button(self, text="Estimate", command=lambda: canvas.estimate(self.client)).grid(
            column=3, row=12
        )



if __name__ == "__main__":
    app = MainFrame()
    app.mainloop()
