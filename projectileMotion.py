import pygame
from math import sin, radians
from itertools import cycle

def SinGen():
    for i in cycle(range(360)):
        i*=4
        yield sin(radians(i))
sinGen = SinGen()

pygame.init()
WINDOW_SIZE = (400,400)
pygame.display.set_caption("projectile motion")
window = pygame.display.set_mode(WINDOW_SIZE)
bg = pygame.Surface(WINDOW_SIZE)

clock = pygame.time.Clock()
while True:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    bg.fill((107, 255, 178))
    pos = int(sinGen.__next__()*195+200)
    pygame.draw.line(bg,(255, 0, 225),(pos,0),(pos,399),10)

    window.blit(bg,(0,0))
    pygame.display.flip()
