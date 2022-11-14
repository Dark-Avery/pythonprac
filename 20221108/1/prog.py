import collections
import sys


class DivStr(collections.UserString):
    def __init__(self, seq=""):
        super().__init__(seq)

    def __floordiv__(self, other):
        n = len(self) // other
        return iter(self[k:k + n] for k in range(0, other * n, n))

    def __mod__(self, other):
        n = len(self) % other
        return self[-n:]


exec(sys.stdin.read())
