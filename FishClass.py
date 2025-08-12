# Inherits from AssetsClass. Respawn once collected.

from CollectablesClass import collectables

class fishes(collectables):
    # Respawn fish on random grass tile.
    def respawn(self,frontArray,backArray):
        x,y = random.randint(2,len(frontArray[0])-3),random.randint(2,len(frontArray)-3)
        while frontArray[y][x] != 0 or not(backArray[y][x] == 1 or backArray[y][x] == 3):
            x,y = random.randint(2,len(frontArray[0])-3),random.randint(2,len(frontArray)-3)
        
        if frontArray[y][x] != 0:
            self.respawn(frontArray,backArray)
        frontArray[y][x] = 3
        return x,y,frontArray

import random