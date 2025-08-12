# Inherits from EnemiesClass and AssetsClass. Cars move along the road tiles in the game.

from EnemiesClass import enemies

class cars(enemies):
    def __init__(self, visibleOnScreen, col, row, imageFile, soundFile, name, tileWidth, index,basePath):
        super().__init__(visibleOnScreen, col, row, imageFile, soundFile, name, tileWidth, index,basePath)
        self.__rotatedCar = pygame.transform.rotozoom(self._imageFile,0,1) # negative angle = clockwise.
        self.__lastDir = "None"
        self.__speed = random.randint(3,5)

    # Move car along road. 
    def move(self,backArray,frontArray):
        if self._visibleOnScreen == True:
            if self._tileOfset == [0,0]:
                try:
                    if backArray[self._row-1][self._col] == 3 and self.__lastDir != "down": #Point up.
                        self.__rotatedCar = pygame.transform.rotozoom(self._imageFile,0,1)
                        self.__lastDir = "up" # Stores opposite direction to current movement to prevent car going back on itself after moving one tile accross.
                    elif backArray[self._row][self._col-1] == 3 and self.__lastDir != "right": # Point left.
                        self.__rotatedCar = pygame.transform.rotozoom(self._imageFile,90,1)
                        self.__lastDir = "left"
                    elif backArray[self._row+1][self._col] == 3 and self.__lastDir != "up": # Point down.
                        self.__rotatedCar = pygame.transform.rotozoom(self._imageFile,180,1)
                        self.__lastDir = "down"
                    elif backArray[self._row][self._col+1] == 3 and self.__lastDir != "left": # Point right.
                        self.__rotatedCar = pygame.transform.rotozoom(self._imageFile,-90,1)
                        self.__lastDir = "right"
                    self._mask = pygame.mask.from_surface(self.__rotatedCar)
                except: # In case this row/col doesn't exist  due to unforseen circumstances.
                    pass

            if self.__lastDir == "up": # If not moved a full tile-accross yet, keep offsetting from the current tile to create scrolling effect.
                self._tileOfset[0] -= self.__speed
            elif self.__lastDir == "down":
                self._tileOfset[0] += self.__speed
            elif self.__lastDir == "left":
                self._tileOfset[1] -= self.__speed
            elif self.__lastDir == "right":
                self._tileOfset[1] += self.__speed

            if abs(self._tileOfset[0]) >= 40 or abs(self._tileOfset[1]) >= 40: # Only update grid coordinates once moved a full tile.
                if self._tileOfset[0] >= 40:
                    if backArray[self._row+1][self._col] == 3:
                        self._row += 1
                elif self._tileOfset[0] <= -40:
                    if backArray[self._row-1][self._col] == 3:
                        self._row -= 1
                elif self._tileOfset[1] >= 40:
                    if backArray[self._row][self._col+1] == 3:
                        self._col += 1
                elif self._tileOfset[1] <= -40:
                    if backArray[self._row][self._col-1] == 3:
                        self._col -= 1
                self._tileOfset = [0,0]

        if backArray[self._row][self._col] != 3:# # If no longer on road for some reason, respawn. 
            frontArray = self.respawn(frontArray,backArray)

        return frontArray # Returns frontArray (respawn causes it to be ammended).

    # Overrides assetsClass version of this function because it is the rotated version of the car that is bitted (not the origional image).
    def display(self,tileWidth,xOfset,yOfset,display):
        if self._visibleOnScreen == True:
            displayX = self._col*tileWidth -xOfset + self._tileOfset[1] +2
            displayY = self._row*tileWidth -yOfset + self._tileOfset[0] +2
            display.blit(self.__rotatedCar,(displayX,displayY))

    # Respawn car on random piece of road.
    def respawn(self,frontArray,backArray):
        x,y = random.randint(2,len(frontArray[0])-3),random.randint(2,len(frontArray)-3)
        while frontArray[y][x] != 0 or backArray[y][x] != 3:
            x,y = random.randint(2,len(frontArray[0])-3),random.randint(2,len(frontArray)-3)
        self._col,self._row = x,y
        frontArray[y][x] = 8
        self.__speed = random.randint(3,6)
        return frontArray
    
import random
import pygame
pygame.init()