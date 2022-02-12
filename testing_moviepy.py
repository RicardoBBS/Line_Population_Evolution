from numpy import random
from math import sqrt
from PIL import Image

import gizeh
import moviepy.editor as mpy



# Import an image from directory:
im = Image.open("abstract_masterpiece.png")

im = im.convert ('RGB')

# Extracting pixel map:
pixel_map = im.load()

# Extracting the width and height
# of the image:
width, height = im.size



W,H = im.size # width, height, in pixels
duration = 10 # duration of the clip, in seconds



def make_frame(t):
    circleList=[]
    for element in range(100):
      surface = gizeh.Surface(W,H)
      radius = 4
      circle = gizeh.circle(radius, xy = (element*t, element), fill=(1,0,0))
      circleList.append(circle)
    for element in range(100):
      circleList[element].draw(surface)
    return surface.get_npimage()

clip = mpy.VideoClip(make_frame, duration=duration)
clip.write_gif("1st_simulation.gif",fps=15, opt="OptimizePlus", fuzz=10)
