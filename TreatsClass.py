# Inherits from AssetsClass. Respawn once collected.

from CollectablesClass import collectables
import random
import pygame
pygame.init()
import os

class treats(collectables):
    # Respawn treat on random grass tile.
    def respawn(self,frontArray,backArray,tileWidth,basePath):
        x,y = random.randint(2,len(frontArray[0])-3),random.randint(2,len(frontArray)-3)
        while frontArray[y][x] != 0 or not(backArray[y][x] == 1 or backArray[y][x] == 3):
            x,y = random.randint(2,len(frontArray[0])-3),random.randint(2,len(frontArray)-3)
        if frontArray[y][x] != 0:
            self.respawn(frontArray,backArray)
        
        frontArray[y][x] = 4

        type = str(random.randint(1,4))
        image = pygame.image.load(os.path.join(basePath,"Assets/Collectables/Treats")+type+".png").convert_alpha()
        imageFile = pygame.transform.smoothscale(image,(tileWidth,tileWidth))
        return x,y,frontArray,imageFile
