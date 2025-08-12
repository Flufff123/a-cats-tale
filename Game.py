'''
In this program:
- Handles player movement.
- Handles collisions.
- Updates display.
- Runs the game itself!
'''

# Returns initial tile coordinates for all tiles of the current tileType in the frontArray.
def findStartPos(tileType,frontArray):
    tiles = []
    for y in range(0,len(frontArray)):
        for x in range(0,len(frontArray[y])):
            if frontArray[y][x] == tileType:
                tiles.append([x,y])
    return tiles

# Unstick player if overlapping with a collision tile.
def pushOut(xOfset,yOfset,rotatedCat,rockMask,waterMask,backArray,tileWidth,display,catMask):
    # Try pushing out in all directions, up to 20 pixels.
    for nudgeAmount in range(1,21): # Max 20 pixels.
        # Try each direction.
        for dx,dy in [(nudgeAmount,0),(-nudgeAmount,0),(0,nudgeAmount),(0,-nudgeAmount)]:
            tempX = xOfset + dx
            tempY = yOfset + dy
            collision = checkCollision(tempX,tempY,rotatedCat,rockMask,waterMask,backArray,tileWidth,display,catMask) # Collision in this new position?
            if collision == "None":
                return tempX,tempY # Found safe position.
    return xOfset,yOfset # Couldn’t push out, remain stuck.

