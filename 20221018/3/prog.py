from string import punctuation
try:
    d = {}
    w = int(input())


    while (inp := input()):
        for i in punctuation:
            inp = inp.replace(i, " ")
        for i in inp.split():
            if len(i) == w and i.isalpha():
                d.setdefault(i.lower(), 0)
                d[i.lower()] += 1
except EOFError:
    pass

max = max(d.items(), key = lambda x: x[1])[1]
print(*sorted(i for i in d if d[i] == max))