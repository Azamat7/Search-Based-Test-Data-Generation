import ast

class FuncLister(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
    	print(node.name)
    	for fieldname, value in ast.iter_fields(node):
    		print(fieldname,value)
    		print("\n")
    	self.generic_visit(node)

# Write the function for defining fitness function

class RewriteFunc(ast.NodeTransformer):
    def visit_FunctionDef(self, node):

    	# convert the above function to ast, then plug it in the beginning of node

        return ast.copy_location(ast.Subscript(
            value=ast.Name(id='data', ctx=ast.Load()),
            slice=ast.Index(value=ast.Str(s=node.id)),
            ctx=node.ctx
        ), node)

tree = RewriteName().visit(tree)

if __name__ == '__main__':
	with open("target.py", "r") as source:
		tree = ast.parse(source.read())

	# for node in ast.walk(tree):
	# 	#args = node.values
	# 	print(ast.dump(node),"\n")

	FuncLister().visit(tree)