import cv2
import time
import numpy as np
from threading import Thread



"""
This class has been edited so that it works with the video sorter
It captures video from the local port corresponding to the drone's ID
"""
class BackgroundFrameRead:
    """
    This class read frames from a VideoCapture in background. Use
    backgroundFrameRead.frame to get the current frame.
    """

    def __init__(self, address):
        self.Old_Frame_Time = 0
        self.New_Frame_Time = 1
        self.FPS = 1
        f = open('hive/GUI_Camera_Module/NoFrame.jpg', 'rb')
        image_bytes = f.read()
        self.PlaceholderFrame = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), -1)
        print("BackgroundFrameRead started")
        self.cap = cv2.VideoCapture(address)
        if not self.cap.isOpened():
            self.cap.open(address)
        self.grabbed, self.frame = self.cap.read()
        while not self.grabbed or self.frame is None:
            self.grabbed, self.frame = self.cap.read()
        print("Frame finally grabbed")
        self.stopped = False
        self.worker = Thread(target=self.update_frame, args=(), daemon=True)
        self.worker.start()

    def update_frame(self):
        """Thread worker function to retrieve frames from a VideoCapture
        Internal method, you normally wouldn't call this yourself.
        """
        while not self.stopped:
            if not self.grabbed or not self.cap.isOpened():
                self.stop()
            else:
                self.grabbed, self.frame = self.cap.read()
                try:
                    if self.grabbed:
                        self.New_Frame_Time = time.time()
                        self.FPS = 1/(self.New_Frame_Time-self.Old_Frame_Time)
                        self.Old_Frame_Time = self.New_Frame_Time
                    else:
                        print(f'Grabbed status is: {self.grabbed}')
                        self.Old_Frame_Time = time.time()
                except ZeroDivisionError:
                    print("Division by zero error when finding video feed fps")
                    self.FPS = 0
                    self.Old_Frame_Time = time.time()


    def stop(self):
        """Stop the frame update worker
        Internal method, you normally wouldn't call this yourself.
        """
        self.stopped = True
        self.worker.join()
