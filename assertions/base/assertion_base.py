from contextlib import contextmanager
from typing import Callable, ContextManager, TypeVar, Union
from assertions.base.assertion_types import AssertionTypes

T = TypeVar('T')
StepProvider = Callable[[str], ContextManager]

@contextmanager
def default_step_provider(step: str):
    """
    Поставщик шагов по умолчанию. 
    Используется для создания контекстного менеджера без дополнительных действий.
    :param step: Описание текущего шага.
    """
    yield

class AssertionBase:
    """
    Базовый класс для утверждений. 
    Предоставляет общую функциональность для создания и работы с утверждениями.
    """
    
    def __init__(self, expected: T) -> None:
        """
        Инициализация базового класса утверждения.
        :param expected: Ожидаемое значение для сравнения.
        """
        self.expected = expected
        self._description: Union[str, None] = None
        self._step_provider: StepProvider = default_step_provider

    def _error_template(self, actual: T, method: AssertionTypes):
        """
        Шаблон для сообщения об ошибке.
        :param actual: Фактическое значение.
        :param method: Тип утверждения (например, равенство, больше и т.д.).
        :return: Строка с описанием ошибки.
        """
        return f"""
        Checking: {self._description}
        Expected: {self.expected} {type(self.expected)}
        Actual: {actual} {type(actual)}
        
        Expression: assert {self.expected} {method} {actual}
        """

    def set_description(self, description: str):
        """
        Установить описание утверждения.
        :param description: Описание.
        :return: Объект утверждения (для цепочки вызовов).
        """
        self._description = description
        return self

    @property
    def step_provider(self) -> StepProvider:
        """
        Возвращает текущий поставщик шагов.
        :return: Поставщик шагов.
        """
        return self._step_provider

    @step_provider.setter
    def step_provider(self, provider: StepProvider):
        """
        Устанавливает поставщика шагов.
        :param provider: Функция, являющаяся поставщиком шагов.
        """
        self._step_provider = provider