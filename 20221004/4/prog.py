from math import *

def Calc(s, t, u):
    S = lambda x: eval(s)
    T = lambda x: eval(t)
    U = lambda x, y: eval(u)
    return lambda x: U(S(x), T(x))

F = Calc(*eval(input()))
print(F(eval(input())))
