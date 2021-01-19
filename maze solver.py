#imports

from pygame import *
from random import *

#initializing pygame
init()

#loading the maze image
imageLocation = input("please input your image's location (input SAMPLE if you want a sample maze):\n")
if imageLocation == "SAMPLE":
        img = image.load("Sample_Maze.png")
else:
        img = image.load(imageLocation)
screen = display.set_mode((img.get_width(), img.get_height()))
screen.blit(img, (0, 0))

print("you may now click on any two points to find the shortest path between them!")


def Solve(x1, y1, x2, y2):
        #Set the color for filling the maze
        #color = (randint(0, 255), randint(0, 255), randint(0, 255))
        color = (150, 120, 170)
        #Set the parent of all nodes (pixels on screen) to (-2,-2)
        par=[[(-2, -2) for i in range (1000)] for j in range (1000)]
        par[x1][y1] = (-2, -2)
        #Set the height of every node to a very large number
        h=[[1000000000000 for i in range (1000)] for j in range (1000)]
        h[x1][y1] = 0
        #initialize a Queue for use in the BFS algorithm
        q = []
        #we do not implement a queue data structure and instead use a simple pointer to the current queue front
        qPointer = 0
        #append the starting point to the queue
        q.append((x1, y1))
        #simple function that returns the sum of the difference of the color values of two points
        def dif(a,b):
                q = abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])
                #print(q)
                return q
        #Begin the BFS algorithm and continue untill the q is empty (we haven't reached the end of our array)
        while qPointer != len(q):
                #define x and y to represent the co-ordinates of the current node (pixel)
                x,y = q[qPointer]
                #set the color (used as coloring the maze for a visual effect before displaying the solution
                screen.set_at((x, y), color)
                #we do not need to update the disply evey pixel we update, instead we update every 1000 pixels we color
                #this improves performance and creates a visual effect of filling the maze
                if qPointer % 1000 == 0:
                        display.update()
                #increment the queue pointer
                qPointer += 1
                #check to make sure the pixel we are about to process is in bounds
                if x < 1 or x > img.get_width()-5 or y < 1 or y > img.get_height()-5:
                        continue #otherwise skip this pixel and move to the next in queue
                
                #we go through the four different children of the current node
                #these are the pixels in the cardinal directions of the current pixel
                
                #the pixel to the top of the current pixel
                xNext = x - 1
                yNext = y
                #check the color difference of the two pixels to make sure there is no wall
                #(10 is a number that works for most clear mazes with white path and black walls,
                # this number needs to be tweaked for other kinds of mazes)
                if dif(img.get_at((x, y)), img.get_at((xNext, yNext))) < 10:
                        if h[x][y] + 1 < h[xNext][yNext]: #ensure we havent visited this node yet
                                h[xNext][yNext] = h[x][y] + 1 #set the height of the node
                                par[xNext][yNext] = (x, y) #set the parent (which is current node)
                                q.append((xNext, yNext)) #add the node to the processing queue
                                
                #the pixel to the right of the current pixel
                xNext = x 
                yNext = y + 1
                #check the color difference of the two pixels to make sure there is no wall
                #(10 is a number that works for most clear mazes with white path and black walls,
                # this number needs to be tweaked for other kinds of mazes)
                if dif(img.get_at((x, y)), img.get_at((xNext, yNext))) < 10:
                        if h[x][y] + 1 < h[xNext][yNext]: #ensure we havent visited this node yet
                                h[xNext][yNext] = h[x][y] + 1 #set the height of the node
                                par[xNext][yNext] = (x, y) #set the parent (which is the current node)
                                q.append((xNext, yNext)) #add the node to the processing queue

                #the pixel to the left of the current pixel
                xNext = x 
                yNext = y - 1
                #check the color difference of the two pixels to make sure there is no wall
                #(10 is a number that works for most clear mazes with white path and black walls,
                # this number needs to be tweaked for other kinds of mazes)
                if dif(img.get_at((x, y)), img.get_at((xNext, yNext))) < 10:
                        if h[x][y] + 1 < h[xNext][yNext]: #ensure we havent visited this node yet
                                h[xNext][yNext] = h[x][y] + 1 #set the height of the node
                                par[xNext][yNext] = (x, y) #set the parent (which is the current node)
                                q.append((xNext, yNext)) #add the node to the processing queue

                #the pixel blow the current pixel
                xNext = x + 1
                yNext = y
                #check the color difference of the two pixels to make sure there is no wall
                #(10 is a number that works for most clear mazes with white path and black walls,
                # this number needs to be tweaked for other kinds of mazes)
                if dif(img.get_at((x, y)), img.get_at((xNext, yNext))) < 10:
                        if h[x][y] + 1 < h[xNext][yNext]: #ensure we havent visited this node yet
                                h[xNext][yNext] = h[x][y] + 1 #set the height of the node
                                par[xNext][yNext] = (x, y) #set the parent (which is the current node)
                                q.append((xNext, yNext)) #add the node to the processing queue

        #set the color depicting the path
        #color2 = (255 - color[0], 255 - color[1], 255 - color[2])
        color2 = (255, 255, 255)
        #start from the end point and color the parents until we reach the starting point (with parent (-2,-2))
        while (par[x2][y2] != (-2, -2)):
                screen.set_at((x2, y2), color2)
                x2, y2 = par[x2][y2]
                display.update()

#initialize the starting point and a flag for when the program is closed
xStart = -1 
yStart = -1
closeFlag = 0

#main render loop
while not closeFlag:
        #process events
        for e in event.get():
                if e.type == MOUSEBUTTONDOWN:
                        if xStart == -1: #this means that the starting point hasnt been set, so set it
                                xStart, yStart = mouse.get_pos()
                        else: #otherwise reset set the end points and do the processing, then reset the starting point
                                xEnd, yEnd = mouse.get_pos()
                                Solve(xStart, yStart, xEnd, yEnd)
                                xStart = -1
                                yStart = -1
                if e.type == QUIT:
                        quit()
                        closeFlag = 1
        if not closeFlag:
                display.update()
