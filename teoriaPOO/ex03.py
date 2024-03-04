# Encapsulamento
class Foo:
    def __init__(self, x):
        self._x = x
    
    @property
    def x(self):
        return self.x or 0
    
    @x.setter
    def x(self, value):
        self._x += value

    @x.deleter
    def x(self):
        self._x = -1

foo = Foo(10)
print(foo.x)
foo.x = 99
print(foo.x)
