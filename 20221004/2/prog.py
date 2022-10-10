def pareto(*args):
    ans = []
    help = lambda x, y: (x[0] <= y[0] and x[1] <= y[1]) and (x[0] < y[0] or x[1] < y[1])
    for i in range(len(args)):
        for j in range(len(args)):
            if i != j and help(args[i], args[j]):
                break
        else:
            ans.append(args[i])
    return tuple(ans)


print(pareto(*eval(input())))