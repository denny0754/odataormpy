"""
Author: Diego Vaccher <dvaccher99@gmail.com>
Created on: 2025-09-24

Description:
    Provides the template object field class to interact with OData entities' fields

Change Log:
    2025-09-25 - Diego Vaccher - Initial creation
"""

from orm_expression import ORMExpression

class ORMObjectField:

    def __init__(self, name):
        self.__name = name

    def __eq__(self, other) -> ORMExpression:  # type: ignore[override]
        return ORMExpression(f"{self.__name} eq {self._format(other)}")

    def __ne__(self, other) -> ORMExpression:  # type: ignore[override]
        return ORMExpression(f"{self.__name} ne {self._format(other)}")

    def __gt__(self, other) -> ORMExpression:
        return ORMExpression(f"{self.__name} gt {self._format(other)}")

    def __ge__(self, other) -> ORMExpression:
        return ORMExpression(f"{self.__name} ge {self._format(other)}")

    def __lt__(self, other) -> ORMExpression:
        return ORMExpression(f"{self.__name} lt {self._format(other)}")

    def __le__(self, other) -> ORMExpression:
        return ORMExpression(f"{self.__name} le {self._format(other)}")

    def _format(self, value) -> str:
        if isinstance(value, str):
            return f"'{value}'"
        return str(value)