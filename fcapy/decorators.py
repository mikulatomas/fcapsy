# Decorators for easier formatting of output

def metadata(name, short_name=None):
    def wrapper(func):
        setattr(func, 'name', name)
        if short_name is None:
            setattr(func, 'short_name', name)
        else:
            setattr(func, 'short_name', short_name)
        return func
    return wrapper
