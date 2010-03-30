#!/usr/bin/env python

"""Utility to persistently cache results of callables."""

# =============================================================================

import hashlib
from os.path import exists
import shelve
import sys
import time

# =============================================================================

class Cache(object):
    
    def __init__(self, fname, repr=repr):
        """Create a new persistent cache using the given file name.
        
        The keyword `repr` may specify an alternative representation function
        to be applied to the arguments of callables to cache. The
        representation function is used to calculate a hash of the arguments.
        Representation functions need to differentiate argument values
        sufficiently (for the purpose of the callable) and identically across
        different invocations of the Python interpreter. The default
        representation function `repr()` is suitable for basic types, lists,
        tuples and combinations of them as well as for all types which
        implement the `__repr__()` method according to the requirements
        mentioned above.
        
        """
        self.__repr = repr
        self.__cache = shelve.open(fname, protocol=-1)
        
    def check(self, fn):
        """Decorator function for caching results of a callable."""
        
        def wrapper(*args, **kwargs):
            """Function wrapping the decorated function."""
            
            ckey = hashlib.sha1(fn.__name__) # parameter hash
            for a in args:
                ckey.update(self.__repr(a))
            for k in sorted(kwargs):
                ckey.update("%s:%s" % (k, self.__repr(kwargs[k])))
            ckey = ckey.hexdigest()
            
            if ckey in self.__cache:
                result = self.__cache[ckey]
            else:
                result = fn(*args, **kwargs)
                self.__cache[ckey] = result
            self.__cache["%s:atime" % ckey] = time.time() # access time
            return result
            
        return wrapper

    def close(self):
        """Close cache and save it to disk."""
        
        self.__cache.close()
        
    def clear(self, maxage=0):
        """Clear all cached results or those not used for `maxage` seconds."""

        if maxage > 0:
            outdated = []
            bigbang = time.time() - maxage
            for key in self.__cache:
                if key.endswith(":atime") and self.__cache[key] < bigbang:
                    outdated.append(key)
                    outdated.append(key.rsplit(":", 1)[0])
    
            for key in outdated:
                del self.__cache[key]
        else:
            self.__cache.clear()
        
    def _stats(self):
        """Get some statistics about this cache.
        
        Returns a 3-tuple containing the number of cached results as well as
        the oldest and most recent result usage times (in seconds since epoch).
          
        """
        num = 0
        oldest = time.time()
        newest = 0
        for key in self.__cache:
            if key.endswith(":atime"):
                num += 1
                oldest = min(oldest, self.__cache[key])
                newest = max(newest, self.__cache[key])
        return num, oldest, newest

# =============================================================================
# Command line functionality
# =============================================================================

def _main():

    def age(s):
        """Pretty-print an age given in seconds."""
        
        m, h, d = s // 60, s // 3600, s // 86400
        for val, unit in ((d, "d"), (h, "h"), (m, "m"), (s, "s")):
            if val > 1 or unit == "s":
                return "%d%s" % (val, unit)

    if len(sys.argv) != 2:
        print("Usage: %s CACHEFILE" % sys.argv[0])
        sys.exit(1)

    if not exists(sys.argv[1]):
        print("no such cache file")
        sys.exit(1)

    c = Cache(sys.argv[1])
    now = time.time()
    num, oldest, newest = c._stats()
    print("Number of cached results : %d" % num)
    print("Oldest result usage age  : %s" % age(now - oldest))
    print("Latest result usage age  : %s" % age(now - oldest))

if __name__ == '__main__':
    _main()