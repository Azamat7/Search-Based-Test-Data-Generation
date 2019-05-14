import random 
import time
import astor
import ast
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
    mirror = {ast.Gt : ast.LtE, ast.Lt : ast.GtE, ast.GtE : ast.Lt, ast.LtE : ast.Gt, ast.Eq : ast.NotEq, 
    ast.NotEq : ast.Eq}
    k = 1

    x,y = branch[0]
    i=0
    line = body.pop(0)

    if isinstance(line, ast.If):
        i+=1
    else:
        d = eval_line(line, d, params)

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

    b = (1 - 1.001 ** bdist(left.get_value(), right.get_value(), k))
    fitness = applvl + b

    if fitness == 0:
        return 0
    elif len(branch)==1:
        return fitness
    else:
        if b==0:
            if y==2:
                return get_fitness(params, [x for x in line.orelse], branch[1:], d, applvl-1)
            return get_fitness(params, [x for x in line.body], branch[1:], d, applvl-1)
        else:
            return fitness

def evaluate(left, right, op):
    if isinstance(op, ast.Add):
        return left + right
    elif isinstance(op, ast.Sub):
        return left - right
    elif isinstance(op, ast.Mult):
        return left * right
    elif isinstance(op, ast.Div):
        return left / right
    elif isinstance(op, ast.Pow):
        return left ** right
    elif isinstance(op, ast.FloorDiv):
        return left // right
    elif isinstance(op, ast.Mod):
        return left % right

def eval_line(line, d, params):
    if isinstance(line, ast.AugAssign):
        target = line.target.id
        num = predicateElement(line.value, d)
        d[target] = evaluate(d[target], num.get_value, line.op)
    elif isinstance(line, ast.Assign):
        target = line.targets[0].id
        if isinstance(line.value, ast.BinOp):
            left = predicateElement(line.value.left,d)
            right = predicateElement(line.value.right,d)
            d[target] = evaluate(left.get_value(), right.get_value(), line.value.op)
        elif isinstance(line.value, ast.Num):
            d[target] = line.value.n
    return d

def format_inputs(params):
    if not params:
        return "-"
    args = ""
    for a in params:
        args += str(a)
        args += ", "
    return args[:-2]

if __name__ == '__main__':

    tree = astor.parse_file("target.py")
    print(astor.dump_tree(tree))

    functionDefs = [line for line in tree.body if isinstance(line, ast.FunctionDef)]
    for function in functionDefs:
        arguments = [x.arg for x in function.args.args]

        branches = get_branches(function.body)
        #print(branches)
        
        inputs = []
        print("Search Started ... ")
        for branch in branches:
            applvl = len(branch)-1
            params = [0]*len(arguments)
            fitness_result = applvl+1
            
            ticks = time.time()
            unreachable = 0
            while fitness_result != 0:
                if (time.time()-ticks)>1:
                    unreachable = 1
                    break
                params = [random.randint(-100,100) for _ in range(len(params))]
                d = dict()
                for (i,x) in enumerate(arguments):
                    d[x] = params[i]
                fitness_result = get_fitness(params, [x for x in function.body], branch, d, applvl)
            
            if unreachable:
                inputs.append(None)
            inputs.append(params)

        #print(inputs)

        finputs = []
        for branch in branches:
            x,y = branch[-1]
            branch[-1] = (x,2)
            applvl = len(branch)-1
            params = [0]*len(arguments)
            fitness_result = applvl+1

            ticks = time.time()
            unreachable = 0
            while fitness_result != 0:
                if (time.time()-ticks)>1:
                    unreachable = 1
                    break
                params = [random.randint(-100,100) for _ in range(len(params))]
                d = dict()
                for (i,x) in enumerate(arguments):
                    d[x] = params[i]
                fitness_result = get_fitness(params, [x for x in function.body], branch, d, applvl)

            if unreachable:
                finputs.append(None)
            finputs.append(params)
        #print(finputs)

        for i in range(len(branches)):
            print("%sT: %s" % (str(i+1),format_inputs(inputs[i])))
            print("%sF: %s" % (str(i+1),format_inputs(finputs[i])))

