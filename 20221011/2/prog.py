from math import *


inp = input().split()
w, h, a, b, func = int(inp[0]), int(inp[1]), float(
    inp[2]), float(inp[3]), lambda x: eval(inp[4])


image = [[' '] * w for i in range(h)]
i = a
y_val, x_val = [], []

while i < b:
    y_val.append(i)
    x_val.append(func(i))
    i += (b - a) / w

min_x, max_x = min(x_val), max(x_val)
scale = (h - 1) / (max_x - min_x)
x_val = [(x - min_x) * scale for x in x_val]
x_val = [h - 1 - int(x) for x in x_val]


new_x_val = []
for i in range(1, w):
    if abs(x_val[i - 1] - x_val[i]) > 1:
        for j in range(min(x_val[i - 1], x_val[i]),
                       max(x_val[i - 1], x_val[i])):
            new_x_val.append((i, j))
x_val = [(i, x_val[i]) for i in range(w)] + new_x_val
for x, y in x_val:
    image[y][x] = "*"
for row in image:
    print("".join(row))
