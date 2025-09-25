"""
Author: Diego Vaccher <dvaccher99@gmail.com>
Created on: 2025-09-24

Description:
    Provides the expression object used on filter calls

Change Log:
    2025-09-25 - Diego Vaccher - Initial creation
"""

class ORMExpression:
    """Expression object to build expressions/conditions when using the filter
    parameter.
    """
    def __init__(self, expr: str):
        """

        :param expr: Expression object.
        """
        self._expr = expr

    def __and__(self, other : "ORMExpression"):
        """Combines two expressions and ands them.

        :param other: ORMExpression object.
        :return: Combined expression object.
        """
        return ORMExpression(f"({self._expr}) and ({other._expr})")

    def __or__(self, other : "ORMExpression"):
        """Combines two expressions and ors them.

        :param other: ORMExpression object.
        :return: Combined expression object.
        """
        return ORMExpression(f"({self._expr}) or ({other._expr})")

    def __str__(self):
        """Returns the string representation of the expression.

        :return: String representation of the expression.
        """
        return self._expr
