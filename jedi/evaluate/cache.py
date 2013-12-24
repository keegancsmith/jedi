"""
- the popular ``memoize_default`` works like a typical memoize and returns the
  default otherwise.
- ``CachedMetaClass`` uses ``memoize_default`` to do the same with classes.
"""


def memoize_default(default, cache_is_in_self=False):
    """ This is a typical memoization decorator, BUT there is one difference:
    To prevent recursion it sets defaults.

    Preventing recursion is in this case the much bigger use than speed. I
    don't think, that there is a big speed difference, but there are many cases
    where recursion could happen (think about a = b; b = a).
    """
    def func(function):
        def wrapper(obj, *args, **kwargs):
            if cache_is_in_self:
                cache = obj.memoize_cache
            else:
                cache = obj._evaluator.memoize_cache

            try:
                memo = cache[function]
            except KeyError:
                memo = {}
                cache[function] = function

            key = (args, frozenset(kwargs.items()))
            if key in memo:
                return memo[key]
            else:
                memo[key] = default
                rv = function(obj, *args, **kwargs)
                memo[key] = rv
                return rv
        return wrapper
    return func


class CachedMetaClass(type):
    """ This is basically almost the same than the decorator above, it just
    caches class initializations. I haven't found any other way, so I do it
    with meta classes.
    """
    @memoize_default(None)
    def __call__(self, *args, **kwargs):
        return super(CachedMetaClass, self).__call__(*args, **kwargs)
