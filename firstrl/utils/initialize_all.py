from functools import wraps
import inspect


def __intialize_all(self, pre, names, defaults, func, *args, **kargs):
    """
    Automatically assigns the parameters
    
    >>> class process:
    ...     @initialize_all_pre         (or @initialize_all_post)
    ...     def __init__(self, cmd, reachable=False, user='root'):
    ...         pass
    >>> p = process('halt', True)
    >>> p.cmd, p.reachable, p.user
    ('halt', True, 'root')
    """
    if pre:
        toReturn = func(self, *args, **kargs)
    for name, arg in list(zip(names[1:], args)) + list(kargs.items()):
        setattr(self, name, arg)
    
    for name, default in zip(reversed(names), reversed(defaults)):
        if not hasattr(self, name):
            setattr(self, name, default)
    if not pre :
        toReturn = func(self, *args, **kargs)
    return toReturn


def initialize_all_pre(func):

    names, _, _, defaults = inspect.getargspec(func)

    @wraps(func)
    def __wrapper(self, *args, **kargs):
        __intialize_all(self, True, names, defaults, func, *args, **kargs)

    return __wrapper


def initialize_all_post(func):

    names, _, _, defaults = inspect.getargspec(func)

    @wraps(func)
    def __wrapper(self, *args, **kargs):
        __intialize_all(self, False, names, defaults, func, *args, **kargs)

    return __wrapper
