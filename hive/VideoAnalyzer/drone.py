import cv2
import numpy as np

# Video Input
VideoCapture = cv2.VideoCapture(0)

# Cascades
faceCascade = cv2.CascadeClassifier("Resource/haarcascade_frontalface_default.xml") # For frontface detection
bodyCascade = cv2.CascadeClassifier("Resource/haarcascade_fullbody.xml") # For fullbody detection

# Color detection values
fColor = [
    [168, 78, 161, 179, 255, 255], # Red
    #[0, 160, 150, 179, 255, 255], # Yellow
    [13, 185, 150, 179, 255, 255], # New Yellow
    #[93, 71, 0, 179, 255, 255], # Blue
    #[90, 134, 0, 179, 255, 255], # New Blue
    [93, 134, 0, 179, 255, 255], # Test Blue
]

# Ignore color if in woods
iColor = [
    []
]


def findFace(img):
    """Face detection via haarcascade"""

    # convert frame to grayscale
    grayConversion = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(grayConversion, 2, 6)

    # Draw rectangle around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(output, (x, y), (x+w, y+h), (0, 0, 0), 2) # Draw on image
        cv2.putText(output, 'Face', (x,y), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2) # Write on image

    cv2.putText(output, 'Number of Faces: ' + str(len(faces)), (20, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

def findBody(img):
    """Fullbody detection via haarcascade"""

    # convert frame to grayscale
    grayConversion = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    bodies = bodyCascade.detectMultiScale(grayConversion, 1.1, 4)

    # Draw rectangle around detected bodies
    for (x, y, w, h) in bodies:
        cv2.rectangle(output, (x, y), (x+w, y+h), (255, 255, 255), 2) # Draw on image
        cv2.putText(output, 'Body', (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2) # Write on image



def findColor(img, fColor):
    """Searches for colors from fColor"""
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    for color in fColor:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        getContours(mask)
        cv2.imshow("Mask", mask)

def getContours(img):
    """Finds contours for detected colors"""
    contours,hiearchy  = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 800:
            cv2.drawContours(output, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x, y, w, h = cv2.boundingRect(approx)

while True: # Searches each frame for faces, bodies and colors
    ret, frame = VideoCapture.read()
    output = frame
    findColor(frame, fColor)
    findFace(frame)
    findBody(frame)
    cv2.imshow("Original", output)
    cv2.waitKey(1)
