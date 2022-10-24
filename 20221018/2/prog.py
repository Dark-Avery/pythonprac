from math import *
d = {}
c, l = 1, 1
while (inp := input().split())[0] != 'quit':
    l += 1
    if inp[0][0] == ":":
        if len(inp) == 2:
            d[inp[0][1:]] = eval(f"lambda: {inp[-1]}")
        else:
            a, *args, f = inp
            d[a[1:]] = eval(f"lambda {','.join(args)}: {inp[-1]}")
        c += 1
    else:
        a, *args = inp
        print(d[a](*[eval(i) for i in args]))
print(" ".join(inp[1:]).replace('"', '').format(c, l))