def hello():
    print('hello')
def add(a,b):
    print(a+b)
    
def in_add():
    a=int(input("enter:"))
    b=int(input("enter:"))
    print(a+b)
    hello()
def addd(a,b,c):
    return a+b,a+c,b+c
a=[1,2]
def list(x):
    print(x)
    for i in x:
        print(i,)
hello()
add(1,2)
in_add()
x,y,z=addd(1,2,3)
print(x,y,z)
list(a)
