class InvalidInput(Exception):
    pass


class BadTriangle(Exception):
    pass


def triangleSquare(inStr):
    try:
        (x1, y1), (x2, y2), (x3, y3) = eval(inStr)
    except Exception:
        raise InvalidInput
    for c in [x1, y1, x2, y2, x3, y3]:
        if not isinstance(c, int) and not isinstance(c, float):
            raise BadTriangle
    ans = abs(0.5*(x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2)))
    if ans <= 0:
        raise BadTriangle
    return ans


while (buf := input()):
    try:
        ans = triangleSquare(buf)
    except InvalidInput:
        print('Invalid input')
    except BadTriangle:
        print('Not a triangle')
    else:
        print('{0:.2f}'.format(ans))
