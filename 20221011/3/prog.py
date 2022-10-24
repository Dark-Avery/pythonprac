try:
    wall = input()
    gas = 0
    liq = 0
    wid = 2
    while (inp := input()) != wall:
        gas += sum(1 for i in inp if i == '.')
        liq += sum(1 for i in inp if i == '~')
        wid += 1
except EOFError:
    pass
print('#' * wid)
liq_r = (liq + wid - 3) // (wid - 2)
gas_r = len(wall) - 2 - liq_r

for i in range(gas_r):
    print('#' + '.' * (wid - 2) + '#')
for i in range(liq_r):
    print('#' + '~' * (wid - 2) + '#')

print('#' * wid)

if gas < liq:
    len_row = round(gas / liq * 20)
    print('.' * len_row + ' ' + f'{gas:>{len(str(liq)) + 20 - len_row}}' + '/' + str(gas + liq))
    print('~' * 20 + ' ' + str(liq) + '/' + str(gas + liq))
else:
    len_row = round(liq / gas * 20)
    print('.' * 20 + ' ' + str(gas) + '/' + str(gas + liq))
    print('~' * len_row + ' ' + f'{liq:>{len(str(gas)) + 20 - len_row}}' + '/' + str(gas + liq))