# Checks for collisions at a future position using tile masks for greater precision.
def checkCollision(futureXofset,futureYofset,rotatedCat,rockMask,waterMask,backArray,tileWidth,display,catMask):
    catXofset = (display.get_width() - rotatedCat.get_width()) // 2
    catYofset = (display.get_height() - rotatedCat.get_height()) // 2

    topRow = round(max(0,futureYofset//tileWidth)) # Determines rows/cols of tiles currrnetly visible on screen.
    botRow = round(min(len(backArray),topRow+ display.get_height()//tileWidth +4))
    leftCol = round(max(0,futureXofset//tileWidth))
    rightCol = round(min(len(backArray[0]),leftCol+ display.get_width()//tileWidth +2))

    for yIndex in range(topRow,botRow): # Iterate through visible tiles and return colliding tileType if there is one.
        for xIndex in range(leftCol,rightCol):
            tile = backArray[yIndex][xIndex]
            x = xIndex*tileWidth -futureXofset
            y = yIndex*tileWidth -futureYofset
            offset = (int(x-catXofset),int(y-catYofset))
            if tile == 2 and catMask.overlap(rockMask,offset):
                return "Rock"
            if tile == 4 and catMask.overlap(waterMask,offset):
                return "Water"

    return "None"

# Loads light and dark images for a button, scales them, and creates a rect for detecting collisions.
def loadAndScaleButton(darkImageName,lightImageName,x,y,display,basePath):
    darkImage = pygame.image.load(os.path.join(basePath,"Assets/Buttons/")+darkImageName+".png")
    lightImage = pygame.image.load(os.path.join(basePath,"Assets/Buttons/")+lightImageName+".png")
    scaleFactor = (display.get_width())/(5*darkImage.get_width())
    darkImage = pygame.transform.smoothscale(darkImage,(int(display.get_width()/5),int(darkImage.get_height()*scaleFactor))) # Smoothscale is reduced pixelisation, preserving quality.
    lightImage = pygame.transform.smoothscale(lightImage,(int(display.get_width()/5),int(lightImage.get_height()*scaleFactor)))
    imageRect = pygame.Rect(x,y,darkImage.get_width(),darkImage.get_height())
    return darkImage,lightImage,imageRect

# Loads a tile image and scales it to 40x40 pixels.
def loadAndScaleTile(imageName,basePath):
    image = pygame.image.load(os.path.join(basePath,"Assets/Tiles/")+imageName+".png").convert_alpha() # convert_alpha() allows for transparency.
    scaledImage = pygame.transform.smoothscale(image,(40,40))
    return scaledImage

# Rotates the cat as it moves, and rotates its paw as it swipes.
def rotateCat(angle,cat,paw,swipeTimer):
    rotatedCat = pygame.transform.rotozoom(cat,-angle,0.07) # Rotozoom = rotate + zoom!
    angle -= swipeTimer # Paw rotation is based on cat angle and adjusted using the swipeTimer.
    rotatedPaw = pygame.transform.rotozoom(paw,-angle,0.125) # negative angle = clockwise.
    return rotatedCat,rotatedPaw

# Load the current screen background graphic.
def loadAndScaleScreen(name,display,basePath):
    image = pygame.image.load(os.path.join(basePath,"Assets/Screens/")+name+".png")
    scaleFactor = (display.get_width())/(image.get_width())
    image = pygame.transform.smoothscale(image,(int(display.get_width()),int(image.get_height()*scaleFactor)))
    return image

async def game(levelNum, display, colouredPrints, pawPrintTrails, backStack, parentPawPrints, username, levelsUnlocked, newAchievements, basePath, mobileFriendlyOn, popupsBool):

    # Load sleeping cat graphic.
    sleepingCat = pygame.image.load(os.path.join(basePath,"Assets/Screens/SleepingCat")+levelNum+".png").convert_alpha()
    sleepingCat = pygame.transform.smoothscale(sleepingCat,(210,140))

    # Load end game screens.
    gameOver = loadAndScaleScreen("GameOver", display, basePath)
    levelComplete = loadAndScaleScreen("LevelComplete", display, basePath)

    # Load and scale game element.
    gameBar = pygame.image.load(os.path.join(basePath, "Assets/Screens/GameBar.png"))
    gameBar = pygame.transform.smoothscale(gameBar, (380, 45))

    # Sound and gameplay variables.
    itemCount = 0 # Initially no items collected.
    meow = pygame.mixer.Sound(os.path.join(basePath, "Assets/Screens/Meow.ogg"))

    fishCount = 5 # Initial count of collectible fishies!
    mobileBonus = 20 # Mobile firendly is more difficult so time for fish to deplete can be increased to reduce difficulty.

    # Load fonts.
    font = pygame.font.Font(os.path.join(basePath, "Assets/Screens/BoldFont.ttf"), 30)
    largeFont = pygame.font.Font(os.path.join(basePath, "Assets/Screens/BoldFont.ttf"), 40)

    # Load and scale back button.
    backDark = pygame.image.load(os.path.join(basePath, "Assets/Buttons/BackDark.png"))
    backLight = pygame.image.load(os.path.join(basePath, "Assets/Buttons/BackLight.png"))
    scaleFactor = (display.get_width()) / (10.5 * backDark.get_width())
    backDark = pygame.transform.smoothscale(backDark, (int(display.get_width() / 10.5), int(backDark.get_height() * scaleFactor)))
    backLight = pygame.transform.smoothscale(backLight, (int(display.get_width() / 10.5), int(backLight.get_height() * scaleFactor)))
    backRect = pygame.Rect(display.get_width() - backDark.get_width() - 20, 5, backDark.get_width() * 0.95, backDark.get_height() * 0.95)

    # Position and movement variables.
    xOfset = 0 # Grid offset for horizontal movement.
    yOfset = 0 # Grid offset for vertical movement.
    swipePower = 10 # Limited swipes for increased difficulty.
    angle = 180 # Initial orientation of the cat and paw
    tileWidth = 40
    fishTimer = 0 # Rate of depete of player's fish.
    endTimer = 300 # End game popup display timer.
    swiping = False
    horizontalDirection = "None" # Lats player movement was neither left nor right.
    verticalDirection = "None" # Last player movement was neither up nor down.
    popups = [] # List of popups currently active (so each is processed in turn).
    activePopup = None # No popups currently active (visiblw on screen).

    # Load level-specific map and cat assets.
    if levelNum == "1":
        backArray = LevelArrays.backArray1()
        frontArray = LevelArrays.frontArray1()
        cat = pygame.image.load(os.path.join(basePath, "Assets/Cats/Amber.png")).convert_alpha()
        paw = pygame.image.load(os.path.join(basePath, "Assets/Cats/AmberPaw.png")).convert_alpha()
    elif levelNum == "2":
        backArray = LevelArrays.backArray2()
        frontArray = LevelArrays.frontArray2()
        cat = pygame.image.load(os.path.join(basePath, "Assets/Cats/Ollie.png")).convert_alpha()
        paw = pygame.image.load(os.path.join(basePath, "Assets/Cats/OlliePaw.png")).convert_alpha()
    elif levelNum == "3":
        backArray = LevelArrays.backArray3()
        frontArray = LevelArrays.frontArray3()
        cat = pygame.image.load(os.path.join(basePath, "Assets/Cats/Misty.png")).convert_alpha()
        paw = pygame.image.load(os.path.join(basePath, "Assets/Cats/MistyPaw.png")).convert_alpha()
    elif levelNum == "4":
        backArray = LevelArrays.backArray4()
        frontArray = LevelArrays.frontArray4()
        cat = pygame.image.load(os.path.join(basePath, "Assets/Cats/Igor.png")).convert_alpha()
        paw = pygame.image.load(os.path.join(basePath, "Assets/Cats/IgorPaw.png")).convert_alpha()

    # Load nd scale mobile movement asset.
    mobileBack = pygame.image.load(os.path.join(basePath, "Assets/Buttons/MobileBack.png")).convert_alpha()
    mobileBack = pygame.transform.smoothscale(mobileBack, (200, 200))
    mobileFront = pygame.image.load(os.path.join(basePath, "Assets/Buttons/MobileFront.png")).convert_alpha()
    mobileFront = pygame.transform.smoothscale(mobileFront, (100, 100))
    mobileFrontCentre = (650, 200)

    # Find starting positions for different entities on the front layer.
    fishStartPos = findStartPos(3, frontArray)
    treatStartPos = findStartPos(4, frontArray)
    catNeedStartPos = findStartPos(5, frontArray)
    fleaStartPos = findStartPos(6, frontArray)
    tickStartPos = findStartPos(7, frontArray)
    carStartPos = findStartPos(8, frontArray)
    dogStartPos = findStartPos(9, frontArray)
    lillyStartPos = findStartPos(10, frontArray)

    # Initialize fish assets based on start positions (dynamic generation of objects):
    # There are a different number of objects in each level.
    fishAssets = []
    index = 1
    for asset in fishStartPos:
        fish = fishes(True, asset[0], asset[1], os.path.join(basePath, "Assets/Collectables/Fish.png"),os.path.join(basePath, "Assets/Collectables/Fish.ogg"), "fish", tileWidth, index)
        fishAssets.append(fish)
        index += 1

    # Initialize treat assets with random image (4 options) for variety.
    treatAssets = []
    index = 1
    for asset in treatStartPos:
        type = str(random.randint(1, 4))
        treat = treats(True, asset[0], asset[1], os.path.join(basePath, "Assets/Collectables/Treats") + type + ".png",os.path.join(basePath, "Assets/Collectables/SpeedBoost.ogg"), "treat", tileWidth, index)
        treatAssets.append(treat)
        index += 1

    # Initialize cat needs assets.
    catNeedAssets = []
    index = 1
    for asset in catNeedStartPos:
        item = catNeeds(True, asset[0], asset[1], os.path.join(basePath, "Assets/Collectables/Item") + str(index) + ".png",os.path.join(basePath, "Assets/Collectables/ItemCollect.ogg"), "catNeed", tileWidth, index, basePath)
        catNeedAssets.append(item)
        index += 1

    # Initialize enemy assets: fleas, ticks, cars, dogs, lillies.
    fleaAssets = []
    for asset in fleaStartPos:
        item = fleas(True, asset[0], asset[1], os.path.join(basePath, "Assets/Enemies/Enemy4.png"),os.path.join(basePath, "Assets/Enemies/Enemy4Sound.ogg"), "flea", tileWidth, 4, xOfset, yOfset, backArray, basePath)
        fleaAssets.append(item)

    tickAssets = []
    for asset in tickStartPos:
        item = ticks(True, asset[0], asset[1], os.path.join(basePath, "Assets/Enemies/Enemy3.png"),os.path.join(basePath, "Assets/Enemies/Enemy3Sound.ogg"), "tick", tileWidth, 3, xOfset, yOfset, backArray, basePath)
        tickAssets.append(item)

    carAssets = []
    for asset in carStartPos:
        item = cars(True, asset[0], asset[1], os.path.join(basePath, "Assets/Enemies/Enemy1.png"),os.path.join(basePath, "Assets/Enemies/Enemy1Sound.ogg"), "car", tileWidth, 1, basePath)
        carAssets.append(item)

    dogAssets = []
    for asset in dogStartPos:
        item = dogs(True, asset[0], asset[1], os.path.join(basePath, "Assets/Enemies/Enemy2a.png"),os.path.join(basePath, "Assets/Enemies/Enemy2Sound.ogg"), "dog", tileWidth, 2, basePath, os.path.join(basePath, "Assets/Enemies/Enemy2b.png"))
        dogAssets.append(item)

    lillyAssets = []
    for asset in lillyStartPos:
        item = lillies(True, asset[0], asset[1], os.path.join(basePath, "Assets/Enemies/Enemy5a.png"),os.path.join(basePath, "Assets/Enemies/Enemy5Sound.ogg"), "lilly", tileWidth, 5, basePath, os.path.join(basePath, "Assets/Enemies/Enemy5b.png"))
        lillyAssets.append(item)

    # Load tiles for environment. Only need rock and water masks because player only detects collsisions with these tiles.
    road = loadAndScaleTile("Road", basePath)
    rock = loadAndScaleTile("Rock", basePath)
    rockMask = pygame.mask.from_surface(rock)
    water3 = loadAndScaleTile("Water1", basePath)
    water4 = loadAndScaleTile("Water2", basePath)
    waterMask = pygame.mask.from_surface(water3)

    # Tree and flower tiles, scaled to tileWidth.
    treeImage = pygame.image.load(os.path.join(basePath, "Assets/Tiles/Tree.png"))
    tree = pygame.transform.smoothscale(treeImage, (tileWidth * 2, tileWidth * 3))

    flowerImage = pygame.image.load(os.path.join(basePath, "Assets/Tiles/Flowers.png")).convert_alpha()
    flower = pygame.transform.smoothscale(flowerImage, (tileWidth, tileWidth))

    swipeSound = pygame.mixer.Sound(os.path.join(basePath, "Assets/Cats/Swipe.ogg"))
    waterTimer = 0
    swipeTimer = -100

    # Initialize rotated cat and paw and cat mask.
    rotatedCat, rotatedPaw = rotateCat(angle, cat, paw, swipeTimer)
    catMask = pygame.mask.from_surface(rotatedCat)

    # ================================ GAME LOOP ================================ #
    rowsOnScreen = display.get_height() // tileWidth + 4 # +4 buffer for partial tiles.
    colsOnScreen = display.get_width() // tileWidth + 2 # +2 buffer for partial tiles.
    loop = True # Game ends when loop = False.
    pygame.display.set_caption("A Cat's Tale")

    mouseDown = False
    horizontalDrag = 0 # Player maintains small horizontal momentum when they stop moving.
    verticalDrag = 0 # Player maintains small vertical momentum when they stop moving.
    if mobileFriendlyOn:
        startSpeed = 5 # Pixels/frame cat can move.
    else:
        startSpeed = 6
    speed = startSpeed
    spaceDown = False
    await asyncio.sleep(0.5)
    meow.play() # Meow signifies start of game!

    previousTime = time.time() # Track frame-to-frame time for delta calculation.
    accumulated = 0 # Total unpaused seconds.
    currentTime = 0 # Displayed integer time.

    while loop == True:

        # Accumulated time management.
        now = time.time() # Current time.
        delta = now - previousTime
        previousTime = now
        await asyncio.sleep(0)  
        accumulated += delta

        currentTime = int(accumulated)



        # ================================ EVENTS ================================ #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
                exitType = "Quit"
        
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
                mouseDown = True
            elif event.type in (pygame.MOUSEBUTTONUP, pygame.FINGERUP):
                mouseDown = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    spaceDown = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    spaceDown = False

        if mobileFriendlyOn:
            try:
                x = int(event.x * 800)
                y = int(event.y * 450)
                mousePos = (x,y)
            except:
                mousePos = pygame.mouse.get_pos()
        else:
            mousePos = pygame.mouse.get_pos()

        # ===================== Player Movement ===================== #
        preXofset = 0 # Temp tile offsets for movement.
        preYofset = 0

        if mobileFriendlyOn ==  False: # Normal (arrow key) movement enabled.
            keys = pygame.key.get_pressed()

            # Horizontal movement.
            if keys[pygame.K_LEFT]:
                horizontalDirection = "left" # Directions sed to rotate cat.
                horizontalDrag = 5 # Preserve momnentum when stopping.
                preXofset -= speed
            if keys[pygame.K_RIGHT]:
                horizontalDirection = "right"
                horizontalDrag = 5
                preXofset += speed

            # Gradually reduce horizontal drag if no horizontal key pressed.
            if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]) and horizontalDrag != 0:
                horizontalDrag *= 0.75
                if horizontalDrag < 0.1:
                    horizontalDrag = 0
                if horizontalDirection == "left":
                    preXofset -= horizontalDrag
                elif horizontalDirection == "right":
                    preXofset += horizontalDrag

            # Vertical movement.
            if keys[pygame.K_UP]:
                verticalDirection = "up"
                verticalDrag = 5
                preYofset -= speed
            if keys[pygame.K_DOWN]:
                verticalDirection = "down"
                verticalDrag = 5
                preYofset += speed

            # Gradually reduce vertical drag if no vertical key pressed.
            if not (keys[pygame.K_UP] or keys[pygame.K_DOWN]) and verticalDrag != 0:
                verticalDrag *= 0.75
                if verticalDrag < 0.1:
                    verticalDrag = 0
                if verticalDirection == "up":
                    preYofset -= verticalDrag
                elif verticalDirection == "down":
                    preYofset += verticalDrag
        else:
            # Mobile-friendly movement.
            if mouseDown:
                dx = mousePos[0] - 700 # Calc (squared) straight-line dist between mouse and centre of mobile control circle.
                dy = mousePos[1] - 250
                distSquared = dx * dx + dy * dy

                if distSquared < 10000: # If within 100 pix of mobile control centre, player is moving. Else they are swiping/closing a popup.
                    mobileFrontCentre = (mousePos[0] - 50, mousePos[1] - 50)
                    if mobileFrontCentre[0] > 655:
                        horizontalDirection = "right"
                        horizontalDrag = 5
                        preXofset += speed
                    elif mobileFrontCentre[0] < 645:
                        horizontalDirection = "left"
                        horizontalDrag = 5
                        preXofset -= speed
                    if mobileFrontCentre[1] > 205:
                        verticalDirection = "down"
                        verticalDrag = 5
                        preYofset += speed
                    elif mobileFrontCentre[1] < 195:
                        verticalDirection = "up"
                        verticalDrag = 5
                        preYofset -= speed
            else:
                # Gradually reduce horizontal/vertical momentum if no horizontal/vertical keys pressed.
                horizontalDrag *= 0.75
                if horizontalDrag < 0.1:
                    horizontalDrag = 0
                if horizontalDirection == "left":
                    preXofset -= horizontalDrag
                elif horizontalDirection == "right":
                    preXofset += horizontalDrag

                verticalDrag *= 0.75
                if verticalDrag < 0.1:
                    verticalDrag = 0
                if verticalDirection == "up":
                    preYofset -= verticalDrag
                elif verticalDirection == "down":
                    preYofset += verticalDrag

        # Attempt horizontal movement and check collisions.
        tempXofset = xOfset + preXofset
        horizontalCollision = checkCollision(tempXofset, yOfset, rotatedCat, rockMask, waterMask, backArray, tileWidth, display, catMask)
        if horizontalCollision == "None":
            xOfset = tempXofset # Only adjust actual offsets of tiles if no collisions

        # Attempt vertical movement and check collisions.
        tempYofset = yOfset + preYofset
        verticalCollision = checkCollision(xOfset, tempYofset, rotatedCat, rockMask, waterMask, backArray, tileWidth, display, catMask)
        if verticalCollision == "None":
            yOfset = tempYofset

        # Final collision check at new position, push out if stuck.
        finalCollision = checkCollision(xOfset, yOfset, rotatedCat, rockMask, waterMask, backArray, tileWidth, display, catMask)
        if finalCollision != "None":
            xOfset, yOfset = pushOut(xOfset, yOfset, rotatedCat, rockMask, waterMask, backArray, tileWidth, display, catMask)

        # Adjust rotation angle of cat based on movement direction.
        if (preXofset != 0 and horizontalCollision == "None") or (preYofset != 0 and verticalCollision == "None"):
            angle = math.degrees(math.atan2(preYofset, preXofset)) - 90

        # Reduce speed gradually if above normal speed.
        if mobileFriendlyOn and speed > 8: # Booster speed for mobile friendly is slower.
            speed = 8
        if speed > startSpeed:
            speed -= 0.012

        # ================================ RENDER FRONT & BACK ARRAYS ================================ #
        display.fill((0, 0, 0)) # Clear screen with black

        # Calculate visible tile range for optimization.
        topRow = round(max(0, yOfset // tileWidth))
        botRow = round(min(len(backArray), topRow + rowsOnScreen))
        leftCol = round(max(0, xOfset // tileWidth))
        rightCol = round(min(len(backArray[0]), leftCol + colsOnScreen))

        # Render background tiles within visible range.
        for yIndex in range(topRow, botRow):
            for xIndex in range(leftCol, rightCol):
                x = xIndex * tileWidth - xOfset
                y = yIndex * tileWidth - yOfset
                tile = backArray[yIndex][xIndex]
                if tile != 0:
                    if tile == 1: # Grass.
                        # Draw background tiles based on the backArray tile type.
                        pygame.draw.rect(display,(100,200,100),pygame.Rect(x,y,tileWidth,tileWidth)) # Grass tile.
                    elif tile == 2: # Rock tile.
                        display.blit(rock,(x,y))
                    elif tile == 3: # Road tile.
                        display.blit(road,(x,y))
                    elif tile == 4: # Water tile, toggling between two water images for animation.
                        if waterTimer > 20:
                            display.blit(water4,(x,y))
                        else:
                            display.blit(water3,(x,y))

        waterTimer += 1 # Water tile animation timer.
        if waterTimer == 40:
            waterTimer = 0

        fishTimer += 1
        if fishTimer == 300 + mobileBonus:
            fishTimer = 0
            if fishCount > 1:
                fishCount -= 1 # Decrease fish count over time.
            else:
                fishCount = 0

        # ================================ SWIPE CONTROLS ================================ #
        if mouseDown == True or spaceDown == True:
            # Calculate squared distance from the center point (700, 250) to the mouse position.
            dx = mousePos[0] - 700
            dy = mousePos[1] - 250
            distSquared = dx * dx + dy * dy

            pawX = display.get_width()//2 - rotatedPaw.get_width()//2
            pawY = display.get_height()//2 - rotatedPaw.get_height()//2
            swiping = True
            # Only allow swipe if distance threshold and swipePower conditions are met.
            if ((distSquared > 10000 and mobileFriendlyOn == True) or mobileFriendlyOn == False) and round(swipePower) >= 1:
                if swipeTimer == -100: # Swipe starting angle.
                    swipeTimer = -90
                    swipePower -= 0.5 # Reduce swipe power when swipe starts.
                    swipeSound.play()
                elif swipeTimer > 90: # Swipe max angle reached, reset.
                    swipeTimer = -100
                elif swipeTimer <= 90:
                    swipeTimer += 20 # Increase swipe angle incrementally.

                pawX = display.get_width()//2 - rotatedPaw.get_width()//2
                pawY = display.get_height()//2 - rotatedPaw.get_height()//2
                display.blit(rotatedPaw, (pawX, pawY))  # Draw rotated paw.
                mobileFrontCentre = (650, 200)  # Reset mobile control center.
                # Calculate position to draw the paw image at screen center.
            elif mobileFriendlyOn == True:
                swiping = False
        else:
            swiping = False
            mobileFrontCentre = (650, 200)

        # ================================ RENDER CAT ================================ #
        # Rotate cat and paw images according to swipe angle and timer.
        rotatedCat, rotatedPaw = rotateCat(angle, cat, paw, swipeTimer)
        catMask = pygame.mask.from_surface(rotatedCat)  # Generate mask for collision detection.

        # Draw rotated cat at center screen.
        catX = display.get_width()//2 - rotatedCat.get_width()//2
        catY = display.get_height()//2 - rotatedCat.get_height()//2
        display.blit(rotatedCat, (catX, catY))

        # ================================ PROCESS COLLECTABLES & ENEMIES ================================ #
        for fishAsset in fishAssets:
            fishAsset.checkVisibleOnScreen(topRow, botRow, leftCol, rightCol)
            fishAsset.display(tileWidth, xOfset, yOfset, display)
            # Check collision and update frontArray, fishCount, speed, and itemCount accordingly.
            frontArray, fishCount, speed, itemCount,fishAssets, treatAssets = fishAsset.checkCollision(catMask, catX, catY, tileWidth, xOfset, yOfset, frontArray, backArray, fishCount, speed, itemCount, basePath,fishAssets, treatAssets)

        for treatAsset in treatAssets:
            treatAsset.checkVisibleOnScreen(topRow, botRow, leftCol, rightCol)
            treatAsset.display(tileWidth, xOfset, yOfset, display)
            frontArray, fishCount, speed, itemCount, fishAssets, treatAssets = treatAsset.checkCollision(catMask, catX, catY, tileWidth, xOfset, yOfset, frontArray, backArray, fishCount, speed, itemCount, basePath,fishAssets, treatAssets)

        for fleaAsset in fleaAssets:
            fleaAsset.checkVisibleOnScreen(topRow-1, botRow+1, leftCol-1, rightCol+1)
            fleaAsset.display(tileWidth, xOfset, yOfset, display)
            frontArray, fishCount, speed, itemCount = fleaAsset.checkCollision(catMask, catX, catY, tileWidth, xOfset, yOfset, frontArray, backArray, fishCount, speed, itemCount)
            if swiping == True and round(swipePower) > 0:
                frontArray, fishCount = fleaAsset.checkPawCollision(rotatedPaw, pawX, pawY, tileWidth, xOfset, yOfset,frontArray, backArray, fishCount, basePath)
            if fleaAsset.waitingForDismiss == True:
                popups.append(fleaAsset) # Queue popup for flea.
            frontArray = fleaAsset.move(backArray, display, xOfset, yOfset,frontArray)

        for tickAsset in tickAssets:
            tickAsset.checkVisibleOnScreen(topRow-1, botRow+1, leftCol-1, rightCol+1)
            tickAsset.display(tileWidth, xOfset, yOfset, display)
            frontArray, fishCount, speed, itemCount = tickAsset.checkCollision(catMask, catX, catY, tileWidth, xOfset, yOfset,frontArray, backArray, fishCount, speed, itemCount)
            if swiping == True and round(swipePower) > 0:
                frontArray, fishCount = tickAsset.checkPawCollision(rotatedPaw, pawX, pawY, tileWidth, xOfset, yOfset, frontArray, backArray, fishCount, basePath)
            if tickAsset.waitingForDismiss == True:
                popups.append(tickAsset) # Queue popup for tick.
            frontArray = tickAsset.move(backArray, display, xOfset, yOfset, frontArray)

        for carAsset in carAssets:
            carAsset.checkVisibleOnScreen(topRow-1, botRow+1, leftCol-1, rightCol+1)
            carAsset.display(tileWidth, xOfset, yOfset, display)
            frontArray, fishCount, speed, itemCount = carAsset.checkCollision(catMask, catX, catY, tileWidth, xOfset, yOfset, frontArray, backArray, fishCount, speed, itemCount)
            if carAsset.waitingForDismiss == True:
                popups.append(carAsset) # Queue popup for car.
            frontArray = carAsset.move(backArray,frontArray)

        for dogAsset in dogAssets:
            dogAsset.checkVisibleOnScreen(topRow-1, botRow+1, leftCol-1, rightCol+1)
            dogAsset.display(tileWidth, xOfset, yOfset, display)
            frontArray, fishCount, speed, itemCount = dogAsset.checkCollision(catMask, catX, catY, tileWidth, xOfset, yOfset, frontArray, backArray, fishCount, speed, itemCount)
            if dogAsset.waitingForDismiss == True:
                popups.append(dogAsset) # Queue popup for dog.

        for lillyAsset in lillyAssets:
            lillyAsset.checkVisibleOnScreen(topRow, botRow, leftCol, rightCol)
            lillyAsset.display(tileWidth, xOfset, yOfset, display)
            frontArray, fishCount, speed, itemCount = lillyAsset.checkCollision(catMask, catX, catY, tileWidth, xOfset, yOfset, frontArray, backArray, fishCount, speed, itemCount)
            if lillyAsset.waitingForDismiss == True:
                popups.append(lillyAsset) # Queue popup for lilly.

        for catNeedAsset in catNeedAssets:
            catNeedAsset.checkVisibleOnScreen(topRow, botRow, leftCol, rightCol)
            catNeedAsset.display(tileWidth, xOfset, yOfset, display)
            frontArray, fishCount, speed, itemCount = catNeedAsset.checkCollision(catMask, catX, catY, tileWidth, xOfset, yOfset, frontArray, backArray, fishCount, speed, itemCount)
            if catNeedAsset.waitingForDismiss == True:
                popups.append(catNeedAsset) # Queue popup for catNeed.

        if popups != []:
            for activePopup in popups:
                activePopup.waitingForDismiss = False
                activePopup.collided = False
                # Remove catNeed from assets if popup was catNeed.
                if activePopup.name == "catNeed": # Cat needs cannot respawn- if popup was a catNeed, remove catNeed from list of catNeeds.
                    catNeedAssets.remove(activePopup)
            activePopup = None
            popups = []

        # Draw front layer tiles such as flowers and trees.
        for yIndex in range(topRow, botRow):
            for xIndex in range(leftCol, rightCol):
                x = xIndex * tileWidth - xOfset
                y = yIndex * tileWidth - yOfset
                tile = frontArray[yIndex][xIndex]
                if tile != 0: # Only draw non-empty tiles.
                    if tile == 1: # Flower tile
                        display.blit(flower, (x, y))
                    elif tile == 2: # Tree tile, offset for size.
                        display.blit(tree, (x - tileWidth, y - tileWidth * 2))

        # ================================ RENDER GAME INFO & MOBILE FRIENDLY CONTROLS ================================ #
        # Recharge swipe power slowly if not swiping. #################
        if swipePower < 10 and swiping == False:
            swipePower += 0.006

        # Fish count color (red if low).
        if fishCount < 5:
            fishColour = (255, 0, 0)
        else:
            fishColour = (255, 255, 255)

        # Swipe power color (red if low).
        if swipePower < 5:
            swipeColour = (255, 0, 0)
        else:
            swipeColour = (255, 255, 255)

        # Render player/game info.
        display.blit(gameBar, (0, 0)) # Game bar.
        fishRender = font.render(str(fishCount), True, fishColour)
        itemRender = font.render(f"{itemCount}/17", True, (255, 255, 255))
        timeRender = font.render(str(currentTime), True, (255, 255, 255))
        swipeRender = font.render(str(round(swipePower)), True, swipeColour)
        display.blit(fishRender, (40, 10))
        display.blit(timeRender, (122, 10))
        display.blit(swipeRender, (218, 10))
        display.blit(itemRender, (300, 10))

        # Draw mobile control button if mobile-friendly mode enabled ###############
        if mobileFriendlyOn == True:
            display.blit(mobileBack, (600, 150))
            display.blit(mobileFront, (mobileFrontCentre[0], mobileFrontCentre[1]))

        # ================================ CHECK END CONDITIONS ================================ #
        # Check if all items collected to trigger level end.
        if itemCount == 17:
            if endTimer == 0: # All items collected and bonusTime finished = end level.
                loop = False
                exitType = "PostGameCard"
                timer = currentTime
            elif endTimer == 300:
                bonusTime = largeFont.render("BONUS\nTIME!", True, (255, 0, 0))
                endTimer -= 1
            else:
                endTimer -= 1 # Timer for bonus time.
                display.blit(bonusTime, (5, 210))

        # Handle back button logic and drawing (highlight on hover).
        if backRect.collidepoint(mousePos) and mouseDown == True and len(backStack) > 1:
            loop = False
            exitType = "Back"  # Flag to navigate back screen.
        elif backRect.collidepoint(mousePos):
            display.blit(backLight, (backRect.x, backRect.y))
        else:
            display.blit(backDark, (backRect.x, backRect.y))

        if fishCount <= 0 and itemCount < 17:
        #if fishCount <= 0 and itemCount == 0:
            # Cat is hungry with no fish left — game over.
            loop = False
            display.blit(gameOver,(0,0))
            display.blit(sleepingCat,(295,310))
            loseSound = pygame.mixer.Sound(os.path.join(basePath, "Assets/Screens/Lose.ogg"))
            loseSound.play()
            pygame.display.update()
            await asyncio.sleep(3)
            
            exitType = "Back"

        clock.tick(60)  # Cap framerate to 60 FPS.
        pygame.display.update()
        await asyncio.sleep(0)

    # ================================ POST GAME PROCESSING ================================ #
    import Navigation
    if exitType == "PostGameCard": # Game win.
        display.blit(levelComplete,(0,0))
        display.blit(sleepingCat,(295,310))
        pygame.display.update()
        winSound = pygame.mixer.Sound(os.path.join(basePath, "Assets/Screens/Win.ogg"))
        winSound.play()
        await asyncio.sleep(3)
        newAchievements = [timer, fishCount]  # Store final time and fish collected.
        if int(levelNum)+1 <= 4:
            levelsUnlocked.append(int(levelNum)+1)

        # Navigate to PostGameCard screen.
        await Navigation.jumpToScreen("PostGameCard" + levelNum, display, colouredPrints, pawPrintTrails, backStack, parentPawPrints, username, levelsUnlocked, newAchievements, basePath, mobileFriendlyOn,popupsBool)
    if exitType == "Quit":
        pygame.quit()
        sys.exit()
    elif exitType == "Back":
        await Navigation.backScreen(display, colouredPrints, pawPrintTrails, backStack, parentPawPrints, username, levelsUnlocked, newAchievements, basePath, mobileFriendlyOn,popupsBool)

import pygame
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
from AssetsClass import assets
from EnemiesClass import enemies
from FleasClass import fleas
from TicksClass import ticks
from CarsClass import cars
from DogsClass import dogs
from LilliesClass import lillies
from CatNeedsClass import catNeeds
from FishClass import fishes
from TreatsClass import treats
import os
import time
import math
import LevelArrays
import random
import sys
import asyncio