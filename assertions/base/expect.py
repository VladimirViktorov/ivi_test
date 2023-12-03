from typing import TypeVar
import allure
from assertions.base.assertion_mixin import AssertionMixin

T = TypeVar('T')

def expect(expected: T) -> AssertionMixin:
    """
    Создает и возвращает объект AssertionMixin для выполнения утверждений с заданным ожидаемым значением.
    Эта функция предназначена для удобства использования в тестах, позволяя формулировать утверждения в стиле 'expect'.
    Интегрируется с библиотекой Allure для логирования шагов теста.
    :param expected: Ожидаемое значение, с которым будут сравниваться другие значения в утверждениях.
    :return: Объект AssertionMixin, который предоставляет методы для различных типов утверждений.
    """
    assertion = AssertionMixin(expected=expected)
    assertion.step_provider = allure.step

    return assertion