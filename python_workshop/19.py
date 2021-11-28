def fac(num):
    
    if num==1:
        return 1
    else:
        return num*fac(num-1)
def max():
    a=list(input('Enter list :'))
    a.sort()
    print(a[len(a)-1])
def fibo():
    print('Fibbo')
    t=0
    t1=1
    print(0)
    print(1)
    x=1
    while x<5:
         c=t+t1
         print(c)
         t=t1
         t1=c
         x+=1
a=int(input('Enter number'))
fac(a)
print(fac(a))
max()        
fibo()
