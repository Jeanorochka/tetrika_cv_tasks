import inspect
from functools import wraps


def strict(func):
    """
    декоратор проверяет строгое совпадение типов фактических аргументов
    с аннотациями в прототипе функции
    если тип хотя-бы одного аргумента отличается — вылезет TypeError

    поддерживаются позиционные и именованные параметры (без значений
      по умолчанию, как сказано в условии)

    строгая проверка — используется type(arg) is expected, чтобы
      bool не проходил за int, и наоборот.
    """
    sig = inspect.signature(func)          
    ann = func.__annotations__            

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)  
        for name, value in bound.arguments.items():
            expected = ann.get(name)
            if expected is None:         
                continue
            if type(value) is not expected:
                raise TypeError(
                    f'argument "{name}" must be {expected.__name__}, '
                    f'not {type(value).__name__}'
                )
        return func(*args, **kwargs)

    return wrapper
