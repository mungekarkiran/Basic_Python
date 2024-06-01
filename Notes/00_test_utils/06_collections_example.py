# https://www.geeksforgeeks.org/python-collections-module/
# https://www.javatpoint.com/python-collection-module
# https://docs.python.org/3/library/collections.html
# https://www.naukri.com/code360/library/collections-module-in-python

from collections import Counter

l = ['a', 'b', 'c', 'b', 'c', 'b', 'a', 'a', 'b']

# Get count of each element
counter = Counter(l)
print(counter)

# Get most common element
print(counter.most_common(2))