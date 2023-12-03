from assertions.base.expect import expect

def assert_status_code(actual: int, expected: int) -> None:
    """
    Проверяет соответствие фактического статус-кода ожидаемому.
    :param actual: Фактический статус-код.
    :param expected: Ожидаемый статус-код.
    """
    expect(expected) \
        .set_description("Response status code") \
        .to_be_equal(actual)

def assert_error(actual: str, expected: str) -> None:
    """
    Проверяет соответствие фактического текста ошибки ожидаемому.
    :param actual: Фактический текст ошибки.
    :param expected: Ожидаемый текст ошибки.
    """
    expect(expected) \
        .set_description("Text error") \
        .to_be_equal(actual)

def assert_error_data(actual: str, expected: str) -> None:
    """
    Проверяет наличие ожидаемого текста ошибки в фактическом тексте.
    :param actual: Фактический текст, содержащий ошибку.
    :param expected: Ожидаемый текст ошибки.
    """
    expect(expected) \
        .set_description("Text error") \
        .in_(actual)

def assert_len_database(actual: int, expected: int) -> None:
    """
    Проверяет соответствие фактической длины записей в базе данных ожидаемой.
    :param actual: Фактическая длина записей в базе данных.
    :param expected: Ожидаемая длина записей.
    """
    expect(expected) \
        .set_description("Length Database") \
        .to_be_equal(actual)

def assert_result(actual: str, expected: str) -> None:
    """
    Проверяет соответствие фактического результата ожидаемому.
    :param actual: Фактическое сообщение результата.
    :param expected: Ожидаемое сообщение результата.
    """
    expect(expected) \
        .set_description("Result message") \
        .to_be_equal(actual)