import sys
import inspect
import typing


class check(type):
    def __init__(cls, name, parents, namespace, **flags):
        def new_fun(self):
            annotat = inspect.get_annotations(self.__class__)
            for n in annotat:
                try:
                    attr = getattr(self, n)
                except AttributeError:
                    return False
                atype = (annotat[n]
                         if typing.get_origin(annotat[n]) is None
                         else typing.get_origin(annotat[n]))
                if not isinstance(attr, atype):
                    return False
            return True
        setattr(cls, 'check_annotations', new_fun)
        return super().__init__(name, parents, namespace)


exec(sys.stdin.read())
