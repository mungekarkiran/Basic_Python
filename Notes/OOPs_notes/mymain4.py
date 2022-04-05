# static variable and static method in class using decoretors

class className:

    name = 'kiran' # static variable
    sal = 1000000
    def __init__(self, post, sal) -> None:
        self.post = post
        self.sal = sal

    def add_sal(self):
        self.sal = self.sal + 5000
        return self.sal

    @staticmethod  # static method
    def get_sal():
        return className.name, className.sal


c = className('abc', 20000)

print(className.get_sal())
print(c.add_sal())

c.sal = 12000
print(c.add_sal())

className.name = 'kamal'
className.sal = 450330
print(className.get_sal())