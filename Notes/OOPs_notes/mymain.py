class Emp:

    def __init__(self, name, salary, addr):

        self.name = name
        self.salary = salary
        self.addr = addr

    def printInfo(self):
        return f'The name of employ is {self.name}, salary is {self.salary} and address is {self.addr}. '

class Emp1:

    def printRoles(self, name, age):
        if age > 50:
            return f'The name of employ is {name} and role is sinear. '
        elif 50 > age > 30:
            return f'The name of employ is {name} and role is middel. '
        else:
            return f'The name of employ is {name} and role is low. '

class ListPrinter:

    def printList(self, l):
        if type(l) == list:
            for i in l:
                print(i)
        else:
            print(l,' : This is not a list.')

    def printReverce(self, l):
        if type(l) == list:
            return l[::-1]
        else:
            return f' {l} : This is not a list.'
        
        
my_emp1 = Emp('kiran', 60000, 'virar')
print(my_emp1.printInfo())

my_emp1 = Emp('karan', 70000, 'vasai')
print(my_emp1.printInfo())

my_emp1 = Emp1()
print(my_emp1.printRoles('kamal', 60))
print(my_emp1.printRoles('sham', 40))
print(my_emp1.printRoles('raju', 20))

mylist = [1,2,3,4,5,6,7]
l = ListPrinter()
l.printList(mylist)

print(l.printReverce(mylist))
