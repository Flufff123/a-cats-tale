# Inherits from StaticEnemiesClass, EnemiesClass, and AssetsClass. No movement during game.

from StaticEnemiesClass import staticEnemies

class lillies(staticEnemies):
    def __init__(self, visibleOnScreen, col, row, imageFileA, soundFile, name, tileWidth, index,basePath, imageFileB):
        super().__init__(visibleOnScreen, col, row, imageFileA, soundFile, name, tileWidth, index,basePath, imageFileB)