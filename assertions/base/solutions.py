from assertions.base.expect import expect


def assert_status_code(actual: int, expected: int) -> None:
    expect(expected) \
        .set_description("Response status code") \
        .to_be_equal(actual)

def assert_error(actual: str, expected: str) -> None:
    expect(expected) \
        .set_description("Text error") \
        .to_be_equal(actual)

def assert_error_data(actual: str, expected: str) -> None:
    expect(expected) \
        .set_description("Text error") \
        .in_(actual)

def assert_len_database(actual: int, expected: int) -> None:
    expect(expected) \
        .set_description("Length Database") \
        .to_be_equal(actual)

def assert_key_in_dict(actual: dict, expected: dict) -> None:
    expect(expected) \
        .set_description("Found in data") \
        .in_(actual)