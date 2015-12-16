def checkAlignH(n, grid, p, j):
	if len(grid) == n and len(grid[0]) == n:
		for line in grid:
			aligned = 0
			for val in line:
				if val == j:
					aligned += 1
				else:
					aligned = 0

				if aligned == p:
					return True
	return False
