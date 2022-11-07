from math import sqrt
import sys


class Triangle:
    def __init__(self, x1, x2, x3):
        self.a, self.b, self.c = x1, x2, x3
        self.ab = sqrt((self.a[0] - self.b[0])**2 + (self.a[1] - self.b[1])**2)
        self.bc = sqrt((self.b[0] - self.c[0])**2 + (self.b[1] - self.c[1])**2)
        self.ca = sqrt((self.c[0] - self.a[0])**2 + (self.c[1] - self.a[1])**2)

    def __abs__(self):
        if max(self.ab, self.bc, self.ca) >= \
                min(self.ab + self.bc, self.bc + self.ca, self.ca + self.ab):
            return 0
        return abs(0.5*(self.a[0]*(self.b[1]-self.c[1]) +
                        self.b[0]*(self.c[1]-self.a[1]) +
                        self.c[0]*(self.a[1]-self.b[1])))

    def __bool__(self):
        return bool(abs(self))

    def __lt__(self, other):
        return abs(self) < abs(other)

    def __contains__(self, other):
        if not other:
            return True
        if self < other:
            return False
        tmp = []
        for x, y in (other.a, other.b, other.c):
            x0, y0 = self.a
            x1, y1 = self.b
            x2, y2 = self.c
            a = (x0 - x) * (y1 - y0) - (x1 - x0) * (y0 - y)
            b = (x1 - x) * (y2 - y1) - (x2 - x1) * (y1 - y)
            c = (x2 - x) * (y0 - y2) - (x0 - x2) * (y2 - y)
            tmp.append(a * b >= 0 and b * c >= 0 and a * c >= 0)
        return all(tmp)

    def __and__(self, other):
        if not other or not self:
            return False
        tmp1 = []
        for x, y in (other.a, other.b, other.c):
            x0, y0 = self.a
            x1, y1 = self.b
            x2, y2 = self.c
            a = (x0 - x) * (y1 - y0) - (x1 - x0) * (y0 - y)
            b = (x1 - x) * (y2 - y1) - (x2 - x1) * (y1 - y)
            c = (x2 - x) * (y0 - y2) - (x1 - x0) * (y2 - y)
            tmp1.append(a * b > 0 or b * c > 0)
        tmp2 = []
        for x, y in (self.a, self.b, self.c):
            x0, y0 = other.a
            x1, y1 = other.b
            x2, y2 = other.c
            a = (x0 - x) * (y1 - y0) - (x1 - x0) * (y0 - y)
            b = (x1 - x) * (y2 - y1) - (x2 - x1) * (y1 - y)
            c = (x2 - x) * (y0 - y2) - (x1 - x0) * (y2 - y)
            tmp2.append(a * b > 0 or b * c > 0)
        return any(tmp1) or any(tmp2)


exec(sys.stdin.read())
