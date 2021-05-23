class LimitPoint:
    trueX = 0
    trueY = 0
    text = None
    long = None
    lat = None

    def __init__(self, denominator, x1, x2, y1, y2):
        self.denonimator = denominator
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.Point = None
        self.setTruePoint()

    def drawPoint(self, canvas, color ="#e74c3c"):
        self.Point = canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill=color)
        self.text = canvas.create_text(self.trueX, self.trueY, text=self.denonimator)

    def setTruePoint(self):
        self.trueX = self.x2 - 8
        self.trueY = self.y2 - 8

    def setLongLat(self, lat, long):
        self.lat = lat
        self.long = long