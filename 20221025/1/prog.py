def fib(m, n):
	a, b = 1, 1
	for i in range(m):
		a, b = b, a + b
	for i in range(n - m + 1):
		yield a
		a, b = b, a + b

import sys
exec(sys.stdin.read())