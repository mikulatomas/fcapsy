# Decorators for easier formatting of output

def metadata(name, short_name=None, latex=None):
    def wrapper(func):
        setattr(func, 'name', name)

        if short_name is None:
            setattr(func, 'short_name', name)

            if latex is None:
                setattr(func, 'latex', name)
            else:
                setattr(func, 'latex', latex)
        else:
            setattr(func, 'short_name', short_name)

            if latex is None:
                setattr(func, 'latex', short_name)
            else:
                setattr(func, 'latex', latex)

        return func
    return wrapper
