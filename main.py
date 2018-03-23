# https://github.com/liamHowatt/pySolitaire.git

from random import shuffle
from sys import platform

# Import relevant libraries
import pygame

if platform == "win32":
    import win32api

def constrain(a, minimum, maximum):
    if a < minimum:
        return minimum
    if a > maximum:
        return maximum
    return a

def getCardType(cardID):
    suit = int(cardID/13)
    face = cardID-(suit*13)
    return ((FACES[face], SUITS[suit]), [(255,0,0),(255,0,0),(0,0,0),(0,0,0)][suit])
    # returns (("A","♠"), (0,0,0))

def faceMath(face, increment):
    if not increment:
        return face
    index = FACES.index(face)
    output = index + increment
    if output < 0 or output > 12:
        return -1
    return FACES[output]

def cardVerticalPos():
    return row*constrain((ws[Y]-cw-ch-topOffset)/(len(table)-2),ch/32,ch/2)+hcw+topOffset

SUITS = ("♥", "♦", "♣", "♠")
FACES = ("A","2","3","4","5","6","7","8","9","10","J","Q","K")
table = []
pile = []
hand = [[]]
faceUps = []
mousePos = (0,0)
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
ws = (900,600) # initial window size
pygame.display.set_caption("Solitaire by Trent and Liam")
window = pygame.display.set_mode(ws, pygame.RESIZABLE)
MONITOR_RESOLUTION = pygame.display.list_modes()[0]
bg = pygame.Surface(MONITOR_RESOLUTION, flags=pygame.HWSURFACE).convert()
text = pygame.font.Font('resource/LiberationMono.ttf', 256) # initialized large then scaled down
pendingSizeChange = [True, ws]
# Showing a relevant icon to our game
pygame.display.set_icon(pygame.image.load("resource/icon.png"))
cardback = pygame.image.load("resource/cardback.png").convert()
cardHeightWidthRatio = cardback.get_rect()[3] / cardback.get_rect()[2]
# sizedCardback variable gets updated in the event loop
sizedCardback = pygame.transform.scale(cardback, (int(ws[X]/11), int(ws[X]/11*cardHeightWidthRatio)))
# VSync limited to Windows until we find out figure out other system specific calls
if platform == "win32":
    device = win32api.EnumDisplayDevices()
    settings = win32api.EnumDisplaySettings(device.DeviceName, -1)
    for varName in ['DisplayFrequency']:
        global refreshRate
        refreshRate = getattr(settings, varName)
else:
    refreshRate = 60

framecount = -1
clock = pygame.time.Clock()
while True:
    clock.tick(refreshRate)
    framecount += 1

    if framecount % refreshRate == 0: # things that happen every second
        if pendingSizeChange[0]:  # resizes every second instead of every frame
            pendingSizeChange[0] = False
            ws = pendingSizeChange[1]
            cw = ws[X]/11 # card width
            hcw = cw/2 # half card width
            thcw = cw * 1.5 # three halves card width
            ch = cw*cardHeightWidthRatio # card height
            sizedCardback = pygame.transform.scale(cardback, (int(cw), int(ch)))
            topOffset = cw+ch
            window = pygame.display.set_mode(ws, pygame.RESIZABLE)
        print("fps="+str(round(clock.get_fps(),1)))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.VIDEORESIZE:
            pendingSizeChange = [True, event.size]
        elif event.type == pygame.MOUSEMOTION:
            mousePos = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # click event
            for column in range(7):
                if mousePos[X] >= column * thcw + hcw and mousePos[X] <= (column+1) * thcw:
                    break
            else:
                continue
            numCardsInColumn = 0
            while table[numCardsInColumn][column] != None:
                numCardsInColumn += 1
            for row in reversed(range(numCardsInColumn)):
                if mousePos[Y] >= cardVerticalPos():
                    break
            else:
                if column == hand[1] and mousePos[Y] >= topOffset + hcw and mousePos[Y] <= ws[Y] - hcw:
                    for i,card in enumerate(hand[0]):
                        table.append([None]*7)
                        table[i+numCardsInColumn][column] = card
                    hand = [[]]
                continue
            if (row == numCardsInColumn-1 and mousePos[Y] > cardVerticalPos() + ch)\
                or (table[row][column] not in faceUps and table[row+1][column] != None):
                continue
            if hand == [[]]:
                hand.append(column)
                for i in range(row, numCardsInColumn):
                    hand[0].append(table[i][column])
                    table[i][column] = None
                continue
            if table[row][column] in faceUps:
                heldCard = getCardType(hand[0][0])
                targetCard = getCardType(table[row][column])
                if faceMath(heldCard[0][0], 1) != targetCard[0][0] or heldCard[0][1] == targetCard[0][1]:
                    continue
            for i,card in enumerate(hand[0]):
                table.append([None]*7)
                table[row+i+1][column] = card
            hand = [[]]

    while table[-2] == [None]*7 and len(table) > 2: # won't delete the constant empty row
        del(table[-1]) # deletes empty rows from memory

    bg.fill((0, 140, 30))
    pygame.draw.rect(bg, (0, 94, 20), ((0,0), (ws[X], topOffset)))
    for i in [0,3,4,5,6]:
        pygame.draw.rect(bg, (0, 140, 30), ((thcw*i+hcw, hcw), (cw, ch)))
    for i in zip(range(3,7), SUITS):
        temporaryText = text.render(i[1], 0, (0, 94, 20))
        temporaryText = pygame.transform.scale(temporaryText,
            (int(ws[X]/44), int(ws[X]/44/temporaryText.get_rect()[2]*temporaryText.get_rect()[3])) )
        bg.blit(temporaryText,
            ((thcw*i[0]+hcw+(hcw-temporaryText.get_rect()[2]/2)), (hcw+ch/2-temporaryText.get_rect()[3]/2)))
    if pile:
        bg.blit(sizedCardback, (hcw, hcw))
        pygame.draw.rect(bg, (0,0,0), ((hcw, hcw), (cw, ch)), 3)
    for row in range(len(table)):
        for column in range(7):
            if table[row][column] != None:
                rect = ( ((column*thcw+hcw), cardVerticalPos()), (cw, ch) )
                # determines if card should be face-up or not
                if table[row+1][column] == None and table[row][column] not in faceUps and hand == [[]]:
                    faceUps.append(table[row][column])
                if table[row][column] in faceUps:
                    pygame.draw.rect(bg, (255,255,255), rect, 0)
                    cardType = getCardType(table[row][column])
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
