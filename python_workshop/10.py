password='ht'
x=1
while True:
    a=str(input('ENter passwrd:'))
    if(password==a):
        print('loged in')
        break
    else:
        x+=1
    if x == 4:
        break
