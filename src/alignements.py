def checkAlignH(n, grid, p, j):
	for lineI in range(n):
		aligned = 0
		for colI in range(n):
			if grid[lineI][colI] == j:
				aligned += 1
			else:
				aligned = 0

			if aligned == p:
				return True
	return False


def checkAlignV(n, grid, p, j):
	for colI in range(n):
		aligned = 0
		for lineI in range(n):
			if grid[lineI][colI] == j:
				aligned += 1
			else:
				aligned = 0

			if aligned == p:
				return True
	return False


def checkAlignDBT(n, grid, p, j):
	for lineI in range(n - 1, -1, -1):
		for colI in range(n):
			if grid[lineI][colI] == j:
				offset = 1
				while (lineI - offset >= 0) and (colI + offset < n) and (grid[lineI - offset][colI + offset] == j):
					offset += 1
					if offset == p:
						return True
	return False


def checkAlignDTB(n, grid, p, j):
	for lineI in range(n):
		for colI in range(n):
			if grid[lineI][colI] == j:
				offset = 1
				while (lineI + offset < n) and (colI + offset < n) and (grid[lineI + offset][colI + offset] == j):
					offset += 1
					if offset == p:
						return True
	return False


def checkAlign(n, grid, p, j):
	return (
		checkAlignH(n, grid, p, j) or
		checkAlignV(n, grid, p, j) or
		checkAlignDBT(n, grid, p, j) or
		checkAlignDTB(n, grid, p, j)
	)
