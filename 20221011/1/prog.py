from fractions import Fraction

def is_polynom(line):
    s, w, pow_a = line[0], line[1], int(line[2])
    line = line[3:]
    pow = pow_a
    A = Fraction(0)
    for i in range(pow_a + 1):
        A += Fraction(line[i]) * Fraction(s) ** pow
        pow -= 1

    pow_B = int(line[pow_a + 1])
    line = line[pow_a + 2:]
    B = Fraction(0)
    pow = pow_B
    for i in range(pow_B + 1):
        B += Fraction(line[i]) * Fraction(s) ** pow
        pow -= 1
    return A / B == Fraction(w) if B else False


line = [Fraction(x) for x in input().split(",")]
print(is_polynom(line))