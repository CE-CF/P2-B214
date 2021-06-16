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

    def __init__(self, address, ID):
        #self.Old_Frame_Time = 0
        #self.New_Frame_Time = 1
        self.ID = ID
        self.FPS = 0
        self.FrameCount = 0
        # Open placeholder image and encode it into a numpy bit array
        f = open('hive/GUI_Camera_Module/NoFrame.jpg', 'rb')
        image_bytes = f.read()
        self.PlaceholderFrame = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), -1)
        f.close()
        # Open the video capture object and try grabbing the frame forever. This action is blocking
        print(f"\tBackgroundFrameRead started: {self.ID}")
        self.cap = cv2.VideoCapture(address)
        if not self.cap.isOpened():
            self.cap.open(address)
        self.grabbed, self.frame = self.cap.read()
        while not self.grabbed or self.frame is None:
            self.grabbed, self.frame = self.cap.read()
        print(f"\tFrame finally grabbed: {self.ID}")
        # The frame is grabbed and blocking stopped. Create the frame and FPS updating threads and start them.
        self.stopped = False
        self.worker = Thread(target=self.update_frame, args=(), daemon=True)
        self.worker.start()
        #self.FPSThread = Thread(target=self.Update_FPS_Tests, args=(), daemon=True)
        #self.FPSThread.start()
        self.FPSThread = Thread(target=self.Update_FPS, args=(), daemon=True)
        self.FPSThread.start()

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
                        #self.New_Frame_Time = time.time()
                        #self.FPS = 1/(self.New_Frame_Time-self.Old_Frame_Time)
                        #self.Old_Frame_Time = self.New_Frame_Time
                        self.FrameCount += 1
                    else:
                        print(f'Grabbed status is: {self.grabbed}')
                        #self.Old_Frame_Time = time.time()
                except ZeroDivisionError:
                    print("Division by zero error when finding video feed fps")
                    self.FPS = 0
                    self.Old_Frame_Time = time.time()


    def Update_FPS(self):
        # Each second it updates the FPS of the feed using the amount of grabbed frames in that second
        while not self.stopped:
            time.sleep(1)
            self.FPS = self.FrameCount
            self.FrameCount = 0

    def Update_FPS_Tests(self):
        # Function used when testing the FPS of the video feed. Writes the FPS values in a csv file.
        with open(f"fps{self.ID}.csv", "a") as f:
            Seconds = 0
            f.write("\nNew Data Set:\n")
            while not self.stopped:
                time.sleep(1)
                Seconds += 1
                #print(f'BGR updating frame')
                self.FPS = self.FrameCount
                self.FrameCount = 0
                f.write(f"{Seconds},{self.FPS}\n")

    def stop(self):
        """Stop the frame update worker
        Internal method, you normally wouldn't call this yourself.
        """
        self.stopped = True
        self.worker.join()
        self.FrameThread.join()
