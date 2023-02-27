import shlex

fio = input()
mesto = input()

print(shlex.join(["register", fio, mesto]))

print(shlex.split(shlex.join(["register", fio, mesto])))

res2 = input()
print(shlex.split(res2))