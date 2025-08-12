'''
This file simple handles navigation between screens.
'''

import asyncio

async def backScreen(display,colouredPrints,pawPrintTrails,backStack,parentPawPrints,username,levelsUnlocked,newAchievements,basePath,mobileFriendlyOn,popupsBool):
    backStack.pop(len(backStack)-1) # Remove last screen from backStack.
    screenName = backStack[len(backStack)-1] # Next screen will be the new last one in backStack.
    backStack.pop(len(backStack)-1) # Now remove this new current screen since it will be reappended in jumpToScreen.
    await jumpToScreen(screenName,display,colouredPrints,pawPrintTrails,backStack,parentPawPrints,username,levelsUnlocked,newAchievements,basePath,mobileFriendlyOn,popupsBool)

async def jumpToScreen(screenName,display,colouredPrints,pawPrintTrails,backStack,parentPawPrints,username,levelsUnlocked,newAchievements,basePath,mobileFriendlyOn,popupsBool):

    params = [display,colouredPrints,pawPrintTrails,backStack,parentPawPrints,username,levelsUnlocked,newAchievements,basePath,mobileFriendlyOn,popupsBool] # Pass in list of params = quicker + tidier.
    backStack.append(screenName)
    if screenName == "LevelSelect":
        import LevelSelect
        await LevelSelect.levelSelect(*params)
    elif screenName == "Level1":
        import Game
        await Game.game("1",*params)
    elif screenName == "Level2":
        import Game
        await Game.game("2",*params)
    elif screenName == "Level3":
        import Game
        await Game.game("3",*params)
    elif screenName == "Level4":
        import Game
        await Game.game("4",*params)
    elif screenName == "PostGameCard1":
        import PostGameCard
        await PostGameCard.postGameCard("1",*params)
    elif screenName == "PostGameCard2":
        import PostGameCard
        await PostGameCard.postGameCard("2",*params)
    elif screenName == "PostGameCard3":
        import PostGameCard
        await PostGameCard.postGameCard("3",*params)
    elif screenName == "PostGameCard4":
        import PostGameCard
        await PostGameCard.postGameCard("4",*params)
    elif screenName == "PreGameCard1":
        import PreGameCard
        await PreGameCard.preGameCard("1",*params)
    elif screenName == "PreGameCard2":
        import PreGameCard
        await PreGameCard.preGameCard("2",*params)
    elif screenName == "PreGameCard3":
        import PreGameCard
        await PreGameCard.preGameCard("3",*params)
    elif screenName == "PreGameCard4":
        import PreGameCard
        await PreGameCard.preGameCard("4",*params)
    elif screenName == "Quit":
        pygame.quit()
    else:
        pygame.quit() # If an invalid screenName is called, te program quits instead of showing an error message.

import pygame
pygame.init()