'''
In this program:
- User can select a level to play.
- Enter a group code which is validated when they click on a level.
- Unlock levels sequentally.
'''

# Load the current screen background graphic.
def loadAndScaleScreen(name,display,basePath):
    image = pygame.image.load(os.path.join(basePath,"Assets/Screens/")+name+".png")
    scaleFactor = (display.get_width())/(image.get_width())
    image = pygame.transform.smoothscale(image, (int(display.get_width()), int(image.get_height()*scaleFactor)))
    return image

# Loads light and dark images for a button, scales them, and creates a rect for detecting collisions.
def loadAndScaleButton(darkImageName,lightImageName,x,y,display,basePath):
    darkImage = pygame.image.load(os.path.join(basePath,"Assets/Buttons/")+darkImageName+".png")
    lightImage = pygame.image.load(os.path.join(basePath,"Assets/Buttons/")+lightImageName+".png")

    scaleFactor = (display.get_width())/(5*darkImage.get_width())
    darkImage = pygame.transform.smoothscale(darkImage, (int(display.get_width()/5), int(darkImage.get_height()*scaleFactor)))
    lightImage = pygame.transform.smoothscale(lightImage, (int(display.get_width()/5), int(lightImage.get_height()*scaleFactor)))
    imageRect = pygame.Rect(x,y,darkImage.get_width(),darkImage.get_height())
    return darkImage,lightImage,imageRect

# ================================ FUNCTION DEFINITIONS ================================ #
# Handles logic and rendering for the level selection screen.
async def levelSelect(display, colouredPrints, pawPrintTrails, backStack, parentPawPrints, username, levelsUnlocked, newAchievements, basePath, mobileFriendlyOn,popupsBool):

    # Load and scale level buttons.
    screen = loadAndScaleScreen("LevelSelect", display, basePath)

    level1Dark, level1Light, level1Rect = loadAndScaleButton("Level1Dark", "Level1Light", display.get_width() * 0.28, 0.3 * display.get_height(), display, basePath)
    level2Dark, level2Light, level2Rect = loadAndScaleButton("Level2Dark", "Level2Light", display.get_width() * 0.72 - display.get_width() / 5, 0.3 * display.get_height(), display, basePath)
    level3Dark, level3Light, level3Rect = loadAndScaleButton("Level3Dark", "Level3Light", display.get_width() * 0.28, 0.6 * display.get_height(), display, basePath)
    level4Dark, level4Light, level4Rect = loadAndScaleButton("Level4Dark", "Level4Light", display.get_width() * 0.72 - display.get_width() / 5, 0.6 * display.get_height(), display, basePath)

    # Load and scale mobile friendly mode on/off button.
    mobileOn = pygame.image.load(os.path.join(basePath,"Assets/Buttons/MobileOn.png"))
    mobileOff = pygame.image.load(os.path.join(basePath,"Assets/Buttons/MobileOff.png"))
    mobileOn = pygame.transform.smoothscale(mobileOn, (142,32))
    mobileOff = pygame.transform.smoothscale(mobileOff, (int(mobileOn.get_width()),int(mobileOn.get_height())))
    mobileRect = pygame.Rect(29,112,mobileOn.get_width(),mobileOn.get_height())
    if mobileFriendlyOn == True:
        mobileOnOff = mobileOn
    else:
         mobileOnOff = mobileOff

    # Load and scale lock icon.
    lock = pygame.image.load(os.path.join(basePath, "Assets/Buttons/Lock.png"))
    lock = pygame.transform.smoothscale(lock, (150, 150))

    # ================================ GAME LOOP ================================ #
    loop = True
    pygame.display.set_caption("A Cat's Tale")
    counter = 0
    mouseDown = False

    pygame.display.update()

    while loop:

        # ================================ GRAPHICS ================================ #
        display.fill((255, 255, 255))

        # Animate paw print trails.
        for currentTrail in range(0, len(pawPrintTrails)):
            if counter == 20: # Only update prints once every 20 frames.
                pawPrintTrails, parentPawPrints = PawPrints.updatePrints(pawPrintTrails, parentPawPrints, currentTrail, colouredPrints, display)
                counter = 0
            # Draw prints (without updating) every frame.
            pawPrintTrails, parentPawPrints = PawPrints.justDraw(pawPrintTrails, parentPawPrints, currentTrail, colouredPrints, display)
            counter += 1

        display.blit(screen, (0, 0))

        # ================================ EVENTS ================================ #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
                exitType = "Quit"
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
                mouseDown = True
            else:
                mouseDown = False

        # ================================ BUTTONS ================================ #
        mousePos = pygame.mouse.get_pos()

        # Repeat for each level button:
        for level, rect, dark, light in [(1, level1Rect, level1Dark, level1Light),(2, level2Rect, level2Dark, level2Light),(3, level3Rect, level3Dark, level3Light),(4, level4Rect, level4Dark, level4Light)]:
            if rect.collidepoint(mousePos) and mouseDown and (level == 1 or level in levelsUnlocked): # If level clicked and already unlocked:
                loop = False
                exitType = f"Level{level}"
            elif rect.collidepoint(mousePos):
                display.blit(light, (rect.x, rect.y))
            else:
                display.blit(dark, (rect.x, rect.y))
            if level != 1 and level not in levelsUnlocked:
                display.blit(lock, (rect.x, rect.y))

        # Change mobile friendly mode on/off with mouse pos.
        if mobileRect.collidepoint(mousePos) and mouseDown:
            if mobileFriendlyOn == True:
                mobileFriendlyOn = False
                mobileOnOff = mobileOff
                await asyncio.sleep(0.1) # Pause to prevent flicking back to previos option immediately.
            else:
                mobileFriendlyOn = True
                mobileOnOff = mobileOn
                await asyncio.sleep(0.1)
        display.blit(mobileOnOff, (mobileRect.x, mobileRect.y))

        # ================================ END OF GAME LOOP ================================ #
        clock.tick(60)
        pygame.display.update()
        await asyncio.sleep(0)

    # ================================ EXIT AND NAVIGATION ================================ #
    import Navigation
    if exitType == "Quit":
        pygame.quit()
        sys.exit()
    else:
        await Navigation.jumpToScreen(f"PreGameCard{exitType[-1]}", display, colouredPrints, pawPrintTrails, backStack, parentPawPrints, username, levelsUnlocked, newAchievements, basePath, mobileFriendlyOn, popupsBool)

import pygame
pygame.init()
clock = pygame.time.Clock()
import PawPrints
import os
import sys
import asyncio