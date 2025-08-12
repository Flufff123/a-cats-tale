# Parent class for all collectables and enemies.

from abc import ABC, abstractmethod

class assets:
    def __init__(self,visibleOnScreen,col,row,imageFile,soundFile,name,tileWidth,index):
        self._visibleOnScreen = visibleOnScreen # Assets are not shown or updated when not visible on screen.
        self._col = col # Asset coordinates in tiles.
        self._row = row
        image = pygame.image.load(imageFile).convert_alpha()
        self._imageFile = pygame.transform.smoothscale(image,(tileWidth-4,tileWidth-4))
        self._soundFile = pygame.mixer.Sound(soundFile)
        self.name = name # Each type of asset has a different name.
        self._mask = pygame.mask.from_surface(self._imageFile,250) # Player-asset collsision detection done using masks for higher accuracy.
        self._index = index # Numbered enemy and cat need types.

    # Return whether an asset is currently visible on screen.
    def checkVisibleOnScreen(self,topRow,botRow,leftCol,rightCol):
        if (leftCol-2 < self._col < rightCol+2) and (topRow-2 < self._row < botRow+2):
            self.visibleOnScreen = True
        else:
            self.visibleOnScreen = False

    @abstractmethod
    def checkCollision(self,catMask,catX,catY,tileWidth,xOfset,yOfset,frontArray,backArray,fishCount,speed,itemCount,basePath):  #Abstract method- all children overwrite this (interface).
        pass

    @abstractmethod
    def display(self,tileWidth,xOfset,yOfset,display):  #Abstract method- all children overwrite this (interface).
        pass

import pygame
pygame.init()
import pygame
pygame.mixer.init()
from CollectablesClass import collectables