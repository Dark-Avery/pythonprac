matr1 = []
matr2 = []

s = list(eval(input()))
n = len(s)

matr1.append(s)
for i in range(n - 1):
    matr1.append(list(eval(input())))
for i in range(n):
    matr2.append(list(eval(input())))

ans = [[0 for i in range(n)] for i in range(n)]
for i in range(n):
    for j in range(n):
        for t in range(n):
            ans[i][j] += matr1[i][t] * matr2[t][j]
for i in ans:
    print(*i, sep=',')