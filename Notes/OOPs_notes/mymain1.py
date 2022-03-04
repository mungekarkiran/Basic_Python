# Concept of Inheritance

class C1:

    def __init__(self, a, b, c) -> None:
        self.a = a
        self.b = b
        self.c = c
        
    def m1(self):
        print('Method 1 from class 1')
    
    def m2(self):
        print('Method 2 from class 1')

    def m3(self):
        print('Method 3 from class 1')

class C2(C1):
    pass

c = C2(1,2,3)
c.m1()
c.m2()
c.m3()

# ====================================================

class C3:

    def __init__(self, a, b, c) -> None:
        self.a = a
        self.b = b
        self.c = c
        
    def m1(self):
        print('Method 1 from class 3')
    
    def m2(self):
        print('Method 2 from class 3')

    def m3(self):
        print('Method 3 from class 3')

class C4(C3):
    
    def __init__(self, a, b, c) -> None:
        super().__init__(a, b, c)

    def m1(self):
        print('Method 1 from class 4')

c = C4(1,2,3)
c.m1()
c.m2()
c.m3()


# ====================================================


class C5:

    def __init__(self, a, b, c) -> None:
        self.a = a
        self.b = b
        self.c = c
        
    def m1(self):
        print('Method 1 from class 5')
    
    def m2(self):
        print('Method 2 from class 5')

    def m3(self):
        print('Method 3 from class 5')


class C6:

    def __init__(self, p, q, r) -> None:
        self.p = p
        self.q = q
        self.r = r
        
    def m4(self):
        print('Method 4 from class 6')
    
    def m5(self):
        print('Method 5 from class 6')

    def m6(self):
        print('Method 6 from class 6')


class C7(C5, C6):
    pass

c = C7(1,2,3)
try:
    print(c.a,c.b,c.c)
except Exception as e:
    print(e)
c.m1(), c.m2(), c.m3(), c.m4(), c.m5(), c.m6() 
try:
    print(c.p,c.q,c.r)
except Exception as e:
    print(e)


# Multipal Inheritance

class C8(C6, C5):
    pass

c = C8(1,2,3)
try:
    print(c.a,c.b,c.c)
except Exception as e:
    print(e)
c.m1(), c.m2(), c.m3(), c.m4(), c.m5(), c.m6()
try:
    print(c.p,c.q,c.r)
except Exception as e:
    print(e)


# ====================================================

# Multipal Inheritance

class C9(C6, C5):
    def __init__(self, *args, **kwargs) -> None:
        C6.__init__(self, *args)
        C5.__init__(self, **kwargs)

c = C9(1, 2, 3, a=12, b=23, c=34)
try:
    print(c.a,c.b,c.c)
except Exception as e:
    print(e)
c.m1(), c.m2(), c.m3(), c.m4(), c.m5(), c.m6()
try:
    print(c.p,c.q,c.r)
except Exception as e:
    print(e)


# ====================================================

# Multi-Level Inheritance

class C10:
    def __init__(self, a, b, c) -> None:
        self.a = a
        self.b = b
        self.c = c
        
    def m1(self):
        print('Method 1 from class 10')
    

class C11(C10):
        
    def m2(self):
        print('Method 2 from class 11')


class C12(C11):
        
    def m3(self):
        print('Method 3 from class 12')
        
c = C12(111,222,333)
print(c.a,c.b,c.c)
c.m1(), c.m2(), c.m3()


# ====================================================


