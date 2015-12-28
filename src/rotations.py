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


def rotate(n, l, sqr, left):
	square = []
	#isoler le quadrant n. sqr

	if sqr == 0:
		for line in range(n//2):
			linedSquare = []
			for col in range(n//2):
				linedSquare.append(l[line][col])
			square.append(linedSquare.copy())
	elif sqr == 1:
		for line in range(n//2, n):
			linedSquare = []
			for col in range(n//2):
				linedSquare.append(l[line][col])
			square.append(linedSquare.copy())
	elif sqr == 2:
		for line in range(n//2, n):
			linedSquare = []
			for col in range(n//2, n):
				linedSquare.append(l[line][col])
			square.append(linedSquare.copy())
	elif sqr == 3:
		for line in range(n//2):
			linedSquare = []
			for col in range(n//2, n):
				linedSquare.append(l[line][col])
			square.append(linedSquare.copy())

	#effectuer la rotation du quadrant
	square = rotateL(n//2, square) if left else rotateR(n//2, square)

	#reinserer le quadrant dans la liste
	if sqr == 0:
		for line in range(n//2):
			for col in range(n//2):
				l[line][col] = square[line][col]
	elif sqr == 1:
		for line in range(n//2, n):
			for col in range(n//2):
				l[line][col] = square[line - 3][col]
	elif sqr == 2:
		for line in range(n//2, n):
			for col in range(n//2, n):
				l[line][col] = square[line - 3][col - 3]
	elif sqr == 3:
		for line in range(n//2):
			for col in range(n//2, n):
				l[line][col] = square[line][col - 3]

	return l


lTest = [
	[1, 0, 0, 1, 0, 0],
	[0, 0, 0, 0, 0, 0],
	[0, 0, 2, 0, 0, 2],
	[1, 0, 0, 1, 0, 0],
	[0, 0, 0, 0, 0, 0],
	[0, 0, 2, 0, 0, 2]
]
result = rotate(6, lTest, 0, False)
for i in result:
	print(i)
