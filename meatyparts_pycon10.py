#! /usr/bin/env python

def foo():
    print("Hello World!")

def add_10(x):
    """
    adds 10 to the input value
    >>> add_10(5)
    15
    >>> add_10(-2)
    8
    """
    return x + 10

class C: pass

c = C()

def bar(x):
    """
    >>> c #doctest: +ELLIPSIS
    <__main__.C instance at 0x...>
    """
    if x:
        print "a"
    else:
        print "b"

def named_param(a, foo=[]):
    if not foo:
        foo.append(a)
    # return foo


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    # doctest.testfile('meatyparts_pycon10.py')
    
 
