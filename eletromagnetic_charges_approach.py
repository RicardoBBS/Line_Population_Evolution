from re import X
from numpy import random
from math import sqrt
from PIL import Image, ImageFilter
from tqdm import tqdm

import gizeh
from moviepy.editor import *






class generalCounter:
    def __init__(self,count):
        self.count = count
    def getCount(self):
        return self.count
    def incrementCount(self):
        self.count += 1




#General variables to tweak
# only mass or dt should be needed as they are used only once in a multiplication, their values can be collapsed
class simSettings:
   def __init__(self):
      self.neighborRadius = 300

class Node:
   def __init__(self, x, y):
      self.x = x
      self.y = y
      self.history=[]
      self.charge = 0
      self.appliedForce = [0,0]
      self.neighborList = []

   
   def updateCharge(self, im):
      R,G,B = im.getpixel((self.x, self.y))
      brightness = sum([R,G,B])/3 ##0 is dark (black) and 255 is bright (white)
      self.charge = brightness2ChargeFunction(brightness)
      

      



def distance(node1,node2):
   return sqrt((node1.x - node2.x)**2 + \
               (node1.y - node2.y)**2   \
               )




def oneTimeGraphCreation(list, simSettings):
   for element in list:
      for potentialNeighbor in list:
         if element == potentialNeighbor:
            continue
         if distance(element,potentialNeighbor) <= simSettings.neighborRadius:
            element.neighborList.append(potentialNeighbor)
            #Potential Neighbor just got promoted to Neighbor



#TODO: make this function also customizable in blender
def brightness2ChargeFunction(brightness):
   return (brightness - 255*7/8)*chargeFactor


#not real-world accurate force to deslocation relation but serves its purpose
#TODO: make function update values within class

def updateLocation(element):
   x = element.x + element.appliedForce[0]
   y = element.y + element.appliedForce[1]
   
   if(x<0):
      x = 0
   elif(w<x):
      x = w -1

   if(y<0):
      y = 0
   elif(h<y):
      y = h -1

   return x, y


#RETURNS: function by which force diminishes with distance
#default is return 1/r^2
#TODO: is to make this function customizable with blender curve editor
def distanceFunction(node1,node2):
   if distance(node1,node2) == 0:
      return 1000
   return 1/(distance(node1,node2)**2)

def forceDirection(node1,node2):
   if distance(node1,node2) == 0:
      return [0,0]
   #[x1-x2,y1-y2] normalized, order of subtraction inverted for charges to apply correctly
   x= (node1.x - node2.x)/distance(node1,node2)
   y= (node1.y - node2.y)/distance(node1,node2)
   
   return x,y


def forceVector(node1,node2):
   x,y = forceDirection(node1,node2)
   x *= node1.charge * node2.charge * distanceFunction(node1,node2)
   y *= node1.charge * node2.charge * distanceFunction(node1,node2)
   return x,y

def updateState(list, im):
   for element in list:
      element.history.append([int(element.x), int(element.y)])
      #print(element.x, element.y, updateLocation(element))
      element.x, element.y = updateLocation(element)
      #print(element.x, element.y)
      element.appliedForce = [0,0]
      element.updateCharge(im)



def runPhysicsCycle(list, im):
   updateState(list, im)
   for element in list:
      for neighbor in element.neighborList:
         x,y=  forceVector(element,neighbor)
         element.appliedForce[0] += x
         element.appliedForce[1] += y


"""
def neighborOfNeighborGraphUpdate(list, simSettings):
   #alternate implementation would be just testing distances and adding without need
   #for this candidate list, but this would mean checking the same nodes too many times

   #i just figured out that we do need the list anyways so that we aren't deleting or creating
   #unnecessarily other points in our exploration space
   potentialNeighborList = []
   for element in list:
      potentialNeighborList = []
      for neighbor in element.neighborList:

         #Gather contestants
         for secondDegreeNeighbor in neighbor.neighborList:
            if secondDegreeNeighbor not in potentialNeighborList:
               potentialNeighborList.append(secondDegreeNeighbor)
         #VIP gets a spot too
         if neighbor not in potentialNeighborList:
               potentialNeighborList.append(neighbor)

      #Elimination phase
      for potentialNeighbor in potentialNeighborList:
         if element == potentialNeighbor:
            potentialNeighborList.remove(potentialNeighbor)
            continue
            #self cannot compete
         if distance(element,potentialNeighbor) > simSettings.neighborRadius:
            potentialNeighborList.remove(potentialNeighbor)
            #Potential Neighbor just got eliminated from the contest

      #flush 
      #TODO: (maybe not necessary we'll see)
      element.neighborList = []
      #all winners get cookies
      element.neighborList = potentialNeighborList

def recordPositions(list):
   record = []
   for element in list:
      record.append([element.x,element.y])
   return record
   """








# Import an image from directory:
im = Image.open("abstract_masterpiece.png")

im = im.convert ('RGB')

# Extracting pixel map:
pixel_map = im.load()

# Extracting the width and height
# of the image:
width, height = im.size








chargeFactor = 0.5






gc = generalCounter(0)



nodeList = [] 
simSettings = simSettings()
  
for i in range (500):
    nodeList.append( Node(random.uniform(0,width),random.uniform(0,height)) )

oneTimeGraphCreation(nodeList, simSettings)




w,h = im.size # width, height, in pixels
duration = 10 # duration of the clip, in seconds
iterations = 100

#Runnning simulation

for n in tqdm(range(iterations)):

   im1 = im.filter(ImageFilter.GaussianBlur(radius = (iterations - n)/2))
   im1 = im.convert ('RGB')

   # Extracting pixel map:
   pixel_map = im1.load()


   runPhysicsCycle(nodeList,im1)
      
   






def make_frame(t):
    circleList = []
    
    for node in nodeList:
        surface = gizeh.Surface(w, h)
        radius = 3
        circle = gizeh.circle(radius, xy=(node.history[gc.getCount()][0], node.history[gc.getCount()][1]), fill=(1, 0, 0))
        circleList.append(circle)
    for element in circleList:
        element.draw(surface)
    if gc.getCount() < len(nodeList[0].history) - 1:
        gc.incrementCount()

    return surface.get_npimage()


duration = 20

clip = VideoClip(make_frame, duration=duration)
clip.write_gif("6nd_simulation.gif",fps=6,opt="OptimizePlus", fuzz=10)
