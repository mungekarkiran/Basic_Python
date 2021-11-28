#a=1
#b=2
#a,b=2,1
a=int(input('Enter a:'))
b=int(input('Enter b:'))
c=int(input('Enter c:'))
#b=int(input('Enter b:'))
if a>b & a>c:
    print(a,'a is greater')
elif b>c:
    print(b,'b is greater')
else:
    print(c,'c is greater')
print('hello %02d wel'%a)
print('hello %s wel'%a)
