import ast

if __name__ == '__main__':
	with open("target.py", "r") as source:
		tree = ast.parse(source.read())

	for node in ast.walk(tree):
		print(ast.dump(node))
