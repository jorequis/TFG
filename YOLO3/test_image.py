from io import BytesIO

import PIL.Image
import numpy as np
import requests
import cv2

from pydarknet import Detector, Image


def test_image():
    r = requests.get("https://raw.githubusercontent.com/madhawav/darknet/master/data/dog.jpg")
    assert r.status_code == 200
    img = PIL.Image.open(BytesIO(r.content))

    img = np.array(img)
    img = img[:,:,::-1] # RGB to BGR

    net = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"), bytes("weights/yolov3.weights", encoding="utf-8"), 0,
                   bytes("cfg/coco.data", encoding="utf-8"))

    img2 = Image(img)

    results = net.detect(img2)

    print("Results: " + str(results))
    for cat, score, bounds in results:
        print("Bounds: " + str(bounds))
        x, y, w, h = bounds
        img = cv2.rectangle(img, (int(x-w/2),int(y-h/2)),(int(x+w/2),int(y+h/2)),(255,0,0), 2)
        #cv2.putText(img, str(cat.decode("utf-8")), (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0))

    cv2.imshow("preview", img)

    while(True):
        k = cv2.waitKey(1)
        if k == 0xFF & ord("q"):
            break

    #results_labels = [x[0].decode("utf-8") for x in results]

    #assert "bicycle" in results_labels
    #assert "dog" in results_labels
    #assert "truck" in results_labels
    #assert len(results_labels) == 3

test_image()