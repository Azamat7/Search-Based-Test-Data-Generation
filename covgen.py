import astor
import ast
import random 
from predicates import *

def get_arguments(args):
    arguments = []
    for arg in args:
        arguments.append(arg.arg)
    return arguments

def tune_parameters(left, right, f, k):
    while not f(left.get_value(), right.get_value(), k):
        if left.get_type() == "Var":
            left.set_value(random.randint(-100,100))
        if right.get_type() == "Var":
            right.set_value(random.randint(-100,100))
    return left, right


if __name__ == '__main__':

    k = 1 # for fitness function

    tree = astor.parse_file("target.py")
    print(astor.dump_tree(tree))

    arguments = get_arguments(tree.body[1].args.args)
    print(arguments)

    treeBody = tree.body[1].body

    d = {ast.Gt : greater_than, ast.GtE : greater_than_equal, ast.Lt : less_than, ast.LtE : less_than_equal,
    ast.Eq : equal, ast.NotEq: not_equal}

    for line in treeBody:
        if isinstance(line, ast.If):
            comparator = line.test.ops[0]
            left = predicateElement(line.test.left)
            right = predicateElement(line.test.comparators[0])

            left, right = tune_parameters(left, right, d[type(comparator)], k)
            
            print(left.get_value(), right.get_value())

    #print(ast.body[1].args.args[0].arg)
    #print(isinstance([0], ast.If))

    #_ast.body[0].value.args[0].s = "arrrgh!"
    #exec(astor.to_source(_ast))

# Module(
#     body=[Import(names=[alias(name='math', asname=None)]),
#         FunctionDef(name='getAbsoluteDifference',
#             args=arguments(
#                 args=[arg(arg='a', annotation=None), arg(arg='b', annotation=None)],
#                 vararg=None,
#                 kwonlyargs=[],
#                 kw_defaults=[],
#                 kwarg=None,
#                 defaults=[]),
#             body=[AugAssign(target=Name(id='a'), op=Sub, value=Num(n=1)),
#                 If(test=Compare(left=Name(id='a'), ops=[Gt], comparators=[Name(id='b')]),
#                     body=[Return(value=BinOp(left=Name(id='a'), op=Sub, right=Name(id='b')))],
#                     orelse=[]),
#                 Return(value=BinOp(left=Name(id='b'), op=Sub, right=Name(id='a')))],
#             decorator_list=[],
#             returns=None)])



# import astor

# def hello():
#     print('hello!')
#     return

# _ast = astor.code_to_ast(hello)
# _ast.body[0].value.args[0].s = "arrrgh!"
# exec(astor.to_source(_ast))
# hello()
    

