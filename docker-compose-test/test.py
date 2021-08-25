class Foo(object):
    def __init__(self):
        self.func()
    def func(self):
        print('in foo')

class Son(Foo):
    def func(self):
        print('in son')
Son()

class Foo(object):
    def __init__(self):
        self.__func() # self._Foo__func() 
    def __func(self):
        print('in foo')

class Son(Foo):
    def __func(self):
        print('in son')
Son() 