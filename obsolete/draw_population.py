from PIL import Image
from numpy import random

class Circle:
    species = "Canis familiaris"
        # should come in format (0,0,1,[0,0,0])
    def __init__(self, x, y, r, color):
        self.x = x
        self.y = y
        self.r = r 
        self.color = color
    def getPosition(self):
        return self.x, self.y
    def getRadius(self):
        return self.r
    def getColor(self):
        return self.color
    def modifyPosition(self,x,y):
        self.x = x
        self.y = y
    def modifyRadius(self,r):
        self.r = r
    def modifyColor(self,color):
        self.color = color
        
        
        
        
        
        
        
    def draw_circle(self, im):

        x,y=self.getPosition()
        r= self.getRadius()
        c= self.getColor()
        width, height = im.size
        print("\n\nThis Circle's properties inside class function", x, y, r)
        print("\nThis image properties inside class function", width, height)
        for i in range(width):
            for j in range(height):

                # the following if part will create
                # a square with color orange
                if((x-i)**2 + (y-j)**2 < r):

                    # RGB value of orange.
                    pixel_map[i, j] = (1,1,1)


                    
                    
                    
                    
                    
    def modify_color_2_avg(self, im):
        x,y = self.getPosition()
        r= self.getRadius()
        
        width, height = im.size
        
        average_color = [0,0,0]
        pixel_counter = 0

        for i in range(width):
            for j in range(height):

                # the following if part will create
                # a square with color orange
                if((x-i)**2 + (y-j)**2 < r):
                    average_color[0] += im.getpixel((i, j))[0]
                    average_color[1] += im.getpixel((i, j))[1]
                    average_color[2] += im.getpixel((i, j))[2]
                    pixel_counter += 1
        for k in range(len(average_color)):
            average_color[k] //= pixel_counter

        self.modifyColor((* average_color,)) #convert list to tuple
        

# Import an image from directory:
im = Image.open("mona.png")

# Extracting pixel map:
pixel_map = im.load()

# Extracting the width and height
# of the image:
width, height = im.size

# taking half of the width:
for i in range(width//2):
	for j in range(height):
		
		# getting the RGB pixel value.
		r, g, b, p = im.getpixel((i, j))
		
		# Apply formula of grayscale:
		grayscale = (0.299*r + 0.587*g + 0.114*b)

		# setting the pixel value.
		pixel_map[i, j] = (int(grayscale), int(grayscale), int(grayscale))


circle_population = []
new_x, new_y, new_radius = 0, 0, 0
for i in range(21):
    new_x = random.uniform(0,width)
    new_y = random.uniform(0,height) 
    new_radius = random.uniform(width/4,width)
    
    circle_population.append(Circle(new_x, new_y, new_radius, [30,30,30]))
    circle_population[i].modify_color_2_avg(im)
    
    
    print("This Circle's properties", new_x, new_y, new_radius)
    circle_population[i].draw_circle(im)
    print(circle_population[i])

        
        
# Saving the final output
# as "grayscale.png":
im.save("bubbles.png", format="png")

# use input_image.show() to see the image on the
# output screen.
im.show()
