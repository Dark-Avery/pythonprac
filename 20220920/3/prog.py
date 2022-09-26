n = int(input())

i = n
while i <= n+2:
    j = n
    while j <= n+2:
        mult = i * j
        sum = 0
        while mult > 0:
            sum += mult % 10
            mult //= 10
        print(i, ' * ', j, ' = ', ':=)' if sum == 6 else i*j, end = ' ')
        j += 1
    print()
    i += 1