import sys


class dump(type):
    def __new__(metacls, name, parents, namespace, **flags):
        methods = [i for i in namespace if callable(namespace[i])]
        for n in methods:
            def new_method(self, *args, _ffun=namespace[n],
                           _ffname=n, **kwargs):
                print(f'{_ffname}: {args}, {kwargs}')
                return _ffun(self, *args, **kwargs)
            namespace[n] = new_method
        return super().__new__(metacls, name, parents, namespace)


exec(sys.stdin.read())
