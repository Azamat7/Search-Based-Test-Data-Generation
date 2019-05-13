import math

def getSquareRounded(a):
	ceil = 100
	ans = a * a 
	if ans>ceil:
		return ceil
	return ans

# def getAbsoluteDifference(a,b):
# 	if a>b:
# 		return a-b
# 	return b-a
