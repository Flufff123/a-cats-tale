# Inherits from EnemiesClass and AssetsClass. No movement during game.

from EnemiesClass import enemies

class staticEnemies(enemies):
    def __init__(self,visibleOnScreen, col, row, imageFileA, soundFile, name, tileWidth, index,basePath, imageFileB):
        super().__init__(visibleOnScreen, col, row, imageFileA, soundFile, name, tileWidth, index, basePath)
        self.__animationTimer = 0
        imageB = pygame.image.load(imageFileB).convert_alpha()
        self.__imageFileB = pygame.transform.smoothscale(imageB,(tileWidth-4,tileWidth-4))

    # Respawn on random grass tile.
    def respawn(self,frontArray,backArray):
        x,y = random.randint(2,len(frontArray[0])-3),random.randint(2,len(frontArray)-3)
        while frontArray[y][x] != 0 or backArray[y][x] != 1:
            x,y =random.randint(2,len(frontArray[0])-3),random.randint(2,len(frontArray)-3)
        self._col,self._row = x,y
        if self.name == "dog":
            frontArray[y][x] = 9
        elif self.name == "lily":
            frontArray[y][x] = 10
        return frontArray
    
    # Overrides display function because of timmed costume changes for 2-frame animation.
    def display(self,tileWidth,xOfset,yOfset,display):
        if self._visibleOnScreen == True:
            displayX = self._col*tileWidth -xOfset+2
            displayY = self._row*tileWidth -yOfset+2
            self.__animationTimer += 1
            if self.__animationTimer < 10:
                display.blit(self._imageFile,(displayX,displayY))
            elif self.__animationTimer < 20:
                display.blit(self.__imageFileB,(displayX,displayY))
            else:
                self.__animationTimer = 0
                display.blit(self._imageFile,(displayX,displayY))
  
import random
import pygame
pygame.init()