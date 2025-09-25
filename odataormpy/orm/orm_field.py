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
    """Defines an OData object field. Used to interact with fields and
    use expressions.
    """
    def __init__(self, name):
        """

        :param name: Name of the field.
        """
        self.__name = name

    def __eq__(self, other) -> ORMExpression:  # type: ignore[override]
        """Equality operator.

        :param other: Other OData field.
        :return: Expression object for equality.
        """
        return ORMExpression(f"{self.__name} eq {self._format(other)}")

    def __ne__(self, other) -> ORMExpression:  # type: ignore[override]
        """Inequality operator.

        :param other: Other OData field.
        :return: Expression object for inequality.
        """
        return ORMExpression(f"{self.__name} ne {self._format(other)}")

    def __gt__(self, other) -> ORMExpression:
        """Greater operator.

        :param other: OData field.
        :return: Expression object for greater equality.
        """
        return ORMExpression(f"{self.__name} gt {self._format(other)}")

    def __ge__(self, other) -> ORMExpression:
        """Greater operator.

        :param other: OData field.
        :return: Expression object for greater equality or equality.
        """
        return ORMExpression(f"{self.__name} ge {self._format(other)}")

    def __lt__(self, other) -> ORMExpression:
        """Lesser operator.

        :param other: OData field.
        :return: Expression object for less equality.
        """
        return ORMExpression(f"{self.__name} lt {self._format(other)}")

    def __le__(self, other) -> ORMExpression:
        """Lesser operator.

        :param other: OData field.
        :return: Expression object for less equality or equality.
        """
        return ORMExpression(f"{self.__name} le {self._format(other)}")

    def _format(self, value) -> str:
        """Formats a value to a string for ease of use in the expression.

        :param value: Value to format.
        :return: Formatted value.
        """
        if isinstance(value, str):
            return f"'{value}'"
        return str(value)
