def rotateR(m, l):
	newList = []

	for col in range(m):
		annexList = []
		for line in range(m - 1, -1, -1):
			annexList.append(l[line][col])
		newList.append(annexList.copy())

	return newList


def rotateL(m, l):
	newList = l.copy()
	for k in range(0, 3):
		newList = rotateR(m, newList)
	return newList


def rotate(n, l, sqr, left):
	square = []

	for line in range(n):
		if line < n//2:
			if sqr == 0:
				square.append(l[line][0:n//2])
			elif sqr == 3:
				square.append(l[line][n//2:n])
		else:
			if sqr == 1:
				square.append(l[line][0:n//2])
			elif sqr == 2:
				square.append(l[line][n//2:n])

	square = rotateL(n//2, square) if left else rotateR(n//2, square)
	for line in range(n):
		for col in range(n):
			pass
			#reinserer square dans la liste
	return square
	#gerer le retour


lTest = [
	[1, 0, 0, 1, 0, 0],
	[0, 0, 0, 0, 0, 0],
	[0, 0, 2, 0, 0, 2],
	[1, 0, 0, 1, 0, 0],
	[0, 0, 0, 0, 0, 0],
	[0, 0, 2, 0, 0, 2]
]
result = rotateR(6, lTest)
for i in result:
	print(i)
