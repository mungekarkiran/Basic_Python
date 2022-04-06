# Overload and Override

class test:

    def fun(self):
        print('this is my sample class.')


t = test()
print(t) # <__main__.test object at 0x000002981FC61250>


class test1:

    def fun(self):
        print('this is my sample class.')

    def __str__(self) -> str: # overloading of __str__ method 
        return 'this is function called at the time of object print.'

t = test1()
print(t) # this is function called at the time of object print.

# or 

def fun(*args): 
    return args

# overloading of fun function
print(fun(1,2,3,4,5,6,7,8))
print(fun('a','s','d','f','g','h','j','k','l'))



# overriding 

class test11:

    def car(self):
        print('this is car from test11 class.')

class test12(test11):

    def car(self): # overriding the car method.
        print('this is car from test12 class.')

t11 = test11()
t12 = test12()
for obj in (t11, t12):
    obj.car()