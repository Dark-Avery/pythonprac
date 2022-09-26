a = eval(input())
if a % 25 == 0:
    if a % 2 == 0:
        s = "A + B - "
    else:
        s = "A - B + "
else:
    s = "A - B - "
if a % 8 == 0:
    s += "C +"
else:
    s += "C -"
print(s)
