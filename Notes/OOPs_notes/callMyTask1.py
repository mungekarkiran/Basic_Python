import myTask1

d = myTask1.DictonaryParsing({1:2,3:4,5:6})
print(d.getKeys())
print(d.getValues())


from myTask1 import DictonaryParsing as dp

d = dp({11:12,13:14,15:16})
print(d.getKeys())
print(d.getValues())
