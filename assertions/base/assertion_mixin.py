from typing import TypeVar

from assertions.base.assertion_base import AssertionBase
from assertions.base.assertion_types import AssertionTypes

T = TypeVar('T')


class AssertionMixin(AssertionBase):

    def to_be_equal(self, actual: T):
        step_name = f'Checking that "{self._description}" equals to "{self.expected}"'
        with self.step_provider(step_name):
            template = self._error_template(actual, AssertionTypes.EQUAL)
            assert self.expected == actual, template

        return self

    def not_to_be_equal(self, actual: T):
        step_name = f'Checking that "{self._description}" not equals to "{self.expected}"'
        with self.step_provider(step_name):
            template = self._error_template(actual, AssertionTypes.NOT_EQUAL)
            assert self.expected != actual, template

        return self

    def in_(self, actual: T):
        step_name = f'Checking that "{self._description}" in "{self.expected}"'
        with self.step_provider(step_name):
            template = self._error_template(actual, AssertionTypes.IN_)
            assert self.expected != actual, template

        return self