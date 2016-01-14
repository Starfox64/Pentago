def rotateR(m, l):
	newList = []

	for col in range(m):
		annexList = []
		for line in range(m - 1, -1, -1):
			annexList.append(l[line][col])
		newList.append(annexList.copy())

	return newList

def rotateL(m, l):
	for k in range(3):
		l = rotateR(m, l)
	return l


def rotate(n, l, indX, indY, left):
	square = []

	#isoler le quadrant n. sqr
	if indX == 0 and indY == 0:
		for line in range(n//2):
			linedSquare = []
			for col in range(n//2):
				linedSquare.append(l[line][col])
			square.append(linedSquare.copy())
	elif indX == 0 and indY == 1:
		for line in range(n//2, n):
			linedSquare = []
			for col in range(n//2):
				linedSquare.append(l[line][col])
			square.append(linedSquare.copy())
	elif indX == 1 and indY == 1:
		for line in range(n//2, n):
			linedSquare = []
			for col in range(n//2, n):
				linedSquare.append(l[line][col])
			square.append(linedSquare.copy())
	elif indX == 1 and indY == 0:
		for line in range(n//2):
			linedSquare = []
			for col in range(n//2, n):
				linedSquare.append(l[line][col])
			square.append(linedSquare.copy())

	#effectuer la rotation du quadrant
	square = rotateL(n//2, square) if left else rotateR(n//2, square)

	#reinserer le quadrant dans la liste
	if indX == 0 and indY == 0:
		for line in range(n//2):
			for col in range(n//2):
				l[line][col] = square[line][col]
	elif indX == 0 and indY == 1:
		for line in range(n//2, n):
			for col in range(n//2):
				l[line][col] = square[line - 3][col]
	elif indX == 1 and indY == 1:
		for line in range(n//2, n):
			for col in range(n//2, n):
				l[line][col] = square[line - 3][col - 3]
	elif indX == 1 and indY == 0:
		for line in range(n//2):
			for col in range(n//2, n):
				l[line][col] = square[line][col - 3]

	return l
