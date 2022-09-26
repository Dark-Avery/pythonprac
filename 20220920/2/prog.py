s = 0
while (a := int(input())) > 0:
    s += a
    if s > 21:
        print(s)
        break
else:
    print(a)