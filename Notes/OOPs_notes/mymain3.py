# Concept of Polymorphism

# example:
def test(a,b):
    return a+b
# one function but diff. output

print(test(12,65)) # doing addition

print(test('kiran','mun')) # doing concatination

# Polymorphism example 1 :

class insta:
    
    def share_stories(self):
        print('share my insta story')

class fbook:
    
    def share_stories(self):
        print('share my facebook story')

def shareStory(obj):
    obj.share_stories()

i = insta()
f = fbook()
shareStory(i)
shareStory(f)


# Polymorphism example 2 :

class social_media:

    def share_stories(self):
        print('share my story.')

    def upload_pic(self):
        print('upload my pics.')

class insta(social_media):

    def share_stories(self): # over-ridding
        print('share my insta story.')

class fbook(social_media):

    def share_stories(self): # over-ridding
        print('share my facebook story.')

i = insta()
f = fbook()

i.share_stories()
f.share_stories()
i.upload_pic()
f.upload_pic()


# Polymorphism example 2 :

# try to create your own exception class

class testException(Exception):

    def __init__(self, msg) -> None:
        self.msg = msg

try:
    raise(testException('raise my new exception'))
except testException as te:
    print('TE : ',te)

try:
    raise(testException('raise my new exception : zero se kon divide karata hai bhai...'))
    5/0
except testException as te:
    print('TE : ',te)


class testException1(Exception):

    def __init__(self, msg, my_val) -> None:
        self.msg = msg
        self.my_val = my_val

try:
    raise(testException1('raise my new exception with my value as error code : ', 156))
except testException1 as te:
    print('TE : ',te)

try:
    raise(testException1('raise my new exception with my value as error code : ', '404 - Page Not Found'))
except testException1 as te:
    print('TE : ',te)


