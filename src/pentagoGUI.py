import pygame
import os
import json
from random import randint
from pygame.locals import *
from src.rotations import *
from src.bases import *
from src.alignements import *

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

pieceWhite = pygame.image.load(os.path.join(WD, '../resources/pieceWhite.png')).convert_alpha()
WHITE_CHIP = pygame.transform.scale(pieceWhite, (60, 60))

EMPTY_CHIP = WHITE_CHIP.copy()
EMPTY_CHIP.fill((255, 255, 255, 30), None, pygame.BLEND_RGBA_MULT)  # Makes chip transparent

pieceBlack = pygame.image.load(os.path.join(WD, '../resources/pieceBlack.png')).convert_alpha()
BLACK_CHIP = pygame.transform.scale(pieceBlack, (60, 60))

sliderLeft = pygame.image.load(os.path.join(WD, '../resources/grey_sliderLeft.png')).convert_alpha()
LEFT_SLIDER = pygame.transform.scale(sliderLeft, (40, 30))

LEFT_SLIDER_T = LEFT_SLIDER.copy()
LEFT_SLIDER_T.fill((255, 255, 255, 50), None, pygame.BLEND_RGBA_MULT)

sliderRight = pygame.image.load(os.path.join(WD, '../resources/grey_sliderRight.png')).convert_alpha()
RIGHT_SLIDER = pygame.transform.scale(sliderRight, (40, 30))

RIGHT_SLIDER_T = RIGHT_SLIDER.copy()
RIGHT_SLIDER_T.fill((255, 255, 255, 50), None, pygame.BLEND_RGBA_MULT)

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
ALIGN_WIN = 5


# Functions #


def newGame(grid=None, state=1, player=1):
	global currentGrid, gameState, currentPlayer
	currentGrid = grid or generateGrid(GRID_SIZE)
	gameState = state
	currentPlayer = player

	mainFrame.blit(BG, (0, 0))
	draw(currentGrid, mainFrame, True)
	drawText(mainFrame, 'Place a ' + ('white' if currentPlayer == 1 else 'black') + ' chip.',  BLACK, WHITE, 0)

	pygame.display.update()


def loadGame():
	try:
		file = open(os.path.join(WD, '../save.json'), 'r')
	except FileNotFoundError:
		return 'Save not available.'

	gameData = json.loads(file.read())
	file.close()
	newGame(gameData['grid'], gameData['state'], gameData['player'])
	return 'Game loaded.'


def saveGame(grid, state, player):
	file = open(os.path.join(WD, '../save.json'), 'w')
	file.write(json.dumps({'grid': grid, 'state': state, 'player': player}))
	return 'Game saved.'


def addClickPos(type, pos, size, args=None):
	clickPos.append({
		'type': type,
		'pos': pos,
		'size': size,
		'args': args
	})


def drawBlock(grid, surface, posX, posY, indX, indY, calcClickPos):
	surface.blit(BLOCK, (posX, posY))
	surface.blit(LEFT_SLIDER if gameState == 2 else LEFT_SLIDER_T, (posX - 5 + BLOCK_SIZE[0] / 6, posY - 30))
	surface.blit(RIGHT_SLIDER if gameState == 2 else RIGHT_SLIDER_T, (posX - 5 + 4 * (BLOCK_SIZE[0] / 6), posY - 30))

	if calcClickPos:
		addClickPos(
			'rotate',
			(posX - 5 + BLOCK_SIZE[0] / 6, posY - 30),
			(40, 30),
			{'left': True, 'indX': (indX + 1) // 3, 'indY': (indY + 1) // 3}
		)
		addClickPos(
			'rotate',
			(posX - 5 + 4 * (BLOCK_SIZE[0] / 6), posY - 30),
			(40, 30),
			{'left': False, 'indX': (indX + 1) // 3, 'indY': (indY + 1) // 3}
		)

	for y in range(3):
		yOffset = CHIP_SPACING + 10 if y == 0 else CHIP_SPACING + 20
		for x in range(3):
			xOffset = CHIP_SPACING + 10 if x == 0 else CHIP_SPACING + 20
			chip = CHIPS[grid[indY + y][indX + x]]
			surface.blit(chip, (posX + x * xOffset, posY + y * yOffset))

			if calcClickPos:
				addClickPos(
					'slot',
					(posX + x * xOffset, posY + y * yOffset),
					(CHIP_SIZE, CHIP_SIZE),
					{'index': (indY + y, indX + x)}
				)


def draw(grid, surface, calcClickPos=False):
	newRect = drawText(surface, ' New Game', WHITE, BLACK, 50)
	loadRect = drawText(surface, 'Load Game', WHITE, BLACK, 75)
	saveRect = drawText(surface, 'Save Game', WHITE, BLACK, 100)

	if calcClickPos:
		global clickPos
		clickPos = list()
		addClickPos('newgame', newRect.topleft, newRect.size)
		addClickPos('loadgame', loadRect.topleft, loadRect.size)
		addClickPos('savegame', saveRect.topleft, saveRect.size)

	blocks = len(grid) // 3
	for y in range(blocks):
		yOffset = 20 + (BLOCK_SPACING if y == 0 else BLOCK_SPACING * 2)
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


def drawText(surface, text, textCol=BLACK, bgCol=WHITE, y=None):
	textSurface = FONT.render(text, True, textCol, bgCol)
	rect = textSurface.get_rect()
	if y is None:  # Bottom Right
		rect.bottomright = (FRAME_SIZE[0], FRAME_SIZE[1])
	else:
		rect.topright = (FRAME_SIZE[0], y)

	surface.blit(textSurface, rect)
	return rect


# Event Loop #
playing = True
update = False
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
					update = True
					bottomNotif = None

					if click['type'] == 'slot' and gameState == 1:
						if putChip(currentGrid, currentPlayer, click['args']['index']):
							if checkAlign(len(currentGrid), currentGrid, ALIGN_WIN, currentPlayer):
								gameState = 3
								bottomNotif = 'The ' + ('whites' if currentPlayer == 1 else 'blacks') + ' won!'
								break
							gameState = 2
					elif click['type'] == 'rotate' and gameState == 2:
						currentGrid = rotate(
							len(currentGrid),
							currentGrid,
							click['args']['indX'],
							click['args']['indY'],
							click['args']['left']
						)
						if checkAlign(len(currentGrid), currentGrid, ALIGN_WIN, currentPlayer):
							gameState = 3
							bottomNotif = 'The ' + ('whites' if currentPlayer == 1 else 'blacks') + ' won!'
							break
						currentPlayer = 2 if currentPlayer == 1 else 1
						gameState = 1
					elif click['type'] == 'newgame':
						newGame()
					elif click['type'] == 'savegame':
						bottomNotif = saveGame(currentGrid, gameState, currentPlayer)
					elif click['type'] == 'loadgame':
						bottomNotif = loadGame()
					break

	if update:
		update = False
		mainFrame.blit(BG, (0, 0))
		draw(currentGrid, mainFrame)
		if gameState == 1:
			drawText(mainFrame, 'Place a ' + ('white' if currentPlayer == 1 else 'black') + ' chip.', BLACK, WHITE, 0)
		elif gameState == 2:
			drawText(mainFrame, 'Now rotate a block.', BLACK, WHITE, 0)
		if bottomNotif is not None:
			drawText(mainFrame, bottomNotif)

		pygame.display.update()


pygame.quit()
