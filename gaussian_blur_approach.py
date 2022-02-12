from re import X
from numpy import append, random, argmin
from math import sqrt, sin, cos, pi
from PIL import Image, ImageFilter
from tqdm import tqdm


import gizeh
from moviepy.editor import *



#as a matter of orders we will start with one point descending gaussian blur in image


class Node:
    def __init__(self, x, y):
        self.position = [x , y]
        self.history=[]
        self.radiusofMovement = 200
    
    def decideAndMove(self, im):
        brightnesses = []
        division = 16
        angle = 0
        for count in range(division):
            angle = count/division
            brightnesses.append(self.getProbeBrightness(im, angle))
        chosen = argmin(brightnesses)
        #time to write history, update jump-range, 
        self.history.append(self.position)
        self.radiusofMovement *= brightnesses[chosen] #the darker the point we move toward, the less we need to move afterwards
        angle = chosen / division
        self.setPosition(self.getProbePosition(angle))



    def setPosition(self, updatedP):
        X , Y = updatedP[0], updatedP[1]
        if (0<=X<=w):
            self.position[0] = X
        elif(X<0):
            self.position[0] = 0
        elif(w<X):
            self.position[0] = w

        if (0<=Y<=h):
            self.position[1] = Y
        elif(Y<0):
            self.position[1] = 0
        elif(h<Y):
            self.position[1] = h


    def getProbePosition(self,angle):
        X , Y = self.position
        r = self.radiusofMovement
        return X+r*cos(2*pi*angle) , Y+r*sin(2*pi*angle)

    def getProbeBrightness(self, im, angle):

        #Get probe position
        probePosition = self.getProbePosition(angle)

        #Check probe is inside image
        if ( 0<probePosition[0]<w and 0<probePosition[1]<h):
            R,G,B = im.getpixel(probePosition)
            return sum([R,G,B])/3 ##0 is dark (black) and 255 is bright (white)
        #If not we report a "repellent" color
        else:
            return 255 





# Import an image from directory:
im = Image.open("aM2.png")

im = im.filter(ImageFilter.GaussianBlur(radius = 30))
#im.show()

im = im.convert ('RGB')

# Extracting pixel map:
pixel_map = im.load()

w, h = im.size








nodeList=[]

for i in range (500):
    nodeList.append( Node(random.uniform(0,w),random.uniform(0,h)) )



#run simulation

for t in tqdm(range(500)):
    for node in nodeList:
        node.decideAndMove(im)




print(len(nodeList[0].history))

def make_frame(t):
    circleList = []
    T = int(min(t, len(nodeList[0].history) - 1))
    for node in nodeList:
        surface = gizeh.Surface(w, h)
        radius = 3
        circle = gizeh.circle(radius, xy=(node.history[T][0], node.history[T][1]), fill=(1, 0, 0))
        circleList.append(circle)
    for element in circleList:
        element.draw(surface)

    return surface.get_npimage()


duration = 20

clip = VideoClip(make_frame, duration=duration)
clip.write_gif("2nd_simulation.gif",fps=12, opt="OptimizePlus", fuzz=10)


#TODO: figure out how to run simple image sequence














"""
duration = 10


screensize = (w,h)
image_clip =  ImageClip("abstract_masterpiece.png", duration=duration)
final_clip = CompositeVideoClip([image_clip,final_clip.set_pos('center')])
final_clip.write_videofile('coolTextEffects.avi',fps=25,codec='mpeg4')
"""
