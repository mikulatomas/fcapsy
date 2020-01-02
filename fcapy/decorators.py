def info(display_name):
    def wrapper(func):
        setattr(func, 'display_name', display_name)
        return func
    return wrapper
