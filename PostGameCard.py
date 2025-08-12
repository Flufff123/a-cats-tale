'''
In this program:
- Shows post-game card for a level.
- Displays achievements.
- Link button to cats protection website.
- Shows time and fish.
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


async def postGameCard(levelNum,display,colouredPrints,pawPrintTrails,backStack,parentPawPrints,username,levelsUnlocked,newAchievements,basePath,mobileFriendlyOn,popupsBool):

    screenName = "PostGame"+levelNum
    screen = loadAndScaleScreen(screenName,display,basePath)

    helpMoreCatsDark,helpMoreCatsLight,helpMoreCatsRect = loadAndScaleButton("HelpMoreCatsDark","HelpMoreCatsLight",display.get_width()//22,int(display.get_height()*0.85),display,basePath)

    # Load and scale back button.
    backDark = pygame.image.load(os.path.join(basePath,"Assets/Buttons/BackDark.png"))
    backLight = pygame.image.load(os.path.join(basePath,"Assets/Buttons/BackLight.png"))
    scaleFactor = (display.get_width())/(10.5*backDark.get_width())
    backDark = pygame.transform.smoothscale(backDark, (display.get_width()/10.5, backDark.get_height()*scaleFactor))
    backLight = pygame.transform.smoothscale(backLight, (display.get_width()/10.5, backLight.get_height()*scaleFactor))
    backRect = pygame.Rect(display.get_width()-backDark.get_width()-20,5,backDark.get_width()*0.95,backDark.get_height()*0.95)

    font = pygame.font.Font(os.path.join(basePath,"Assets/Screens/Font.ttf"), 30)
    timer = str(newAchievements[0])
    fish  = str(newAchievements[1])
    timeRender = font.render(timer,True,(122,27,114))
    fishRender = font.render(fish,True,(122,27,114))

    # ================================ GAME LOOP ================================ #
    loop = True
    pygame.display.set_caption("A Cat's Tale")
    mouseDown = False
    while loop == True:

        # ================================ BACKGROUND ================================ #
        display.fill((255,255,255))
        display.blit(screen,(0,0))

        display.blit(timeRender,(103,328))
        display.blit(fishRender,(270,328))

        # ================================ EVENTS ================================ #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
                exitType = "Quit"
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN): # If mouse down then a button may have been pressed.
                mouseDown = True
            else:
                mouseDown = False

        # ================================ BUTTONS ================================ #
        mousePos = pygame.mouse.get_pos()

        if helpMoreCatsRect.collidepoint(mousePos) and mouseDown == True: # Help more cats button.
            loop = False
            exitType = "Link" # Flag which screen is next
        elif helpMoreCatsRect.collidepoint(mousePos):
            display.blit(helpMoreCatsLight,(helpMoreCatsRect.x,helpMoreCatsRect.y))
        else:
            display.blit(helpMoreCatsDark,(helpMoreCatsRect.x,helpMoreCatsRect.y))

        if backRect.collidepoint(mousePos) and mouseDown == True and len(backStack) > 1: # Back button.
            loop = False
            exitType = "Back" # Flag which screen is next
        elif backRect.collidepoint(mousePos):
            display.blit(backLight,(backRect.x,backRect.y))
        else:
            display.blit(backDark,(backRect.x,backRect.y))
        
        # ================================ END OF GAME LOOP ================================ #
        clock.tick(60)
        pygame.display.update()
        await asyncio.sleep(0)

    import Navigation
    newAchievements = []
    if exitType == "Link":
        import webbrowser
        webbrowser.open("https://www.cats.org.uk/adopt-a-cat/find-a-cat")
        backStack.pop(len(backStack)-1) # Remove game and pregame from stack
        backStack.pop(len(backStack)-1)
        await Navigation.backScreen(display,colouredPrints,pawPrintTrails,backStack,parentPawPrints,username,levelsUnlocked,newAchievements,basePath,mobileFriendlyOn,popupsBool)
    if exitType == "Quit":
        pygame.quit()
        sys.exit()
    elif exitType == "Back":
        backStack.pop(len(backStack)-1) # Remove game and pregame from stack
        backStack.pop(len(backStack)-1)
        await Navigation.backScreen(display,colouredPrints,pawPrintTrails,backStack,parentPawPrints,username,levelsUnlocked,newAchievements,basePath,mobileFriendlyOn,popupsBool)

import pygame
pygame.init()
clock = pygame.time.Clock()
import os
import sys
import asyncio