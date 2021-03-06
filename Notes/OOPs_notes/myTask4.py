'''
q1 - create your own class to achive multipal, multilevel inharitance
q2 - create your own class to represent polymorphism
q3 - create your own class for custom exception 
q4 - create your own class to achive encapsulation
q5 - create your own class to achive method overloading and overriding.
'''

# q1 - create your own class to achive multipal, multilevel inharitance
# multipal inharitance
class p1:

    def __init__(self, a, b) -> None:
        self.a = a
        self.b = b

    def add_num(self):
        return self.a + self.b

    def sub_num(self):
        return self.a - self.b

class p2:

    def __init__(self, p, q) -> None:
        self.p = p
        self.q = q

    def mul_num(self):
        return self.p * self.q

    def div_num(self):
        return self.p / self.q
    
class my_math(p1, p2):

    def __init__(self, a, b) -> None:
        self.data1 = a
        self.data2 = b
        p1.__init__(self, self.data1, self.data2)
        p2.__init__(self, self.data1, self.data2)

    def call_math(self):
        self.add = self.add_num()
        self.sub = self.sub_num()
        self.mul = self.mul_num()
        self.div = self.div_num()
        return self.add, self.sub, self.mul, self.div 

mm = my_math(24, 2)
print(mm.call_math())


# multi-level inharitance
class q1:

    def __init__(self, a, b, c) -> None:
        self.a, self.b, self.c = a, b, c

    def add_num(self):
        return self.a + self.b + self.c

    def sub_num(self):
        return self.a - self.b - self.c

class q2(q1):

    def __init__(self, a, b, c) -> None:
        # q1.__init__(a, b, c)
        super().__init__(a, b, c)

        self.a, self.b, self.c = a, b, c

    def mul_num(self):
        return self.a * self.b * self.c 

    def div_num(self):
        return self.a / self.b / self.c
    
class my_math(q2):

    def __init__(self, a, b, c) -> None:
        # q2.__init__(a, b, c)
        super().__init__(a, b, c)

    def call_math(self):
        return self.add_num(), self.sub_num(), self.mul_num(), self.div_num()

mm1 = my_math(12, 13, 14)
print(mm1.call_math())


# q2 - create your own class to represent polymorphism

class about_me:

    def print_something(self):
        return 'I am an animal from earth.'

class my_sound:

    def my_voice(self):
        return 'I have normal voice.'

class dog(about_me, my_sound):

    def __init__(self) -> None:
        super().__init__()

    def my_voice(self):
        return 'I have woof-woof voice.'

class cat(about_me, my_sound):

    def __init__(self) -> None:
        super().__init__()

    def my_voice(self):
        return 'I have meow-meow voice.'

d = dog()
c = cat()

print(d.print_something(), '\n', d.my_voice() )
print(c.print_something(), '\n', c.my_voice() )

# or 

for obj in (d, c):
    print(obj.print_something(), '\n', obj.my_voice() )



# q3 - create your own class for custom exception 

class divide_by_5(Exception):

    def __init__(self, msg) -> None:
        self.msg = msg
    
try:
    a =int(input('Enter a value for "a" : '))
    b =int(input('Enter a value for "b" : '))

    if b == 5:
        raise(divide_by_5('Not able to divide by 5 '))

except ValueError as ve:
    print('ValueError : ',ve)

except divide_by_5 as d5:
    print(d5)

else:
    try:
        print(a/b)
    except ZeroDivisionError as ze:
        print('ZeroDivisionError : ',ze)