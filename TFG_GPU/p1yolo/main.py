
#Imports necesarios
import cv2
import numpy as np
import cython as cy
import time
from pydarknet import Detector, Image

def draw_prediction(img, label, confidence, x, y, x_plus_w, y_plus_h, color):

    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)

    cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

def print_prediction(label, x, y, w, h, output):

    output.write(label + " " + str(x) + " " + str(y) + " " + str(w) + " " + str(h) + "\n")

def execute(video, config, weights, coco):

    output_file = "p1_output.txt"
    output = open(output_file, "w")

    cap = cv2.VideoCapture(video)

    if(not cap.isOpened()):
        print("Video file not found")
        return None

    prev_x = 0
    prev_y = 0
    prev_w = 0
    prev_h = 0

    #Get the dimensions of the image, can optimize because video has constant dimensions
    Width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    Height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    output.write(str(Width) + " " + str(Height) + "\n")

    average_time = 0

    print(weights);    

    net = Detector(bytes(config, encoding="utf-8"), bytes(weights, encoding="utf-8"), 0, bytes(coco, encoding="utf-8"))

    start_time = time.time()

    while (cap.isOpened()):
        success, frame = cap.read()

        if frame is None:
            break

        if success == False:
            break
            
        dark_frame = Image(frame)
        results = net.detect(dark_frame)
        del dark_frame

        found_person = False

        for cat, score, bounds in results:
            #if(score > 5):
            #print("Score: " + str(score) + ", Cat: " + str(cat.decode("utf-8")))
            #print("---------")
            if(str(cat.decode("utf-8")) == "person"):
                found_person = True
                
                x, y, w, h = bounds
                x = x - w/2
                y = y - h/2

                prev_x = x
                prev_y = y
                prev_w = w
                prev_h = h

                print_prediction("person", x, y, w, h, output)
                frame = cv2.rectangle(frame, (int(x),int(y)),(int(x+w),int(y+h)),(255,0,0), 2)
                frame = cv2.putText(frame, "person", (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0))

                #break
        
        if found_person == False:
            print_prediction("lost", prev_x, prev_y, prev_w, prev_h, output)
            frame = cv2.rectangle(frame, (int(prev_x),int(prev_y)),(int(prev_x+prev_w),int(prev_y+prev_h)),(0,0,255), 2)
            frame = cv2.putText(frame, "lost", (int(prev_x), int(prev_y)), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255))
        
        cv2.imshow("preview", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break


    end_time = time.time()
    print("Process Time: " + str(end_time - start_time))

    cv2.destroyAllWindows()
    output.close()

    return output_file