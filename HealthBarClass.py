# Keeps track of andblits to the screen, health bars for fleas and ticks.

class healthBars:

    def __init__(self):
        self.health = 3
        
    # Every flea and tick has a health bar that changes colour as they are struck by the player's paw until they die.
    def drawBar(display,x,y,healthBar):
        blackRect = pygame.Rect(x,y,40,10)
        pygame.draw.rect(display,(0,0,0),blackRect)
        if healthBar.health == 3:
            colRect = pygame.Rect(x+3,y+3,34,4)
            pygame.draw.rect(display,(0,255,0),colRect)
        if healthBar.health == 2:
            colRect = pygame.Rect(x+3,y+3,22,4)
            pygame.draw.rect(display,(255,165,0),colRect)
        if healthBar.health == 1:
            colRect = pygame.Rect(x+3,y+3,11,4)
            pygame.draw.rect(display,(255,0,0),colRect)

    def decreaseBar(healthBar,fishCount):
        if healthBar.health == 1:
            healthBar.health = 3
            fishCount += 1
        else:
            healthBar.health -= 1
        return fishCount

import pygame
pygame.init()