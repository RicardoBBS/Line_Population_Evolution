from re import X
from numpy import random
from math import sqrt
from PIL import Image

import gizeh
import moviepy.editor as mpy


#General variables to tweak
# only mass or dt should be needed as they are used only once in a multiplication, their values can be collapsed
class simSettings:
   def __init__(self):
      self.neighborRadius = 100
      self.dt = 0.01
      self.frame = 0

class Node:
   def __init__(self, x, y):
      self.x = x
      self.y = y
      self.charge = 0
      self.appliedForce = [0,0]
      self.neighborList = []

   
   def updateCharge(self, im):
      R,G,B = im.getpixel((self.x, self.y))
      brightness = sum([R,G,B])/3 ##0 is dark (black) and 255 is bright (white)
      self.charge = brightness2ChargeFunction(brightness)

      

# Import an image from directory:
im = Image.open("abstract_masterpiece.png")

im = im.convert ('RGB')

# Extracting pixel map:
pixel_map = im.load()

# Extracting the width and height
# of the image:
width, height = im.size


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
   return (brightness - 255/2)*100


#not real-world accurate force to deslocation relation but serves its purpose
#TODO: make function update values within class

def updateLocation(element):
   x = element.x + element.appliedForce[0]
   y = element.y + element.appliedForce[1]
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

def forceFunction(node1,node2):
   x,y = forceDirection(node1,node2)
   x *= node1.charge * node2.charge * distanceFunction(node1,node2)
   y *= node1.charge * node2.charge * distanceFunction(node1,node2)
   return x,y

def updateState(list, im):
   for element in list:
      element.x, element.y = updateLocation(element)
      element.appliedForce = [0,0]
      element.updateCharge(im)



def runPhysicsCycle(list, im):
   updateState(list, im)
   for element in list:
      for neighbor in element.neighborList:
         element.appliedForce += forceFunction(element,neighbor)



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


list = [] 
simSettings = simSettings()
  
for i in range (500):
    list.append( Node(random.uniform(0,width),random.uniform(0,height)) )

oneTimeGraphCreation(list, simSettings)

frames = []


W,H = im.size # width, height, in pixels
duration = 3 # duration of the clip, in seconds


#Runnning simulation
for forty in range(3):
   #TODO: make period between neighbor graph update exploration
   print("\n\n HELLO Bitches", forty)
   for n in range(40):
      runPhysicsCycle(list,im)
      frames.append(recordPositions(list))
   simSettings.neighborRadius *= 0.6 
   neighborOfNeighborGraphUpdate(list, simSettings)
   frames.append(recordPositions(list))






def make_frame(t):
   circleList = []
   for node in frames[int(t*15)]:
      surface = gizeh.Surface(W, H)
      radius = 3
      circle = gizeh.circle(radius, xy=(node[0], node[1]), fill=(1, 0, 0))
      circleList.append(circle)
   for element in circleList:
      element.draw(surface)
   return surface.get_npimage()

clip = mpy.VideoClip(make_frame, duration=duration)
clip.write_gif("2nd_simulation.gif",fps=15, opt="OptimizePlus", fuzz=10)

