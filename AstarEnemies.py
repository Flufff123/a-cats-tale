# Inherits from EnemiesClass and AssetsClass. Move towards player using Astar algorithm.

from EnemiesClass import enemies

class astarEnemies(enemies):
    def __init__(self, visibleOnScreen, col, row, imageFile, soundFile, name, tileWidth, index, xOfset, yOfset, backArray, basePath):
        super().__init__(visibleOnScreen, col, row, imageFile, soundFile, name, tileWidth, index,basePath)
        playerScreenX = 800
        playerScreenY = 225
        # Convert to map‐coordinates
        playerCol =  (xOfset + playerScreenX)//40
        playerRow =  (yOfset + playerScreenY)//40
        self.__route = Astar.astar(self._row,self._col,backArray,playerCol,playerRow)
        self.__healthBar = healthBars()

    # Respawn tick on random grass tile.
    def respawn(self,frontArray,backArray):
        validTile = False
        while validTile == False:
            x,y = random.randint(2,len(frontArray[0])-3),random.randint(3,len(frontArray)-3)
            validTile = True
            for yAdjust in [y-1,y,y+1]:
                for xAdjust in [x-1,x,x+1]:
                    if backArray[yAdjust][xAdjust] not in [1,3]:
                        validTile = False
                        continue
        
        if self.name == "flea":
            frontArray[y][x] = 6
        elif self.name == "tick":
            frontArray[y][x] = 7
        self._col,self._row = x,y
        return frontArray
    
    # Override because must also draw health bar.
    def display(self,tileWidth,xOfset,yOfset,display):
        if self._visibleOnScreen == True:
            displayX = self._col*tileWidth -xOfset +self._tileOfset[1] +2
            displayY = self._row*tileWidth -yOfset +self._tileOfset[0] +2
            display.blit(self._imageFile,(displayX,displayY))
            healthBars.drawBar(display,displayX,displayY,self.__healthBar)
            
    # Collided with player's paw = respawn.
    def checkPawCollision(self,rotatedPaw,pawX,pawY,tileWidth,xOfset,yOfset,frontArray,backArray,fishCount,basePath):
        if self._visibleOnScreen == True:
            pawRect = pygame.Rect(pawX,pawY,rotatedPaw.get_width(),rotatedPaw.get_height())
            selfRect =  pygame.Rect(self._col*tileWidth -xOfset+2,self._row*tileWidth -yOfset+2,36,36)
            if pawRect.colliderect(selfRect):
                frontArray = self.respawn(frontArray,backArray)
                fishCount = healthBars.decreaseBar(self.__healthBar,fishCount)
                dieSound = pygame.mixer.Sound(os.path.join(basePath,"Assets/Enemies/Die.ogg"))
                dieSound.play()
        return frontArray,fishCount

    # Move fleas/ticks using Astar pathfinding towards player.
    def move(self, backArray, display, xOfset, yOfset, frontArray):
        if not self._visibleOnScreen:
            return frontArray

        playerScreenX = display.get_width() // 2
        playerScreenY = display.get_height() // 2

        half = 20

        # If we've accumulated >= one tile of offset, convert those whole tiles into grid movement.
        # This handles the general case (in case speed > 1 pixel/frame in future).
        if abs(self._tileOfset[0]) >= 40 or abs(self._tileOfset[1]) >= 40:
            if abs(self._tileOfset[1]) >= 40:
                steps = int(self._tileOfset[1] // 40) # positive or negative whole steps.
                self._col += steps
                self._tileOfset[1] -= steps * 40
            if abs(self._tileOfset[0]) >= 40:
                steps = int(self._tileOfset[0] // 40)
                self._row += steps
                self._tileOfset[0] -= steps * 40

            # Recompute route from the current integer grid position.
            playerCol = (xOfset + playerScreenX) // 40
            playerRow = (yOfset + playerScreenY) // 40
            # astar expects (row, col, backArray, endCol, endRow) in your codebase
            self.__route = Astar.astar(self._row, self._col, backArray, playerCol, playerRow)

        # If we've got a route, ensure the *next* tile is still valid- but compute A* start
        # Based on the tile the enemy is mostly in (so mid-tile recomputes are correct).
        if len(self.__route) > 1:
            nextCol, nextRow = self.__route[1]

            # Determine the effective "current tile" to use if we need to re-run A*:
            startCol = self._col
            startRow = self._row
            if backArray[nextRow][nextCol] not in (1,3):
                    self.__route = Astar.astar(startRow, startCol, backArray, playerCol, playerRow)
            else:
                if abs(self._tileOfset[1]) > half: # More than halfway across a horizontal tile.
                    if self._tileOfset[1] > 0:
                        startCol += 1
                    else:
                        startCol -= 1
                if abs(self._tileOfset[0]) > half: # More than halfway across a vertical tile.
                    if self._tileOfset[0] > 0:
                        startRow += 1
                    else:
                        startRow -= 1

            # If next tile is out of bounds or invalid, recompute route from the effective tile.
            need_recompute = False
            if not (0 <= nextRow < len(backArray) and 0 <= nextCol < len(backArray[0])):
                need_recompute = True
            else:
                if backArray[nextRow][nextCol] not in [1, 3]:
                    need_recompute = True

            if need_recompute:
                playerCol = (xOfset + playerScreenX) // 40
                playerRow = (yOfset + playerScreenY) // 40
                self.__route = Astar.astar(startRow, startCol, backArray, playerCol, playerRow)

            # If there is still a route, move one pixel towards the next tile, clamping so we never overshoot.
            if len(self.__route) > 1:
                nextCol, nextRow = self.__route[1]

                if nextCol > self._col:
                    target = 40
                    # Add speed. clamp not to exceed target.
                    self._tileOfset[1] = min(self._tileOfset[1] + 2, target)
                elif nextCol < self._col:
                    target = -40
                    self._tileOfset[1] = max(self._tileOfset[1] - 2, target)
                if nextRow > self._row:
                    target = 40
                    self._tileOfset[0] = min(self._tileOfset[0] + 2, target)
                elif nextRow < self._row:
                    target = -40
                    self._tileOfset[0] = max(self._tileOfset[0] - 2, target)

        return frontArray

import Astar
import random
import pygame
pygame.init()
from EnemiesClass import enemies
from HealthBarClass import healthBars
import os
pygame.mixer.init()