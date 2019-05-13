import astor

if __name__ == '__main__':

    ast = astor.parse_file("target.py")

    print(astor.dump_tree(ast))

    #_ast.body[0].value.args[0].s = "arrrgh!"
    #exec(astor.to_source(_ast))

    

