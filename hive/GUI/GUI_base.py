import tkinter as tk
from .GUI_route import App


class MainFrame(tk.Tk):
    def __init__(self):
        """Initialize root window"""
        super().__init__()

        # Configuration of window
        self.title("DroneHive")
        self.state("zoomed")

        self.__create_widgets()

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, client):
        self._client = client

    def __create_widgets(self):
        # Create input frame
        GUI_Route = App(self)
        GUI_Route.pack()


if __name__ == "__main__":
    app = MainFrame()
    app.mainloop()
