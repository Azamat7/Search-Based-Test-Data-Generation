import astor
import ast
import random 
from predicates import *

def tune_parameters(left, right, f, k):
    while not f(left.get_value(), right.get_value(), k):
        if left.get_type() == "Var":
            left.set_value(random.randint(-100,100))
        if right.get_type() == "Var":
            right.set_value(random.randint(-100,100))
    return left, right

def get_branches(body, parents = []):
    branches = []
    i = 1
    for line in body:
        if isinstance(line, ast.If):
            parents.append((i,1))
            branches.append([x for x in parents])
            more = get_branches(line.body, [x for x in parents])
            branches += more
            parents.pop()

            if line.orelse:
                parents.append((i,2))
                more = get_branches(line.orelse, [x for x in parents])
                branches += more
                parents.pop()
            i+=1
    return branches

def get_fitness(params, body, branch, d, applvl):
    preds = {ast.Gt : greater_than, ast.GtE : greater_than_equal, ast.Lt : less_than, ast.LtE : less_than_equal,
    ast.Eq : equal, ast.NotEq: not_equal}
    mirror = {ast.Gt : ast.Lt, ast.Lt : ast.Gt, ast.GtE : ast.LtE, ast.LtE : ast.GtE, ast.Eq : ast.NotEq, 
    ast.NotEq : ast.Eq}
    k = 1

    x,y = branch[0]
    i=0
    line = body.pop(0)

    if isinstance(line, ast.If):
        i+=1

    while i!=x:
        line = body.pop(0)
        if isinstance(line, ast.If):
            if y==2:
                temp = line.orelse
            i+=1
        else:
            d = eval_line(line, d, params)

    comparator = line.test.ops[0]
    bdist = preds[type(comparator)]
    if y==2:
        comparator = mirror[type(comparator)]
        bdist = preds[comparator]
    left = predicateElement(line.test.left, d)
    right = predicateElement(line.test.comparators[0], d)

    fitness = applvl + (1 - 1.001 ** bdist(left.get_value(), right.get_value(), k))

    if fitness == 0:
        return 0
    elif len(branch)==1:
        return fitness
    else:
        if y==2:
            return get_fitness(params, [x for x in line.orelse], branch[1:], d, applvl-1)
        return get_fitness(params, [x for x in line.body], branch[1:], d, applvl-1)

def eval_line(line, d, params):
    return d


if __name__ == '__main__':

    tree = astor.parse_file("target.py")
    print(astor.dump_tree(tree))

    functionDefs = [line for line in tree.body if isinstance(line, ast.FunctionDef)]
    for function in functionDefs:
        arguments = [x.arg for x in function.args.args]

        branches = get_branches(function.body)
        print(branches)
        
        inputs = []
        print("Search Started ... ")
        for branch in branches:
            applvl = len(branch)-1
            params = [0]*len(arguments)
            fitness_result = applvl+1
            while fitness_result != 0:
                params = [random.randint(-100,100) for _ in range(len(params))]
                d = dict()
                for (i,x) in enumerate(arguments):
                    d[x] = params[i]
                fitness_result = get_fitness(params, [x for x in function.body], branch, d, applvl)
            inputs.append(params)
            print(branch, params)

        print(inputs)

        # for line in function.body:
        #     if isinstance(line, ast.If):
        #         comparator = line.test.ops[0]
        #         left = predicateElement(line.test.left)
        #         right = predicateElement(line.test.comparators[0])

        #         left, right = tune_parameters(left, right, d[type(comparator)], k)
                
        #         print(left.get_value(), right.get_value())



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
    

