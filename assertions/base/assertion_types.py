from enum import Enum

class AssertionTypes(str, Enum):
    """
    Перечисление типов утверждений, используемых для описания различных видов проверок.
    Атрибуты класса:
    EQUAL: Строковое представление оператора равенства.
    NOT_EQUAL: Строковое представление оператора неравенства.
    LENGTH: Представляет проверку на длину.
    IN_: Представляет проверку на принадлежность элемента к контейнеру.
    """
    
    EQUAL = '=='
    NOT_EQUAL = '!='
    LENGTH = 'is length'
    IN_ = 'is in'