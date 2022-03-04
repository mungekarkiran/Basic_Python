'''
q1 - create a file class for reading data from respective file with a method name read and write. 
q2 - try to inherit read and write method form parent class to child class to perform read and write operation.
'''

class MyFile:
    
    def __init__(self, fileName) -> None:
        self.fileName = fileName
        try:
            f = open(self.fileName, "x")
            f.close()
            print(f'The file {self.fileName} is created by constructor. ')
        except Exception as e:
            print(f'Your file is not able to create by constructor : {e} ')
        
    def readFile(self):
        try:
            f = open(self.fileName, 'r')
            print(f.read())
        except Exception as e:
            print(f'Your file is not able to read : {e} ')
        
    def writeFile(self, msg):
        try:
            f = open(self.fileName, 'w')
            f.write(msg)
            f.close()
            print(f'The file {self.fileName} is writen. ')
        except Exception as e:
            print(f'Your file is not able to write : {e} ')
        
mf = MyFile('test1.txt')
mf.writeFile('Hello Kiran !!! \n Welcome to file test1.')
mf.readFile()

mf = MyFile('test2.txt')
mf.writeFile('Hello Kiran !!! \n Welcome to file test2.')
mf.readFile()

class MyFileC1(MyFile):
    pass

mf = MyFileC1('test3.txt')
mf.writeFile('Hello Kiran !!! \n Welcome to file test3.')
mf.readFile()

mf = MyFileC1('test4.txt')
mf.writeFile('Hello Kiran !!! \n Welcome to file test4.')
mf.readFile()
