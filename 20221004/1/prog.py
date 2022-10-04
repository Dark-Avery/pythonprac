def bin_search(x, y):
    if len(y) == 0:
        return False
    elif y[(len(y)-1)//2] == x:
        return True
    elif x > y[len(y)//2]:
        return bin_search(x, y[:(len(y)-1)//2])
    else:
        return bin_search(x, y[(len(y)-1)//2+1:])

x, y = eval(input())
print(bin_search(x, y))