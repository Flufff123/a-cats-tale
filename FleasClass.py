# Inherits from EnemiesClass and AssetsClass. Move towards player using Astar algorithm.

from AstarEnemies import astarEnemies

class fleas(astarEnemies):
    def __init__(self, visibleOnScreen, col, row, imageFile, soundFile, name, tileWidth, index, xOfset, yOfset, backArray, basePath):
        super().__init__(visibleOnScreen, col, row, imageFile, soundFile, name, tileWidth, index, xOfset, yOfset, backArray, basePath)