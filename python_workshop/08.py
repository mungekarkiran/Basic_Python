a=int(input('enter number of people'))
b=int(input('enter number of cars'))
c=int(input('enter number of truck'))
cc=60
bb=5
aa=bb*b
ccc=cc*c
if a<bb or a<aa:
    print('go in car')
elif a<cc or a<=ccc:
    print('go in truck')
else:
    print('vehicle not avalible')
