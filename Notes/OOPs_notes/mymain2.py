# Concept of Public, Private and Protected

# ======================= Public


class C1:
    
    def __init__(self, a, b, c) -> None:
        self.a = a
        self.b = b
        self.c = c

class C2(C1):
    pass

z = C2(1,2,3)
print(z.a, z.b, z.c)
z.c = 100
print(z.a, z.b, z.c)



# ======================= Protected
class C3:
    
    def __init__(self, a, b, c) -> None:
        self._a = a
        self.b = b
        self.c = c

class C4(C3):
    
    def __init__(self, a,b,c) -> None:
        C3.__init__(self, a,b,c)
        self._a = 10

class C5(C4):
    pass

z = C4(1,2,3)
print(z._a, z.b, z.c)
z._a = 100
print(z._a, z.b, z.c)

z1 = C4(1,2,3)
z1._a = 50
print(z1._a, z1.b, z1.c)


# ======================= Private
class C6:

    def __init__(self, a,b,c) -> None:
        self.__a = a
        self.b = b
        self.c = c
        
class C7(C6):

    def __init__(self, a, b, c) -> None:
        super().__init__(a, b, c)
        self.__a = 25

try:
    z = C7(1,2,3)
    z.__a = 100
    print(z._a, z.b, z.c)
except Exception as e:
    print(e)


# ======================= Test all

class C8:

    def __init__(self, a,b,c) -> None:
        self.__a = a
        self._b = b
        self.c = c

class C9(C8):
    pass

x1 = C8(1,2,3)
x2 = C9(1,2,3)

try:
    print(x1.__a)
    print(x1._b)
    print(x1.c)
except Exception as e:
    print(e)

try:
    print(x1._C8__a)
    print(x1._b)
    print(x1.c)
except Exception as e:
    print(e)

x1.__a = 10
x1._b = 20
x1.c = 30

print(x1.__a)
print(x1._b)
print(x1.c)



try:
    print(x2.__a)
    print(x2._b)
    print(x2.c)
except Exception as e:
    print(e)

try:
    print(x2._C8__a)
    print(x2._b)
    print(x2.c)
except Exception as e:
    print(e)

x2.__a = 10
x2._b = 20
x2.c = 30

print(x2.__a)
print(x2._b)
print(x2.c)


# ======================= Test 1

class BonousCalculator:

    def __init__(self, empid, emprating) -> None:
        self.empid = empid
        self.emprating = emprating
        self.__bonousforratingA = '70%'
        self.__bonousforratingB = '60%'
        self.__bonousforratingC = '50%'

    def bonouscalculator(self):
        if self.emprating == 'A':
            return 'You get '+self.__bonousforratingA
        elif self.emprating == 'B':
            return 'You get '+self.__bonousforratingB
        elif self.emprating == 'C':
            return 'You get '+self.__bonousforratingC
        else:
            return 'You get Nothing !!!'

emp = BonousCalculator(101, 'A') 
print(emp.bonouscalculator())

emp = BonousCalculator(102, 'B') 
print(emp.bonouscalculator())

emp = BonousCalculator(103, 'C') 
print(emp.bonouscalculator())

emp = BonousCalculator(104, 'D') 
print(emp.bonouscalculator())

emp = BonousCalculator(106, 'B')
emp.__bonousforratingB = '90%' 
print(emp.bonouscalculator())

# We can modify the private variable using its class name only
emp._BonousCalculator__bonousforratingB = '90%' 
print(emp.bonouscalculator())