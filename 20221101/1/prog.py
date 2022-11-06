import sys


class Omnibus:
    attr = {}

    def __setattr__(self, a, v):
        if not a.startswith("_"):
            self.attr.setdefault(a, set())
            self.attr[a].add(self)

    def __getattr__(self, a):
        if not a.startswith("_"):
            return len(self.attr[a])

    def __delattr__(self, a):
        if self in self.attr.get(a, set()):
            self.attr[a] -= {self}


exec(sys.stdin.read())
