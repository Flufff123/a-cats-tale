'''
In this program:
- Shows pre-game card.
- Button to start actual game.
'''

# Load the current screen background graphic.
def loadAndScaleScreen(name,display,basePath):
    image = pygame.image.load(os.path.join(basePath,"Assets/Screens/")+name+".png")
    scaleFactor = (display.get_width())/(image.get_width())
    image = pygame.transform.smoothscale(image, (display.get_width(), image.get_height()*scaleFactor))
    return image

# Load and scale light and dark centre button graphics, and generate a rect in the same position.
def loadAndScaleButton(darkImageName,lightImageName,x,y,display,basePath):
    darkImage = pygame.image.load(os.path.join(basePath,"Assets/Buttons/")+darkImageName+".png")
    lightImage = pygame.image.load(os.path.join(basePath,"Assets/Buttons/")+lightImageName+".png")
    scaleFactor = (display.get_width())/(2.3*darkImage.get_width())
    darkImage = pygame.transform.smoothscale(darkImage, (display.get_width()/2.3, darkImage.get_height()*scaleFactor))
    lightImage = pygame.transform.smoothscale(lightImage, (display.get_width()/2.3, lightImage.get_height()*scaleFactor))
    imageRect = pygame.Rect(x,y,darkImage.get_width(),darkImage.get_height())
    return darkImage,lightImage,imageRect

async def preGameCard(levelNum, display, colouredPrints, pawPrintTrails, backStack, parentPawPrints, username, levelsUnlocked, newAchievements, basePath, mobileFriendlyOn, popupsBool):

    screenName = "PreGame" + levelNum
    screen = loadAndScaleScreen(screenName, display, basePath)

    letsGoDark, letsGoLight, letsGoRect = loadAndScaleButton("LetsGoDark", "LetsGoLight", display.get_width() // 22, int(display.get_height() * 0.85), display, basePath)

    # Load and scale back button.
    backDark = pygame.image.load(os.path.join(basePath,"Assets/Buttons/BackDark.png"))
    backLight = pygame.image.load(os.path.join(basePath,"Assets/Buttons/BackLight.png"))
    scaleFactor = (display.get_width())/(10.5*backDark.get_width())
    backDark = pygame.transform.smoothscale(backDark, (display.get_width()/10.5, backDark.get_height()*scaleFactor))
    backLight = pygame.transform.smoothscale(backLight, (display.get_width()/10.5, backLight.get_height()*scaleFactor))
    backRect = pygame.Rect(display.get_width()-backDark.get_width()-20,5,backDark.get_width()*0.95,backDark.get_height()*0.95)

    # ================================ GAME LOOP ================================ #
    loop = True
    pygame.display.set_caption("A Cat's Tale")
    mouseDown = False

    while loop:

        display.fill((255, 255, 255))
        display.blit(screen, (0, 0))

        # ================================ EVENTS ================================ #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
                exitType = "Quit"
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
                mouseDown = True
            else:
                mouseDown = False

        # ================================ BUTTONS ================================ #
        mousePos = pygame.mouse.get_pos()

        # Lets Go button.
        if letsGoRect.collidepoint(mousePos) and mouseDown:
            loop = False
            exitType = "PlayGame"
        elif letsGoRect.collidepoint(mousePos):
            display.blit(letsGoLight, (letsGoRect.x, letsGoRect.y))
        else:
            display.blit(letsGoDark, (letsGoRect.x, letsGoRect.y))

        # Back button.
        if backRect.collidepoint(mousePos) and mouseDown and len(backStack) > 1:
            loop = False
            exitType = "Back"
        elif backRect.collidepoint(mousePos):
            display.blit(backLight, (backRect.x, backRect.y))
        else:
            display.blit(backDark, (backRect.x, backRect.y))

        clock.tick(60)
        pygame.display.update()
        await asyncio.sleep(0)

    # ================================ END OF GAME LOOP ================================ #
    import Navigation

    if exitType == "PlayGame":
        await Navigation.jumpToScreen("Level" + levelNum, display, colouredPrints, pawPrintTrails, backStack, parentPawPrints, username, levelsUnlocked, newAchievements, basePath, mobileFriendlyOn, popupsBool)
    elif exitType == "Quit":
        pygame.quit()
        sys.exit()
    elif exitType == "Back":
        await Navigation.backScreen(display, colouredPrints, pawPrintTrails, backStack, parentPawPrints, username, levelsUnlocked, newAchievements, basePath, mobileFriendlyOn,popupsBool)

import pygame
pygame.init()
clock = pygame.time.Clock()
import os
import sys
import asyncio