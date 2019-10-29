import cv2
import numpy as np # Color map
import pyautogui # Used to automatically click with the mouse
import PIL.ImageGrab # get RGB colors
import PySimpleGUI as psg # HSV slider

# Variables
red = 47
green = 93
blue = 66
color = [red, green, blue]
minRange_color = color[2], color[1], color[0]
maxRange_color = color[2] - color[2] + 255, color[1] - color[1] + 255, color[0] - color[2] + 255

# values below are used for the GUI to change the HSV
position = 'horizontal'

slider = [
    [psg.Text('Hue')],
    [psg.Slider(range=(0, 255), default_value=0, size=(21, 10), orientation='{}'.format(position), key='-H-',
                enable_events=True)],
    [psg.Text('Saturation')],
    [psg.Slider(range=(0, 255), default_value=0, size=(21, 10), orientation='{}'.format(position), key='-S-',
                enable_events=True)],
    [psg.Text('Value')],
    [psg.Slider(range=(0, 255), default_value=0, size=(21, 10), orientation='{}'.format(position), key='-V-',
                enable_events=True)]
]

drawSlider = [
    [psg.Text('Min Range')],
    [psg.Slider(range=(0, 500), default_value=100, size=(21, 10), orientation='{}'.format(position), key='-Min-',
                enable_events=True)],
    [psg.Text('Max Range')],
    [psg.Slider(range=(500, 2000), default_value=500, size=(21, 10), orientation='{}'.format(position), key='-Max-',
                enable_events=True)]
]

HSV_slider = psg.Window('Minimum Range HSV', slider)
Draw_slider = psg.Window('Drawing Range', drawSlider)


# Functions
#-----------------------------------------
def colorPick(colorR, colorG, colorB):
    return np.array([colorR, colorG, colorB])

def getPixelBGR():
    return PIL.ImageGrab.grab().load()[pyautogui.position()]
#-----------------------------------------

print(getPixelBGR())

# Selects the video Source
cap = cv2.VideoCapture(1)

while True:
    # Grab the values from the sliders
    event, value = HSV_slider.read(timeout=1)
    eventD, valueD = Draw_slider.read(timeout=1)

    # Start capturing the frames from the video source
    extra, frames = cap.read()

    colorMap = cv2.cvtColor(frames, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(colorMap, colorPick(minRange_color[0], minRange_color[1], minRange_color[2]), colorPick(maxRange_color[0], maxRange_color[1], maxRange_color[2]))

    ret, thresh = cv2.threshold(colorMap, 127, 255, 0) # part 2
    contours, extra = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

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
        if drawArea > valueD['-Min-'] and drawArea < valueD['-Max-']:
            cv2.drawContours(frames, contour, -1, (0, 255, 0), 1)
            cv2.circle(frames, (momentumX, momentumY), 2, (0, 255, 0), -1)
            cv2.line(frames, (pyautogui.position()), (momentumX, momentumY), (0, 255, 0), 1, 1)
            print(pyautogui.position())
            #print(momentumX , momentumY)

            # part 3
            '''
            if cv2.waitKey(1) == 97: # a button
                print(momentumX, momentumY)
                pyautogui.click(momentumX, momentumY)
            '''

    cv2.imshow("Video", frames)
    cv2.imshow("mask", mask)

    # Update HSV based on the slider position & changes occur in real time
    color[0] = int(value['-H-'])
    color[1] = int(value['-S-'])
    color[2] = int(value['-V-'])
    minRange_color = color[0], color[1], color[2]

    # Stop the video capturing loop
    if cv2.waitKey(1) == 27: # ESC button
        break
    '''
    elif keyboard.is_pressed('alt'):
        tempColor = getPixelBGR()
        tempColor = colorsys.rgb_to_hsv(tempColor[0], tempColor[1], tempColor[2])
        color[0] = int(round(tempColor[0]))
        color[1] = int(round(tempColor[1]))
        color[2] = int(round(tempColor[2]))
        print(color[0], color[1], color[2])

        minRange_color = color[0], color[1], color[2]
    '''



# Eradicate the script and close the script
cap.release()
cv2.destroyAllWindows()