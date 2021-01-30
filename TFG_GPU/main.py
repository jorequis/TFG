
import p1yolo
import p2cropsmooth
import p3video

#yolo.py -i ..\clase.mp4 -c yolov3.cfg -w yolov3.weights -cl yolov3.txt

#import os

video = "./video4k.mp4"
config = "./p1yolo/cfg/yolov3-tiny.cfg"
weights = "./p1yolo/weights/yolov3-tiny.weights"
coco = "./p1yolo/cfg/coco.data"

p1_file = p1yolo.execute(video, config, weights, coco)
#p1_file = "p1_output.txt"

p2_file = p2cropsmooth.execute(p1_file, 350)
#p2_file = "p2_output.txt"

p3video.execute(video, p2_file)

#p1_file = os.popen("./p1_yolo/yolo.py" + " -v " + video + " -c " + config + " -w " + weights + " -cl " + names).read()
#p1_file = "p1_output.txt"
#p2_file = os.popen("./p2_crop_smooth/crop_smooth.py" + " -f " + p1_file).read()
#p3_file = os.popen("./p3_video/video.py" + " -v " + video + " -f " + p2_file).read()