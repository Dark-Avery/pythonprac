x = list(eval(input()))
n = len(x)
for i in range(n-1):
    for j in range(n-i-1):
        if x[j] ** 2 % 100 > x[j+1] ** 2 % 100:
            x[j], x[j+1] = x[j+1], x[j]
print(x)