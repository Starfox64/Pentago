import pygame
import os
from src.rotations import *
from pygame.locals import *

FRAME_SIZE = (640, 480)
pygame.init()
mainFrame = pygame.display.set_mode(FRAME_SIZE)
pygame.display.set_caption('Pentago')

GRID = [
	[1, 0, 0, 1, 0, 0],
	[0, 0, 0, 0, 0, 0],
	[0, 0, 2, 0, 0, 2],
	[1, 0, 0, 1, 0, 0],
	[0, 0, 0, 0, 0, 0],
	[0, 0, 2, 0, 0, 2]
]

WD = os.getcwd()  # Working Directory

# Resources #
BG = pygame.image.load(os.path.join(WD, '..', 'resources', 'bg.jpg'))
BG = pygame.transform.scale(BG, FRAME_SIZE)
mainFrame.blit(BG, (0, 0))

pieceWhite = pygame.image.load(os.path.join(WD, '..', 'resources', 'pieceWhite.png')).convert_alpha()
WHITE_CHIP = pygame.transform.scale(pieceWhite, (60, 60))

EMPTY_CHIP = WHITE_CHIP.copy()
EMPTY_CHIP.fill((255, 255, 255, 30), None, pygame.BLEND_RGBA_MULT)  # Makes chip transparent

pieceBlack = pygame.image.load(os.path.join(WD, '..', 'resources', 'pieceBlack.png')).convert_alpha()
BLACK_CHIP = pygame.transform.scale(pieceBlack, (60, 60))

FONT = pygame.font.Font(None, 30)

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

BUTTONS = []


# Functions #
def _initChipsPos_(grid):
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
#					print(posX + xx*xOffset2, posY + yy*yOffset2)
					BUTTONS.append(
						dict([
							("name", "chip"),
							("position", (posX + xx * xOffset2, posY + yy * yOffset2)),
							("size", (CHIP_SIZE, CHIP_SIZE)),
							("gamePhase", 1),
							("listIndex", (indY, indX))
						])
					)
_initChipsPos_(GRID)


def drawBlock(grid, surface, posX, posY, indX, indY):
	surface.blit(BLOCK, (posX, posY))
	for z in BUTTONS:
		if z["name"] == "chip":
			if (indY <= z["listIndex"][0] < indY + 3) and (indX <= z["listIndex"][1] < indX + 3):
				chip = CHIPS[  grid[z["listIndex"][0]][z["listIndex"][1] ]  ]
				surface.blit(chip, (z["position"][0], z["position"][1]))
#	for y in range(3):
#		yOffset = CHIP_SPACING + 30 if y == 0 else CHIP_SPACING + 20
#		for x in range(3):
#			xOffset = CHIP_SPACING + 30 if x == 0 else CHIP_SPACING + 20
#			chip = CHIPS[grid[indY + y][indX + x]]
#			surface.blit(chip, (posX + x * xOffset, posY + y * yOffset))


def drawGrid(grid, surface):
	blocks = len(grid) // 3
	for y in range(blocks):
		yOffset = BLOCK_SPACING if y == 0 else BLOCK_SPACING * 2
		for x in range(blocks):
			xOffset = BLOCK_SPACING if x == 0 else BLOCK_SPACING * 2
			surface.blit(BLOCK, (x * BLOCK_SIZE[0] + xOffset, y * BLOCK_SIZE[1] + yOffset))
			drawBlock(grid, surface, x * BLOCK_SIZE[0] + xOffset, y * BLOCK_SIZE[1] + yOffset, x * 3, y * 3)


def putChip(player, chipPos):

	if GRID[chipPos[0]][chipPos[1]] == 0 :
		GRID[chipPos[0]][chipPos[1]] = player
		return True
	else:
		return False


def displayIndication(surface, sentence, indicationLevel):

	if indicationLevel == "instruction":
		sentenceSurface = FONT.render(sentence, True, BLACK, WHITE)
		sentenceRect = sentenceSurface.get_rect()
		sentenceRect.topleft = (FRAME_SIZE[0] - FONT.size(sentence)[0], FRAME_SIZE[1]//2)

	else:
		sentenceSurface = FONT.render(sentence, True, RED, BLACK)
		sentenceRect = sentenceSurface.get_rect()
		sentenceRect.topleft = (FRAME_SIZE[0] - FONT.size(sentence)[0], FRAME_SIZE[1] - FONT.size(sentence)[1])

	surface.blit(sentenceSurface,sentenceRect)

# Event Loop #
playing = True
redraw = False
currentPlayer = 1
gameState = 1  # 1: Placing / 2: Rotating / 3: Over
drawGrid(GRID, mainFrame)
displayIndication(mainFrame, "Poser un pion " + ("blanc" if currentPlayer == 1 else "noir"), "instruction")

while playing:


	for event in pygame.event.get():
		if event.type == QUIT:
			playing = False

		if event.type == MOUSEBUTTONUP:
			print(event.pos)
			print(pygame.mouse.get_pos())

			for i in BUTTONS:
				if i["position"][0] <= event.pos[0] <= (i["position"][0] + i["size"][0]) and i["position"][1] <= event.pos[1] <= (i["position"][1] + i["size"][1]):
					displayIndication(mainFrame, "Zone interactible", "warning")

#					if gameState == i["gamePhase"]:
#						if i["name"] == "chip":
					if putChip(currentPlayer, i["listIndex"]) is True:
						currentPlayer = 2 if currentPlayer == 1 else 1
						redraw = True
						break
					else:
						displayIndication(mainFrame, "Case Indisponible", "warning")
						redraw = False
	if redraw:
		mainFrame.blit(BG, (0, 0))
		drawGrid(GRID, mainFrame)
		displayIndication(mainFrame, "Poser un pion " + ("blanc" if currentPlayer == 1 else "noir"), "instruction")


	pygame.display.update()

pygame.quit()