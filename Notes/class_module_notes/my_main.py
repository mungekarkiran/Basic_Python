from pkg1 import pkg1test1
from pkg1 import pkg1test2
from pkg1 import pkg1test3
from pkg2 import pkg2test1
from pkg2 import pkg2test2

import sys


if __name__ == '__main__':
    
    print(sys.path)

    pkg1test1.test1()

    pkg1test2.test2()

    pkg1test3.test3()

    pkg2test1.test4()
    
    pkg2test2.test5()

    