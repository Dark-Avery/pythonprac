import sys


class Triangle:
    def __init__(self, x1, x2, x3):
        self.a, self.b, self.c = x1, x2, x3
        self.ab = ((self.a[0] - self.b[0])**2 +
                   (self.a[1] - self.b[1])**2)**0.5
        self.bc = ((self.b[0] - self.c[0])**2 +
                   (self.b[1] - self.c[1])**2)**0.5
        self.ca = ((self.c[0] - self.a[0])**2 +
                   (self.c[1] - self.a[1])**2)**0.5

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
        if self in other or other in self:
            return True
        tmp = []
        for x in [(self.a, self.b),
                  (self.b, self.c),
                  (self.c, self.a)]:
            for y in [(other.a, other.b),
                      (other.b, other.c),
                      (other.c, other.a)]:
                a = (x[1][0] - x[0][0]) * (x[0][1] - y[0][1]) - \
                    (x[1][1] - x[0][1]) * (x[0][0] - y[0][0])
                b = (y[1][0] - y[0][0]) * (x[0][1] - y[0][1]) - \
                    (y[1][1] - y[0][1]) * (x[0][0] - y[0][0])
                n = (x[1][0] - x[0][0]) * (y[1][1] - y[0][1]) - \
                    (x[1][1] - x[0][1]) * (y[1][0] - y[0][0])
                if n == 0:
                    tmp.append(False)
                else:
                    tmp.append((0 < a / n < 1) and (0 < b / n < 1))
        return any(tmp)


exec(sys.stdin.read())
