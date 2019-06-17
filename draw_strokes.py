# this snippet of code is derived taken from:
# https://github.com/hardmaru/sketch-rnn/blob/master/utils.py
# please use consistent license

import numpy as np
import random

# libraries required for visualisation:
from IPython.display import SVG, display
import svgwrite
# conda install -c omnia svgwrite=1.1.6 if you don't have this lib

# helper function for draw_strokes
def get_bounds(data):
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0

    abs_x = 0
    abs_y = 0
    for i in range(len(data)):
        x = float(data[i,0])
        y = float(data[i,1])
        abs_x += x
        abs_y += y
#         print(abs_x, abs_y)
        min_x = min(min_x, abs_x)
        min_y = min(min_y, abs_y)
        max_x = max(max_x, abs_x)
        max_y = max(max_y, abs_y)

    return (min_x, max_x, min_y, max_y)

# little function that displays vector images and saves them to .svg
def draw_strokes(sketches, dims=(640, 360),factor=0.3, svg_filename = 'sample.svg'):
    dwg = svgwrite.Drawing(svg_filename, size=dims)
    dwg.add(dwg.rect(insert=(0, 0), size=dims,fill=svgwrite.rgb(220,220,220)))
    num_objs = len(sketches)
    for i, sketch in enumerate(sketches):
        start_point = (random.randint(int(i/num_objs*dims[0] + 0.1*dims[0]), int((i+1)/num_objs*dims[0]) - 0.1*dims[0]), random.randint(int(i/num_objs*dims[1] + 0.1*dims[1]), int((i+1)/num_objs*dims[1] - 0.1*dims[1])))
        min_x, max_x, min_y, max_y = get_bounds(sketch)
    
        lift_pen = 1
        p = "M%s,%s " % start_point
        # print(p)
        command = "m"
        for i in range(len(sketch)):
            if (lift_pen == 1):
                command = "m"
            elif (command != "l"):
                command = "l"
            else:
                command = ""
            x = (float(sketch[i,0]))/(max_x-min_x)*dims[0]*factor
            y = (float(sketch[i,1]))/(max_y-min_y)*dims[1]*factor
            
            lift_pen = sketch[i, 2]
            p += command+str(x)+","+str(y)+" "
            
        color = svgwrite.rgb(random.randint(0,255), random.randint(0,255), random.randint(0,255))
        stroke_width = 3
        dwg.add(dwg.path(p).stroke(color,stroke_width).fill("none"))
        dwg.save()
        
    return dwg.tostring()
