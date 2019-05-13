import ast

class FuncLister(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        for line in node.body:
            if isinstance(line, ast.If):
                print(line)

        # for fieldname, value in ast.iter_fields(node):
        #     print(fieldname,value)
        #     print("\n")
        #self.generic_visit(node)

# Write the function for defining fitness function

class RewriteFunc(ast.NodeTransformer):
    def visit_FunctionDef(self, node):

        # convert the above function to ast, then plug it in the beginning of node

        print(node.__dict__)
        node.body.append(1)
        print(node.__dict__)

        return node


if __name__ == '__main__':

    with open("target.py", "r") as source:
        tree = ast.parse(source.read())

    FuncLister().visit(tree)
    RewriteFunc().visit(tree)

    # for node in ast.walk(tree):
    # 	#args = node.values
    # 	print(ast.dump(node),"\n")


