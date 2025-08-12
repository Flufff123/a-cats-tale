import asyncio
import pygame
import Navigation
import os
import sys

async def awaitClick(display,colouredPrints,pawPrintTrails,backStack,parentPawPrints,username,levelsUnlocked,newAchievements,basePath,mobileFriendlyOn,popupsBool):
 
    # Load and play background music on a loop.
    tapToPlay = pygame.image.load(os.path.join(basePath,"Assets/Screens/TapToPlay.png"))
    tapToPlay = pygame.transform.smoothscale(tapToPlay, (800,450))
    display.blit(tapToPlay,(0,0))
    pygame.display.update()

    clicked = False
    while clicked == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                clicked = "quit"
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
                pygame.mixer.init()
                pygame.mixer.music.load(os.path.join(basePath,"Assets/Screens/BackgroundMusic.ogg")) # Background music.
                pygame.mixer.music.play(-1) # Loop the music forever.
                clicked = "go"
        await asyncio.sleep(0)

    if clicked == "go":
        await asyncio.sleep(0.1)
        await Navigation.jumpToScreen("LevelSelect",display,colouredPrints,pawPrintTrails,backStack,parentPawPrints,username,levelsUnlocked,newAchievements,basePath,mobileFriendlyOn,popupsBool)
    elif clicked == "quit":
        pygame.quit()
        sys.exit()