from enum import Enum


class AssertionTypes(str, Enum):
    EQUAL = '=='
    NOT_EQUAL = '!='
    IN_ = 'is in'