import pygame
import os
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

# GUI Constants #
BLOCK_SPACING = 30
BLOCK_SIZE = (180, 180)

BLOCK = pygame.Surface(BLOCK_SIZE, pygame.SRCALPHA)
BLOCK.fill((70, 70, 70, 80))

CHIP_SPACING = 40
CHIP_SIZE = 20
CHIPS = (EMPTY_CHIP, WHITE_CHIP, BLACK_CHIP)


# Functions #
def drawBlock(grid, surface, posX, posY, indX, indY):
	surface.blit(BLOCK, (posX, posY))

	for y in range(3):
		yOffset = CHIP_SPACING + 30 if y == 0 else CHIP_SPACING + CHIP_SIZE
		for x in range(3):
			xOffset = CHIP_SPACING + 30 if x == 0 else CHIP_SPACING + CHIP_SIZE
			chip = CHIPS[grid[indY + y][indX + x]]
			surface.blit(chip, (posX + x * xOffset, posY + y * yOffset))


def drawGrid(grid, surface):
	blocks = len(grid) // 3
	for y in range(blocks):
		yOffset = BLOCK_SPACING if y == 0 else BLOCK_SPACING * 2
		for x in range(blocks):
			xOffset = BLOCK_SPACING if x == 0 else BLOCK_SPACING * 2
			drawBlock(grid, surface, x * BLOCK_SIZE[0] + xOffset, y * BLOCK_SIZE[1] + yOffset, x * 3, y * 3)


drawGrid(GRID, mainFrame)

# Event Loop #
playing = True
currentPlayer = 1
gameState = 1  # 1: Placing / 2: Rotating / 3: Over

while playing:
	for event in pygame.event.get():
		if event.type == QUIT:
			playing = False

	pygame.display.update()

pygame.quit()
