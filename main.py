import pygame
from random import shuffle
import win32api

cards = list(range(52))
# order: hearts, diamonds, clubs, spades
# order within each suit: A, 2-10, J, Q, K
shuffle(cards) # yes, this function changes the variable value "in place"
currentCard = -1
for y in range(7): # arranges cards on table
    for x in range(y,7):
        currentCard += 1
        cards[currentCard] = [cards[currentCard], False, [x,y]] # is faceUp = False initially
while currentCard != 51:
    currentCard += 1
    cards[currentCard] = [cards[currentCard], False, [-1,-1]] # cards still in the pile

pygame.init()
X = 0
Y = 1
WS = (900,600) # initial window size
pygame.display.set_caption("Solitaire by Trent and Liam")
window = pygame.display.set_mode(WS, pygame.RESIZABLE)
MONITOR_RESOLUTION = pygame.display.list_modes()[0]
bg = pygame.Surface(MONITOR_RESOLUTION)
pendingSizeChange = False
somethingMoved = True

device = win32api.EnumDisplayDevices()
settings = win32api.EnumDisplaySettings(device.DeviceName, -1)
for varName in ['DisplayFrequency']:
    refreshRate = getattr(settings, varName)

framecount = 0
clock = pygame.time.Clock()
FPS = refreshRate
while True:
    clock.tick(FPS)
    framecount += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.VIDEORESIZE:
            WS = event.size
            pendingSizeChange = True

    if framecount % FPS == 0: # things that happen every second
        if pendingSizeChange:  # resizes every second instead of every frame
            pendingSizeChange = False
            window = pygame.display.set_mode(WS, pygame.RESIZABLE)
        print("fps="+str(round(clock.get_fps(),1)))

    bg.fill((0, 140, 30))

    window.blit(bg,(0,0))
    pygame.display.flip()
