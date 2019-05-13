import astor
import ast
import random 

def get_arguments(args):
    arguments = []
    for arg in args:
        arguments.append(arg.arg)
    return arguments

def greater_than(a, b, k):
    f = b - a + k 
    if f <= 0:
        return True
    return False


if __name__ == '__main__':

    k = 1 # for fitness function

    tree = astor.parse_file("target.py")
    
    arguments = get_arguments(tree.body[1].args.args)
    print(arguments)

    treeBody = tree.body[1].body


    
    for line in treeBody:
        if isinstance(line, ast.If):
            comparator = line.test.ops[0]

            # greate than 
            if isinstance(comparator, ast.Gt):
                left = line.test.left.id
                right = line.test.comparators[0].id

                d = dict()
                d[left] = 0
                d[right] = 0

                f = greater_than

                while not f(d[left], d[right], k):
                    d[left] = random.randint(-100,100)
                    d[right] = random.randint(-100,100)

                print(d[left], d[right])


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
    

