import pygame
from math import sin, radians
from itertools import cycle

pygame.init()
X = 0
Y = 1
WS = (900,600) # initial window size
pygame.display.set_caption("Solitaire by Trent and Liam")
window = pygame.display.set_mode(WS, pygame.RESIZABLE)
MONITOR_RESOLUTION = pygame.display.list_modes()[0]
bg = pygame.Surface(MONITOR_RESOLUTION)
pendingSizeChange = False

framecount = 0
clock = pygame.time.Clock()
FPS = 30
while True:
    clock.tick(FPS)
    framecount += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.VIDEORESIZE:
            WS = event.size
            pendingSizeChange = True

    if pendingSizeChange and framecount % FPS == 0: # renders size change every second to avoid annoying blinking
        pendingSizeChange = False
        window = pygame.display.set_mode(WS, pygame.RESIZABLE)

    bg.fill((255,255,255))

    window.blit(bg,(0,0))
    pygame.display.flip()
