'''
In this program:
- Calls the navigation program, which starts the game.
''' 

import os
import asyncio
basePath = os.path.dirname(__file__) # Gets the directory of the current script.

import pygame
pygame.init()

import PawPrints # Handles paw print assets and animation.
import AwaitClick

# Set up display window.
display = pygame.display.set_mode((800,450))

pawPrintPink = PawPrints.loadPawPrint("PawPrintPink",display,basePath)

# Pass in an array containing each coloured print instead of each coloured print individually.
colouredPrints = [pawPrintPink]

# Reset paw print trails andreturn arrays containing their info.
pawPrintTrails,parentPawPrints,counter = PawPrints.resetPawPrints(colouredPrints,display)

# Initialize game state variables.
backStack = [] # Keeps track of navigation history.
username = None # Not initially logged in.
groupCode = None # Not initially part of a group.
levelsUnlocked = [1] # Initially only level 1 unlocked.
newAchievements = [] # No games played so no achievements.
mobileFriendlyOn = False
popupsBool = False

#async def main(display,colouredPrints,pawPrintTrails,backStack,parentPawPrints,username,groupCode,levelsUnlocked,newAchievements,basePath,mobileFriendlyOn,popupsBool):
async def main(display,colouredPrints,pawPrintTrails,backStack,parentPawPrints,username,levelsUnlocked,newAchievements,basePath,mobileFriendlyOn,popupsBool):
    loop = True
    while loop:
        await AwaitClick.awaitClick(display,colouredPrints,pawPrintTrails,backStack,parentPawPrints,username,levelsUnlocked,newAchievements,basePath,mobileFriendlyOn,popupsBool)
        await asyncio.sleep(0)

asyncio.run(main(display,colouredPrints,pawPrintTrails,backStack,parentPawPrints,username,levelsUnlocked,newAchievements,basePath,mobileFriendlyOn,popupsBool))
pygame.quit()