
#Imports necesarios
import math
import argparse
from collections import namedtuple
from . import kalman as KLMN

Row = namedtuple("Row", "x y w h")
Square = namedtuple("Square", "x y w")

VectorSmooth = namedtuple("VectorSmooth", "x y xv yv")

def find_max(rows):
    max = 0
    for row in rows:
        if row.w > max: max = row.w
        #if row.h > max: max = row.h
    return max

def find_min(rows):
    min = rows[0].w
    for row in rows:
        if row.w < min: min = row.w
        #if row.h < min: min = row.h
    return min

def calculate_squares(rows, squares, w):
    #w = 250 #find_min()
    for row in rows:
        x = ((row.x + row.x + row.w) / 2.0) - w / 2.0
        y = row.y - w / 4 #(row.y + row.y + row.h) / 2.0

        square = Square(x, y, w)
        squares.append(square)

def distance(prev_s, new_s):
    p1 = [prev_s.x, prev_s.y]
    p2 = [prev_s.x, prev_s.y]
    return math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )

def bound_prediction(prediction, w, Width, Height):
    
    x = prediction[0]# - 0.5 * w
    y = prediction[1]# - 0.5 * w

    if(x + w > Width):
        diff = x + w - Width
        x -= diff

    if(y + w > Height):
        diff = x + w - Height
        y -= diff

    if(x < 0): x = 0

    if(y < 0): y = 0

    prediction[0] = x
    prediction[1] = y

def smooth_squares(squares, smooths, Width, Height):

    x = round(squares[0].x)
    y = round(squares[0].y)
    w = round(squares[0].w)
    
    for i in range(0, 100): KLMN.Predict(x, y, w)

    for square in squares:

        x = round(square.x)
        y = round(square.y)
        w = round(square.w)
        
        prediction = KLMN.Predict(x, y, w)
        bound_prediction(prediction, w, Width, Height)

        smooth = Square(float(prediction[0]), float(prediction[1]), w)
        smooths.append(smooth)

def smooth_damp_squares(squares, smooths, Width, Height):

    smooth_vector = VectorSmooth(squares[0].x, squares[0].y, 0, 0)
    w = round(squares[0].w)

    smooth_time = 0.25 # 0.085
    delta_time = 1 / 24

    for square in squares:

        smooth_x = SmoothDamp(smooth_vector.x, square.x, smooth_vector.xv, smooth_time, delta_time)
        smooth_y = SmoothDamp(smooth_vector.y, square.y, smooth_vector.yv, smooth_time, delta_time)

        smooth_vector = VectorSmooth(smooth_x[0], smooth_y[0], smooth_x[1], smooth_y[1])
        
        prediction = [smooth_vector.x, smooth_vector.y]
        bound_prediction(prediction, w, Width, Height)
        
        smooth = Square(float(prediction[0]), float(prediction[1]), w)
        smooths.append(smooth)
        
        smooth = Square(square.x, square.y, w)
        smooths.append(smooth)

def SmoothDamp(current, target, currentVelocity, smoothTime, deltaTime):
    #maxSpeed = 99999

    smoothTime = Max(0.0001, smoothTime)
    num1 = 2 / smoothTime
    num2 = num1 * deltaTime
    num3 = (1.0 / (1.0 + num2 + 0.479999989271164 * num2 * num2 + 0.234999999403954 * num2 * num2 * num2))
    num4 = current - target
    num5 = target
    
    target = current - num4
    num7 = (currentVelocity + num1 * num4) * deltaTime
    currentVelocity = (currentVelocity - num1 * num7) * num3
    num8 = target + (num4 + num7) * num3

    if (num5 - current > 0.0 == num8 > num5):
        num8 = num5
        currentVelocity = (num8 - num5) / deltaTime

    return [num8, currentVelocity]

def Max(a, b):
    if (a > b):
        return a
    return b

def execute(pfile, w):

    rows = []

    squares = []
    smooths = []

    Width = 0
    Height = 0

    input_file = open(pfile, "r")
    lines = input_file.read().splitlines()

    first_line = True
    for line in lines:
        split = line.split(" ")
        if first_line:
            first_line = False
            Width = float(split[0])
            Height = float(split[1])
        else:
            row = Row(float(split[1]), float(split[2]), float(split[3]), float(split[4]))
            rows.append(row)

    calculate_squares(rows, squares, w)
    #smooth_squares(squares, smooths, Width, Height)
    smooth_damp_squares(squares, smooths, Width, Height)

    output_file = "p2_output.txt"
    output = open(output_file, "w")

    for smooth in smooths:
        output.write(str(smooth.x) + " " + str(smooth.y) + " " + str(smooth.w) + "\n")

    output.close()
    
    return output_file