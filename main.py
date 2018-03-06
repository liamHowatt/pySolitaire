# https://github.com/liamHowatt/pySolitaire.git

from random import shuffle
from sys import platform

# Import relevant libraries
import pygame

if platform == "win32":
    import win32api

table = []
pile = []
cards = list(range(52))
shuffle(cards) # yes, this function changes the variable value "in place"
currentCard = -1
for y in range(7): # arranges cards on table
    table.append([None]*7)
    for x in range(y,7):
        currentCard += 1
        table[y][x] = cards[currentCard]
table.append([None]*7) # table stores a constant empty row
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
bg = pygame.Surface(MONITOR_RESOLUTION, flags=pygame.HWSURFACE).convert()
text = pygame.font.Font("resource/Courier Prime Sans Bold.ttf", 48) # initialized large then scaled down
pendingSizeChange = True
# Showing a relevant icon to our game
icon = pygame.image.load("resource/icon.png").convert()
pygame.display.set_icon(icon)
cardback = pygame.image.load("resource/cardback.png").convert()
cardHeightWidthRatio = cardback.get_rect()[3] / cardback.get_rect()[2]
# sizedCardback variable gets updated in the event loop
sizedCardback = pygame.transform.scale(cardback, (int(WS[X]/11), int(WS[X]/11*cardHeightWidthRatio)))

# Dynamic Scaling limited to Windows until we find out figure out other system specific calls
if platform == "win32":
    device = win32api.EnumDisplayDevices()
    settings = win32api.EnumDisplaySettings(device.DeviceName, -1)
    for varName in ['DisplayFrequency']:
        global refreshRate
        refreshRate = getattr(settings, varName)
else:
    refreshRate = 60

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

    if pendingSizeChange:
        temporaryHeight = WS[X]/11*cardHeightWidthRatio
        sizedCardback = pygame.transform.scale(cardback, (int(WS[X]/11), int(temporaryHeight)))
        topOffset = WS[X]/11+temporaryHeight

    if framecount % FPS == 0: # things that happen every second
        if pendingSizeChange:  # resizes every second instead of every frame
            pendingSizeChange = False
            window = pygame.display.set_mode(WS, pygame.RESIZABLE)
        print("fps="+str(round(clock.get_fps(),1)))

    while table[-2] == [None]*7 and len(table) > 2: # won't delete to constant empty row
        del(table[-1]) # deletes empty rows from memory

    bg.fill((0, 140, 30))
    pygame.draw.rect(bg, (0, 94, 20), ((0,0), (WS[X], topOffset)))
    for i in [0,3,4,5,6]:
        pygame.draw.rect(bg, (0, 140, 30), ((WS[X]*(3/22)*i+WS[X]/22, WS[X]/22), (WS[X]/11, temporaryHeight)))
    for i in [(3,"H"),(4,"D"),(5,"C"),(6,"S")]:
        temporaryText = text.render(i[1], 0, (0, 94, 20))
        temporaryText = pygame.transform.scale(temporaryText,
            (int(WS[X]/44), int(WS[X]/44/temporaryText.get_rect()[2]*temporaryText.get_rect()[3])) )
        bg.blit(temporaryText,
            ((WS[X]*(3/22)*i[0]+WS[X]/22+(WS[X]/22-temporaryText.get_rect()[2]/2)), (WS[X]/22+temporaryHeight/2-temporaryText.get_rect()[3]/2)))
    if len(pile):
        bg.blit(sizedCardback, (WS[X]/22, WS[X]/22))
        pygame.draw.rect(bg, (0,0,0), ((WS[X]/22, WS[X]/22), (WS[X]/11, temporaryHeight)), 3)
    for row in range(len(table)):
        for column in range(7):
            if table[row][column] != None:
                rect = ( ((column*(3/22)+(1/22))*WS[X],
                    row*max(min((WS[Y]-WS[X]/11-temporaryHeight-topOffset)/(len(table)-2),temporaryHeight/2),temporaryHeight/32)+WS[X]/22+topOffset),
                    (WS[X]/11, temporaryHeight) )
                if table[row+1][column] == None: # determines if card should be face-up or not
                    pygame.draw.rect(bg, (255,255,255), rect, 0)
                    suit = int(table[row][column]/13)
                    face = table[row][column]-(suit*13)
                    cardType = ((["A","2","3","4","5","6","7","8","9","10","J","Q","K"][face],
                        ["H","D","C","S"][suit]), [(255,0,0),(255,0,0),(0,0,0),(0,0,0)][suit])
                    widthModifier = {True:2, False:1}[cardType[0][0] == "10"]
                    temporaryText = text.render(cardType[0][0], 0, cardType[1])
                    temporaryText = pygame.transform.scale(temporaryText,
                        (int(rect[1][X]/4), int(rect[1][X]/4/temporaryText.get_rect()[2]*widthModifier*temporaryText.get_rect()[3])) )
                    bg.blit(temporaryText, (rect[0][X]+rect[1][X]/8, rect[0][Y]+rect[1][Y]/12))
                    temporaryText = text.render(cardType[0][1], 0, cardType[1])
                    temporaryText = pygame.transform.scale(temporaryText,
                        (int(rect[1][X]/4), int(rect[1][X]/4/temporaryText.get_rect()[2]*temporaryText.get_rect()[3])) )
                    bg.blit(temporaryText, (rect[0][X]+rect[1][X]-temporaryText.get_rect()[2]-rect[1][X]/8, rect[0][Y]+rect[1][Y]/12))
                else: # otherwise facedown
                    bg.blit(sizedCardback, rect[0])
                pygame.draw.rect(bg, (0,0,0), rect, 3) # card outline

    window.blit(bg,(0,0))
    pygame.display.flip()
