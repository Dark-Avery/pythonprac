import sys


class Grange:
    def __init__(self, b0, q, bn):
        self.b0, self.q, self.bn = b0, q, bn
        elem = b0
        seq = []
        while elem < bn:
            seq.append(elem)
            elem *= q
        self.seq = seq

    def __len__(self):
        return len(self.seq)

    def __bool__(self):
        return bool(len(self))

    def __iter__(self):
        return iter(self.seq)

    def __str__(self):
        return f"grange({self.b0}, {self.q}, {self.bn})"

    __repr__ = __str__

    def __getitem__(self, key):
        if type(key) == int:
            return self.b0 * self.q**key
        elif type(key) == slice:
            return Grange(key.start,
                          self.q**key.step if key.step else self.q,
                          key.stop)


exec(sys.stdin.read())
