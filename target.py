import math

def func(a,b):
	a-=1
	if a>b:
		if a>15:
			a = a-b
			if a==30:
				return b
			else:
				if a>40:
					return b-a

				if a>50:
					return 60

	if a<51:
		return a-b

	return b-a


