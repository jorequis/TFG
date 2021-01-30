
import cv2
import time
import argparse
from collections import namedtuple

def execute(video, pfile):

    # Get video stream
    cap = cv2.VideoCapture(video)

    input_file = open(pfile, "r")
    lines = input_file.read().splitlines()

    Square = namedtuple("Square", "x y w")
    smooths = []

    for line in lines:
        split = line.split(" ")
        smooth = Square(float(split[0]), float(split[1]), float(split[2]))
        smooths.append(smooth)

    i = 10
    w = round(smooths[i].w)
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('p3_output.avi', fourcc, fps, (w, w))

    # While we have the video opened so we can get a new frame
    while(cap.isOpened()):

        # Read next frame. If it fails 'success' will be false
        success, image = cap.read()
        
        x = round(smooths[i].x)
        y = round(smooths[i].y)
        
        out.write(image[y:y+w, x:x+w])
        
        cv2.rectangle(image, (x,y), (x+w,y+w), (0,255,0), 2)

        x = round(smooths[i+1].x)
        y = round(smooths[i+1].y)
        
        cv2.rectangle(image, (x,y), (x+w,y+w), (255,0,0), 2)

        #time.sleep(0.1)
        
        # Show the image with the rectangles
        cv2.imshow('frame', image)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

        i += 2

    # Release the video file
    cap.release()
    out.release()
    # Close the window where the image is shown
    cv2.destroyAllWindows()