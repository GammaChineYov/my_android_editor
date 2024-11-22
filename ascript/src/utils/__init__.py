from functools import wraps
from .rect import Rect
from .config_util import Config


import traceback

def singleton(cls):
    instances = {}
    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper


class SingletonMeta(type):
    """
    单例模式的元类
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


def thread_decorator(on_start=None, on_stop=None):
    import threading
    from functools import wraps
    def actual_decorator(func):
        def execute_with_stop(*args, **kwargs):
            result = None
            try:
                if on_start:
                    on_start(thread)
            except:
                traceback.print_exc()
            try:
                result = func(*args, **kwargs)
            except:
                traceback.print_exc()
            try:
                if on_stop_callback:
                    on_stop_callback()
            except:
                traceback.print_exc()
            return result
        @wraps(func)
        def wrapper(*args, **kwargs):
            thread = threading.Thread(target=execute_with_stop, args=args, kwargs=kwargs)
            thread.start()
            return thread
        return wrapper
    
    return actual_decorator