from itertools import islice
from itertools import tee

def slide(seq, n):
    s = seq
    while True:
        seq = iter(seq)
        s, seq = tee(s)
        win = list(islice(seq, n))
        if len(win) < 1:
            return
        yield from win
        next(s)

import sys
exec(sys.stdin.read())