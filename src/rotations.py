def rotateR(m, l):
	newList = []

	for y in range(m - 1, -1, -1):
		annexList = []
		for x in range(0, m):
			annexList.append(l[y][x])
		newList.append(annexList.copy())

	return newList


def rotateL(m, l):
	newList = l.copy()
	for k in range(0, 3):
		newList = rotateR(m, newList)
	return newList


def rotate(n, l, e, left):
	square = []

	for i in range(0, n):
		if i < n//2:
			if e == 0:
				square.append(l[0:n//2][i])
			elif e == 1 :
				square.append(l[n//2:n][i])
		else:
			if e == 2:
				square.append(l[n//2:n][i])
			elif e == 3:
				square.append(l[0:n//2][i])

	square = rotateL(n//2, square) if left else rotateR(n//2, square)
	return square
	#gerer le retour

lTest = [[1, 2, 3, 4],
		 [11, 22, 33, 44],
		 [111, 222, 333, 444],
		 [1111, 2222, 3333, 4444]]
print(rotate(4, lTest, 0, True))
