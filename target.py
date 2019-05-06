import math

def getSquareRounded(a):
 	ceil = 100
 	ans = a * a 
 	if ans>ceil:
 		return ceil
 	return ans

def getAbsoluteDifference(a,b):
	if a>b:
		return a-b
	return b-a


if __name__ == '__main__':
	a = int(input("a: "))
	b = int(input("b: "))
	
	a = getSquareRounded(a)
	b = getSquareRounded(b)

	diff = getAbsoluteDifference(a,b)
	print("Difference is:",diff) 