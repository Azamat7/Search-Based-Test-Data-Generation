import math

def getAbsoluteDifference(a,b):
	a-=1
	if a>b:
		return a-b

	if a>=b:
		return a-b

	if a<51:
		return a-b

	if 89<=b:
		return a-b

	if a==b:
		return a-b

	if a!=b:
		return a-b

	return b-a
