# https://github.com/liamHowatt/pySolitaire.git

from random import shuffle
from sys import platform

# Import relevant libraries
import pygame

if platform == "win32":
    import win32api

def getCardName(number):
    # order: hearts, diamonds, clubs, spades
    # order within each suit: A, 2-10, J, Q, K
    suit = int(number/13)
    face = number-(suit*13)
    return ["ace","2","3","4","5","6","7","8","9","10","jack","queen","king"][face]+\
        " of " + ["hearts","diamonds","clubs","spades"][suit]

table = []
pile = []
cards = list(range(52))
shuffle(cards) # yes, this function changes the variable value "in place"
currentCard = -1
for y in range(7): # arranges cards on table
    table.append([0]*7)
    for x in range(y,7):
        currentCard += 1
        table[y][x] = cards[currentCard]
while currentCard != 51:
    currentCard += 1
    pile.append(cards[currentCard])

pygame.init()
X = 0
Y = 1
WS = (900,600) # initial window size
pygame.display.set_caption("Solitaire by Trent and Liam")
window = pygame.display.set_mode(WS, pygame.RESIZABLE)
MONITOR_RESOLUTION = pygame.display.list_modes()[0]
bg = pygame.Surface(MONITOR_RESOLUTION)
text = pygame.font.Font("McLaren-Regular.ttf", 8)
pendingSizeChange = False
# Showing a relevant icon to our game
icon = pygame.image.load("resource/icon.png")
pygame.display.set_icon(icon)

# Dynamic Scaling limited to Windows until we find out figure out other system specific calls
if platform == "win32":
    device = win32api.EnumDisplayDevices()
    settings = win32api.EnumDisplaySettings(device.DeviceName, -1)
    for varName in ['DisplayFrequency']:
        global refreshRate
        refreshRate = getattr(settings, varName)
else:
    refreshRate = 30

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

    while not sum(table[-1]):
        del(table[-1]) # deletes empty rows from memory

    bg.fill((0, 140, 30))


    window.blit(bg,(0,0))
    pygame.display.flip()
