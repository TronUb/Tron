from enum import Enum

# pylint: disable=E1101
class AutoName(Enum):
    def _generate_next_value_(self, *args):
        return self.lower()

    def __repr__(self):
        return f"main.core.enums.{self}"
