import ast

class predicateElement:
    def __init__(self, obj, d):
        self.object = obj

        if isinstance(obj, ast.Name):
            self.type = "Var"
            self.value = d[obj.id]
        elif isinstance(obj, ast.Num):
            self.type = "Num"
            self.value = obj.n

    def get_value(self):
        if not self.value:
            return 0
        return self.value

    def set_value(self, val):
        self.value = val

    def get_type(self):
        return self.type

def greater_than(a, b, k):
    f = b - a + k 
    if f < 0:
        return 0
    return f

def greater_than_equal(a, b, k):
    f = b - a + k 
    if f <= 0:
        return 0
    return f

def less_than(a, b, k):
    f = a - b + k 
    if f < 0:
        return 0
    return f

def less_than_equal(a, b, k):
    f = a - b + k 
    if f < 0:
        return 0
    return f

def equal(a, b, k):
    f = abs(a-b)
    if f == 0:
        return 0
    return f

def not_equal(a, b, k):
    f = -abs(a-b)
    if f < 0:
        return 0
    return f


