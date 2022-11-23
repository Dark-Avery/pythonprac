import sys
from string import ascii_lowercase


class Alpha:
    __slots__ = list(ascii_lowercase)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)

    def __str__(self):
        return ", ".join(f"{letter}: {self.__getattribute__(letter)}"
                         for letter in self.__slots__
                         if hasattr(self, letter))


class AlphaQ:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key in ascii_lowercase:
                self.__setattr__(key, value)
            else:
                raise AttributeError

    def __setattr__(self, key, value):
        if key in ascii_lowercase:
            self.__dict__[key] = value
        else:
            raise AttributeError

    def __str__(self):
        return ", ".join(f"{letter}: {self.__getattribute__(letter)}"
                         for letter in ascii_lowercase
                         if hasattr(self, letter))


exec(sys.stdin.read())

