'''
This program initialies, updates and creates paw prints.
'''

# Generate new paw prints at game start.
def resetPawPrints(colouredPrints,display):
    pawPrintTrails = [] # [0]x, [1]y, [2]transparency, [3]colour
    parentPawPrints = [] # [0]pivot
    for index in range (0,7): # Number of trails active at once.
        pawPrintTrails,parentPawPrints = createNewPawPrintTrail(pawPrintTrails,parentPawPrints,colouredPrints,display)
    counter = 0
    return pawPrintTrails,parentPawPrints,counter

# Create a new paw print trail (either at start of game/when a trail is deleted).
def createNewPawPrintTrail(pawPrintTrails,parentPawPrints,colouredPrints,display):
    colour = newPrintColour(colouredPrints) # Call function to randomly chose next paw print colour.
    pivot = random.randint(0,1) # Pivot sets left or right print.
    x = random.randint(0,display.get_width() -colouredPrints[0].get_width())+pivot # Random x coordinate of new trail.
    if len(pawPrintTrails) < 6: # Trails generated at random y coodinate if less than 6 trails exist (start of game only).
        y = random.randint(0,display.get_height())
    else:
        y = display.get_height() # Normally start new trail at bottom of screen.
    if pivot == 1: # Initial print is left/right?
        pivot = 20
    else:
        pivot = -20
    pawPrintTrails.append([[x,y,255,colour]]) # Add new trail to both arrays.
    parentPawPrints.append(pivot)
    return pawPrintTrails,parentPawPrints

# Randomly select the colour of the next paw print.
def newPrintColour(colouredPrints):
    colours = {
        0:colouredPrints[0],
    }
    colour = colours[0]
    return colour

# Check for invisible paws and empty trails, and generate a new paw for each trail.
def updatePrints(pawPrintTrails,parentPawPrints,currentTrail,colouredPrints,display):
    if pawPrintTrails[currentTrail][0][2] <= 40: # First paw invisible?
        pawPrintTrails[currentTrail].pop(0) # Yes: Delete paw from trail.
    if len(pawPrintTrails[currentTrail]) == 0: # Length of trail = 0?
        pawPrintTrails.pop(currentTrail) # Delete current trail from both arrays.
        parentPawPrints.pop(currentTrail)
        pawPrintTrails,parentPawPrints = createNewPawPrintTrail(pawPrintTrails,parentPawPrints,colouredPrints,display) # Generate new trail
    else:
        pivot = parentPawPrints[currentTrail] # If current trail isn't empty, continue extending it by generating a new print.
        newX = pawPrintTrails[currentTrail][len(pawPrintTrails[currentTrail])-1][0]+pivot
        newY = pawPrintTrails[currentTrail][len(pawPrintTrails[currentTrail])-1][1] - colouredPrints[0].get_height()

        if newY>=0 and newY<=display.get_height(): # New coordinates fit within screen?
            pawPrintTrails[currentTrail].append([newX,newY,255,newPrintColour(colouredPrints)]) # If so, add paw to end of current trail
            parentPawPrints[currentTrail] = parentPawPrints[currentTrail]*-1 # If paw is created, pivot to other side
    return pawPrintTrails,parentPawPrints

# Draw all the prints in the current trail.
def justDraw(pawPrintTrails,parentPawPrints,currentTrail,colouredPrints,display):
    for currentPrint in range (0,len(pawPrintTrails[currentTrail])): # Repeat for each paw in trail.
        tempPrint = pawPrintTrails[currentTrail][currentPrint][3].copy() # Copy origional paw print imange to avoid changing its transparency perminantly.
        tempPrint.set_alpha(pawPrintTrails[currentTrail][currentPrint][2])
        pawPrintTrails[currentTrail][currentPrint][2] -= 2 # Rate of fade.
        display.blit(tempPrint,(pawPrintTrails[currentTrail][currentPrint][0],pawPrintTrails[currentTrail][currentPrint][1])) # Blit current paw to screen.
    return pawPrintTrails,parentPawPrints

# Load and scale a paw print image.
def loadPawPrint(printName,display,basePath):
    image = pygame.image.load(os.path.join(basePath,"Assets/Screens/")+printName+".png").convert_alpha()
    scaleFactor = display.get_width() /(image.get_width() *50)
    image = pygame.transform.smoothscale(image, (int(display.get_width() /50), int(display.get_height()*scaleFactor*0.5)))
    image.set_alpha(255) # 0 = fully transparent, 255 = fully opaque.
    return image

import pygame
pygame.init()
import random
import os