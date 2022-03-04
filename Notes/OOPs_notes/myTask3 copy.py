'''
q1 - create a file class for reading data from respective file with a method name read and write. 
q2 - try to inherit read and write method form parent class to child class to perform read and write operation.
'''

import logging 

logging.basicConfig(filename="FileLogs.log", filemode='w', level=logging.DEBUG,format="%(asctime)s %(levelname)s %(message)s")

class MyFile:
    
    def __init__(self, fileName) -> None:
        self.fileName = fileName
        try:
            f = open(self.fileName, "x")
            f.close()
            # print(f'The file {self.fileName} is created by constructor. ')
            logging.info(f"Creating file instance varibale. \n The file {self.fileName} is created by constructor. ")
        except Exception as e:
            # print(f'Your file is not able to create by constructor : {e} ')
            logging.error(f'Your file is not able to create by constructor. ')
            logging.exception(f'Exception : {e} ')
        
    def readFile(self):
        logging.info(f"Executing the read method. ")
        try:
            f = open(self.fileName, 'r')
            print(f.read())
        except Exception as e:
            # print(f'Your file is not able to read : {e} ')
            logging.error(f'Your file is not able to read. ')
            logging.exception(f'Exception : {e} ')
        
    def writeFile(self, msg):
        logging.info(f"Executing the write method. ")
        try:
            f = open(self.fileName, 'w')
            # f = open(self.fileName, 'a')
            f.write(msg)
            f.close()
            # print(f'The file {self.fileName} is writen. ')
            logging.info(f"The file {self.fileName} is writen. ")
        except Exception as e:
            # print(f'Your file is not able to write : {e} ')
            logging.error(f'Your file is not able to write. ')
            logging.exception(f'Exception : {e} ')
        
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
