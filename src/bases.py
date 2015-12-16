def generateGrid(n):
	return [[0 for i in range(n)] for i in range(n)]


def printGrid(grid):
	for line in grid:
		for val in line:
			print(str(val) + ' ', end='')
		print('')
