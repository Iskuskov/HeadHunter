# -*- coding: utf-8

__author__ = 'iskuskov'
__email__ = 'iskuskov@gmail.com'

import sys

def memoize(obj):
    '''Мемоизация.'''
    cache = {}

    def memoizer(*args, **kwargs):
        if args not in cache:
            cache[args] = obj(*args, **kwargs)
        return cache[args]
    return memoizer

@memoize
def partition_count(n, k):
    '''Возвращает число разбиений числа n на k слагаемых.'''
    
    # База рекурсии
    if (k == n or k == 1):
        return 1
    if (k > n):
        return 0
    
    # Рекурсия
    return partition_count(n - 1, k - 1) + partition_count(n - k, k)

def main():
    try:
        if len(sys.argv) == 3:
            n, k = int(sys.argv[1]), int(sys.argv[2])
        else:
            n, k = [int(n) for n in raw_input('').split()]
    except ValueError:
        print "Could not convert data to an integer."
        sys.exit(1)
        
    print(partition_count(n, k))

if __name__ == "__main__":
    main()