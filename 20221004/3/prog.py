def sub(x, y):
    return type(x)(i for i in x if i not in y) if (type(x) == tuple or type(x) == list) else x - y

print(sub(*eval(input())))