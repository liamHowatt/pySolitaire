import pygame
from math import sin, radians
from itertools import cycle

def SinGen():
    for i in cycle(range(360)):
        i*=4
        yield sin(radians(i))
sinGen = SinGen()

pygame.init()
X = 0
Y = 1
WS = (1200,800) # window size
pygame.display.set_caption("projectile motion")
window = pygame.display.set_mode(WS)
bg = pygame.Surface(WS)

clock = pygame.time.Clock()
while True:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    bg.fill((107, 255, 178))
    pos = int(sinGen.__next__()*(WS[X]/2-5)+WS[X]/2)
    pygame.draw.line(bg,(255, 0, 225),(pos,0),(pos,WS[Y]),10)

    window.blit(bg,(0,0))
    pygame.display.flip()
