# Parent class for all collectables.

from AssetsClass import assets

class collectables(assets):
    def __init__(self,visibleOnScreen,col,row,imageFile,soundFile,name,tileWidth,index):
        super().__init__(visibleOnScreen,col,row,imageFile,soundFile,name,tileWidth,index)

    # Show an asset on the screen if it is currnetly visible.
    def display(self,tileWidth,xOfset,yOfset,display):
        if self._visibleOnScreen == True:
            displayX = self._col*tileWidth -xOfset +2
            displayY = self._row*tileWidth -yOfset +2
            display.blit(self._imageFile,(displayX,displayY))

    # Check for a player-asset collsision using masks. This function is only used b y treats and fish because other assets have their own checkCollision functions.
    # Polymorphism: Override implemenation of base class.
    def checkCollision(self,catMask,catX,catY,tileWidth,xOfset,yOfset,frontArray,backArray,fishCount,speed,itemCount,basePath,fishAssets,treatAssets):
        displayX = self._col*tileWidth -xOfset +2
        displayY = self._row*tileWidth -yOfset +2
        offset = (catX-displayX,catY-displayY)
        if self._visibleOnScreen == True:
            if self._mask.overlap(catMask,offset):
                respawnYesNo = random.randint(0,1)
                if self.name == "fish":
                    fishCount += 1
                    if respawnYesNo == 1:
                        self._col,self._row,frontArray = fishes.respawn(self,frontArray,backArray) # Fish and treats respawn once collected.
                    else:
                        fishAssets.remove(self) # 50% of fish don't respawn.
                elif self.name == "treat":
                    speed = 10
                    if respawnYesNo == 1:
                        self._col,self._row,frontArray,self._imageFile = treats.respawn(self,frontArray,backArray,tileWidth,basePath) # Treat and treats respawn once collected.
                    else:
                        treatAssets.remove(self) # 50% of treats don't respawn.
                self._soundFile.play()
        return frontArray,fishCount,speed,itemCount,fishAssets,treatAssets

import pygame
import random
pygame.init()
from FishClass import fishes
from TreatsClass import treats
from CatNeedsClass import catNeeds
pygame.mixer.init()