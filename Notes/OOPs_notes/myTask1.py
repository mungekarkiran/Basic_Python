'''
create a class for dictonary parsing 

1 . write a functoin to give all the keys
2 . write a function to give all the values 
3 . write a function to throw an exception in case of input is not dictonary
4 . write a function to take user input and then parse a key and value out of dictonary 
5 . write a function to insert new key value pair into dictonary 
'''

class DictonaryParsing:

    def __init__(self, d) -> None:
        print(f'Constructor is created for DictonaryParsing !!! ')
        self.dict1 = d
    
    def checkDict(self):
        if type(self.dict1) == dict:
            return 1
        else:
            raise Exception(f'{self.dict1}, is not a Dictonary. ')

    def getKeys(self):
        if self.checkDict():
            return list(self.dict1.keys())

    def getValues(self):
        if self.checkDict():
            return list(self.dict1.values())

    def userInput(self):
        self.dict1 = eval(input('Please enter a Dictonary : '))
        try:
            if self.checkDict():
                print(f'Keys : {self.getKeys()} ')
                print(f'Values : {self.getValues()} ')
        except Exception as e:
            print(e)

    def insertValue(self,key,val):
        self.dict1[key] = val
        print(f'Value inserted : {self.dict1}. ')

    def insertValue1(self,**kw): # **kwargs
        for k,v in kw.items():
            self.dict1[k] = v
        print(f'Value inserted : {self.dict1}. ')


# d1 = DictonaryParsing({1:2,3:4,5:6})

# d1_keys = d1.getKeys()
# print(f'Keys: {d1_keys} ')

# d1_values = d1.getValues()
# print(f'Values: {d1_values} ')

# d2 = DictonaryParsing([1,2,3,4])
# try:
#     print(d2.checkDict())
# except Exception as e:
#     print(e)

# d1.userInput()

# d1.insertValue('q','w')

# d1.insertValue1(e='r', e1='r1', e2='r2',e3='r3',e4='r4')