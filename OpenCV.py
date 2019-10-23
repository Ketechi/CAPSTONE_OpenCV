import cv2
import numpy as np
import imutils

# Variables
red = 47
green = 93
blue = 66
color = red, green, blue
minRange_color = color[0] - 30, color[1] - 30, color[2] - 30
maxRange_color = color[0] + 30, color[1] + 30, color[2] + 30

# Functions
#-----------------------------------------
def colorPick(colorR, colorG, colorB):
    return np.array([colorR, colorG, colorB])

#-----------------------------------------

# Selects the video Source
cap = cv2.VideoCapture(1)

while True:
    # Start capturing the frames from the video source
    extra, frames = cap.read()

    colorMap = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
    # mask = cv2.inRange(colorMap, colorPick(minRange_color[0], minRange_color[1], minRange_color[2]), colorPick(maxRange_color[0], maxRange_color[1], maxRange_color[2]))
    ret, thresh = cv2.threshold(colorMap, 127, 255, 0)
    contours, extra = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # Capture each contour and the center of contours
    # contours = imutils.grab_contours(contours)

    #cv2.drawContours(frames, contourMask(mask), -1, (0,255,0), 2)

    for contour in contours:
        # Math for center of contours
        momentum = cv2.moments(contour)
        momentumX = int(momentum['m10'] / (momentum['m00'] + 0.01))
        momentumY = int(momentum['m01'] / (momentum['m00'] + 0.01))

        # Draw the center and the contour
        drawArea = cv2.contourArea(contour)
        if drawArea > 500 and drawArea < 3000:
            cv2.drawContours(frames, contour, -1, (0, 255, 0), 1)
            cv2.circle(frames, (momentumX, momentumY), 1, (0, 255, 0), -1)

    cv2.imshow("Video", frames)

    # Stop the video capturing loop
    if cv2.waitKey(1) == 27:
        break
    elif cv2.waitKey(1) == 122: # Run a color picker
        colorPick()


# Eradicate the script and close the script
cap.release()
cv2.destroyAllWindows()