import tkinter as tk
from tkinter import ttk

from GUI.GUI_route import App


class MainFrame(tk.Tk):
    def __init__(self):
        super().__init__()

        options = {"padx": 5, "pady": 5}

        # Configuration of window
        self.title("DroneHive")
        self.state("zoomed")

        self.__create_widgets()

    @property
    def client(self):
        return self.client

    @client.setter
    def client(self, client):
        self.client = client

    def __create_widgets(self):
        # Create input frame
        rando_frame = App(self)
        rando_frame.pack()


if __name__ == "__main__":
    app = MainFrame()
    app.mainloop()
