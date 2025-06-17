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
def test_strict_decorator():
    @strict
    def add(a: int, b: int) -> int:
        return a + b

    @strict
    def say(name: str, loud: bool) -> str:
        return name.upper() if loud else name.lower()

    # 1. Корректный вызов
    assert add(1, 2) == 3
    assert say("Анна", loud=True) == "АННА"

    # 2. Ошибка типа (b должен быть int)
    try:
        add(1, "2")
    except TypeError as e:
        assert 'argument "b" must be int' in str(e)
    else:
        raise AssertionError("TypeError не был вызван при неправильном типе b")

    # 3. Ошибка типа (name должен быть str)
    try:
        say(123, loud=False)
    except TypeError as e:
        assert 'argument "name" must be str' in str(e)
    else:
        raise AssertionError("TypeError не был вызван при неправильном типе name")

    # 4. Проверка строгости: bool не считается int
    try:
        add(True, 2)
    except TypeError as e:
        assert 'argument "a" must be int' in str(e)
    else:
        raise AssertionError("TypeError не был вызван при передаче bool вместо int")

    print("тесты для @strict прошли успешно.")

if __name__ == "__main__":
    test_strict_decorator()
