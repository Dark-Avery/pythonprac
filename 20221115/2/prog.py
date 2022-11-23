import sys


class Num:
    def __get__(self, obj, cls):
        if not hasattr(obj, '_value'):
            obj._value = 0
        return obj._value

    def __set__(self, obj, val):
        if hasattr(val, 'real'):
            obj._value = val.real
        elif hasattr(val, '__len__'):
            obj._value = len(val)

    def __delete__(self, obj):
        del obj._value


exec(sys.stdin.read())
