import pygame
import os
from random import randint
from pygame.locals import *

FRAME_SIZE = (640, 480)

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.init()

mainFrame = pygame.display.set_mode(FRAME_SIZE)
pygame.display.set_caption('Pentago')


WD = os.getcwd()  # Working Directory

# Resources #
BG = pygame.image.load(os.path.join(WD, '../resources/bg.jpg'))
BG = pygame.transform.scale(BG, FRAME_SIZE)
mainFrame.blit(BG, (0, 0))

pieceWhite = pygame.image.load(os.path.join(WD, '../resources/pieceWhite.png')).convert_alpha()
WHITE_CHIP = pygame.transform.scale(pieceWhite, (60, 60))

EMPTY_CHIP = WHITE_CHIP.copy()
EMPTY_CHIP.fill((255, 255, 255, 30), None, pygame.BLEND_RGBA_MULT)  # Makes chip transparent

pieceBlack = pygame.image.load(os.path.join(WD, '../resources/pieceBlack.png')).convert_alpha()
BLACK_CHIP = pygame.transform.scale(pieceBlack, (60, 60))

FONT = pygame.font.Font(None, 30)

CHIP_SOUNDS = list()
for i in range(1, 4):
	CHIP_SOUNDS.append(pygame.mixer.Sound('../resources/chipsCollide' + str(i) + '.ogg'))


# GUI Constants #
BLOCK_SPACING = 30
BLOCK_SIZE = (180, 180)

BLOCK = pygame.Surface(BLOCK_SIZE, pygame.SRCALPHA)
BLOCK.fill((70, 70, 70, 80))

CHIP_SPACING = 40
CHIP_SIZE = 64
CHIPS = (EMPTY_CHIP, WHITE_CHIP, BLACK_CHIP)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

GRID_SIZE = 6


# Functions #
def generateGrid(n):
	return [[0 for i in range(n)] for i in range(n)]


def newGame():
	global currentGrid, gameState, currentPlayer
	currentGrid = generateGrid(GRID_SIZE)
	gameState = 1
	currentPlayer = 1

	mainFrame.blit(BG, (0, 0))
	drawGrid(currentGrid, mainFrame, True)
	displayIndication(mainFrame, 'Place a ' + ('white' if currentPlayer == 1 else 'black') + ' chip.')


def initClickPos(grid):
	global clickPos
	clickPos = list()
	blocks = len(grid) // 3

	for y in range(blocks):
		yOffset = BLOCK_SPACING if y == 0 else BLOCK_SPACING * 2
		for x in range(blocks):
			xOffset = BLOCK_SPACING if x == 0 else BLOCK_SPACING * 2
			posX, posY = x * BLOCK_SIZE[0] + xOffset, y * BLOCK_SIZE[1] + yOffset
			for yy in range(3):
				yOffset2 = CHIP_SPACING + 30 if yy == 0 else CHIP_SPACING + 20
				for xx in range(3):
					indX, indY = x * 3, y * 3
					xOffset2 = CHIP_SPACING + 30 if xx == 0 else CHIP_SPACING + 20
					indX += xx
					indY += yy

					clickPos.append(
						dict([
							('type', 'slot'),
							('pos', (posX + xx * xOffset2, posY + yy * yOffset2)),
							('size', (CHIP_SIZE, CHIP_SIZE)),
							('index', (indY, indX))
						])
					)


#def drawBlock(grid, surface, posX, posY, indX, indY):
#	surface.blit(BLOCK, (posX, posY))
#	global clickPos
#	for click in clickPos:
#		if click['type'] == 'slot':
#			if (indY <= click['index'][0] < indY + 3) and (indX <= click['index'][1] < indX + 3):
#				chip = CHIPS[grid[click['index'][0]][click['index'][1]]]
#				surface.blit(chip, (click['index'][0], click['index'][1]))


def drawBlock(grid, surface, posX, posY, indX, indY, calcClickPos):
	surface.blit(BLOCK, (posX, posY))

	for y in range(3):
		yOffset = CHIP_SPACING + 10 if y == 0 else CHIP_SPACING + 20
		for x in range(3):
			xOffset = CHIP_SPACING + 10 if x == 0 else CHIP_SPACING + 20
			chip = CHIPS[grid[indY + y][indX + x]]
			surface.blit(chip, (posX + x * xOffset, posY + y * yOffset))

			if calcClickPos:
				global clickPos
				clickPos.append(
					dict([
						('type', 'slot'),
						('pos', (posX + x * xOffset, posY + y * yOffset)),
						('size', (CHIP_SIZE, CHIP_SIZE)),
						('index', (indY + y, indX + x))
					])
				)


def drawGrid(grid, surface, calcClickPos=False):
	if calcClickPos:
		global clickPos
		clickPos = list()
		print('Clearing')

	blocks = len(grid) // 3
	for y in range(blocks):
		yOffset = BLOCK_SPACING if y == 0 else BLOCK_SPACING * 2
		for x in range(blocks):
			xOffset = BLOCK_SPACING if x == 0 else BLOCK_SPACING * 2
			drawBlock(grid, surface, x * BLOCK_SIZE[0] + xOffset, y * BLOCK_SIZE[1] + yOffset, x * 3, y * 3, calcClickPos)


def playChipSound():
	CHIP_SOUNDS[randint(0, 2)].play()


def putChip(grid, player, chipPos):

	if grid[chipPos[0]][chipPos[1]] == 0:
		playChipSound()
		grid[chipPos[0]][chipPos[1]] = player
		return True
	return False


def displayIndication(surface, sentence):
	sentenceSurface = FONT.render(sentence, True, BLACK, WHITE)
	sentenceRect = sentenceSurface.get_rect()
	sentenceRect.topleft = (FRAME_SIZE[0] - FONT.size(sentence)[0], 0)

	surface.blit(sentenceSurface, sentenceRect)


# Event Loop #
playing = True
redraw = False
newGame()

while playing:
	for event in pygame.event.get():
		if event.type == QUIT:
			playing = False
			break

		if event.type == MOUSEBUTTONUP:
			for click in clickPos:
				if (
					click['pos'][0] <= event.pos[0] <= (click['pos'][0] + click['size'][0]) and
					click['pos'][1] <= event.pos[1] <= (click['pos'][1] + click['size'][1])
				):
					if click['type'] == 'slot':
						if putChip(currentGrid, currentPlayer, click['index']):
							currentPlayer = 2 if currentPlayer == 1 else 1
							redraw = True
					elif click['type'] == 'newgame':
						newGame()
					break

	if redraw:
		redraw = False
		mainFrame.blit(BG, (0, 0))
		drawGrid(currentGrid, mainFrame)
		displayIndication(mainFrame, 'Place a ' + ('white' if currentPlayer == 1 else 'black') + ' chip.')

	pygame.display.update()


pygame.quit()
