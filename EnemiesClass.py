# Inherits from AssetsClass. Parent class for all enemies.

from AssetsClass import assets
from abc import ABC, abstractmethod

class enemies(assets):
    def __init__(self,visibleOnScreen, col, row, imageFile, soundFile, name, tileWidth, index,basePath):
        super().__init__(visibleOnScreen, col, row, imageFile, soundFile, name, tileWidth, index)
        self._showHealthbar = True
        self.waitingForDismiss = False
        self.collided = False
        self._tileOfset = [0,0]

    # Overrides checkCollsions in the assets class because self.collided must also be False and also enemy-specific funciton calls.
    def checkCollision(self,catMask,catX,catY,tileWidth,xOfset,yOfset,frontArray,backArray,fishCount,speed,itemCount):
        displayX = self._col*tileWidth +self._tileOfset[1] -xOfset +2
        displayY = self._row*tileWidth +self._tileOfset[0] -yOfset +2
        offset = (catX - displayX, catY - displayY)

        if self._visibleOnScreen == True and self.collided == False:
            if self._mask.overlap(catMask,offset):
                self.waitingForDismiss = True
                self.collided = True
                fishCount -= 1
                if self.name == "flea": # Cat loses fish.
                    frontArray = fleas.respawn(self,frontArray,backArray)
                elif self.name == "tick": # Cat loses fish.
                    frontArray = ticks.respawn(self,frontArray,backArray)
                elif self.name == "car": # Cat loses fish.
                    frontArray = cars.respawn(self,frontArray,backArray)
                elif self.name == "dog": # Cat loses fish.
                    frontArray = dogs.respawn(self,frontArray,backArray)
                elif self.name == "lilly": # Cat loses fish.
                    frontArray = lillies.respawn(self,frontArray,backArray)
                self.collided = False
                self._soundFile.play()

        return frontArray,fishCount,speed,itemCount
    
    @abstractmethod
    def respawn(self,frontArray,backArray):  #Abstract method- all children overwrite this (interface).
        pass

    @abstractmethod
    def display(self,tileWidth,xOfset,yOfset,display):  #Abstract method- all children overwrite this (interface).
        pass

import pygame
pygame.init()
from FleasClass import fleas
from TicksClass import ticks
from CarsClass import cars
from DogsClass import dogs
from LilliesClass import lillies
pygame.mixer.init()