import copy

def rotateSubGridR(m, l):
	newList = []
	for i in range(0, m):
		annexList = []
		for j in range(m - 1, -1, -1):
			annexList.append(l[j][i])
		newList.append(annexList.copy())
	return newList


def rotateSubGridL(m, l):
	newList = l.copy()
	for k in range(0, 3):
		newList = rotateSubGridR(m, newList)
	return newList

def rotate(n, l, e, s):
	pass
	#en cours


lTest = [[1,4,7],[2,5,8],[3,6,9]]
print(lTest)
lTest = rotateSubGridL(len(lTest), lTest)
print(lTest)
rotate(len(lt),lt,1,True)
