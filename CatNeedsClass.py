# Inherits from AssetsClass. Don't respawn once collected.

from CollectablesClass import collectables

class catNeeds(collectables):
    def __init__(self, visibleOnScreen, col, row, imageFile, soundFile, name, tileWidth, index,basePath):
        super().__init__(visibleOnScreen, col, row, imageFile, soundFile, name, tileWidth, index)

        self.collided = False
        self.waitingForDismiss = False

    # Override because must also control waitingForDismiss for popups.
    # Polymorphism: Override implemenation of base class.
    def checkCollision(self,catMask,catX,catY,tileWidth,xOfset,yOfset,frontArray,backArray,fishCount,speed,itemCount):
        displayX = self._col*tileWidth -xOfset +2
        displayY = self._row*tileWidth -yOfset +2
        offset = (catX-displayX,catY-displayY)
        if self._visibleOnScreen == True and self.collided == False:
            if self._mask.overlap(catMask,offset):
                self._soundFile.play()
                self.waitingForDismiss = True
                self.collided = True
                itemCount += 1
                frontArray[self._row][self._col] = 0
                

        return frontArray,fishCount,speed,itemCount

import pygame
pygame.init()
import os
pygame.mixer.init()