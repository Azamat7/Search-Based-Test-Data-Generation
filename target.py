import math

def func(a,b,c):

	if a>b:
		if a<b:
			return a
	a = a % 2
	d = 10
	c = c + a
	a = a - d
	if a>b:
		if a<=15:
			a = a+b
			if c==30:
				return b
			else:
				if a>40:
					return b-a

				if a>50:
					return 60

	if a<51:
		return a-b

	return b-a

def func1(a,b,c):

	if a>b:
		if a<b:
			return a
	a = a % 2
	d = 10
	c = c + a
	a = a - d
	if a>b:
		if a<=15:
			a = a+b
			if c==30:
				return b
			else:
				if a>40:
					return b-a

				if a>50:
					return 60

	if a<51:
		return a-b

	return b-a

