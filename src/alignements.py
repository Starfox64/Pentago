def checkAlignH(n, grid, p, j):
	for lineI in range(n):
		line = grid[lineI]
		aligned = 0
		for i in range(n):
			if line[i] == j:
				aligned += 1
			else:
				aligned = 0

			if aligned == p:
				return True
	return False
