"""
Author: Diego Vaccher <dvaccher99@gmail.com>
Created on: 2025-09-24

Description:
    Provides the expression object used on filter calls

Change Log:
    2025-09-25 - Diego Vaccher - Initial creation
"""

class ORMExpression:
    
    def __init__(self, expr: str):
        self.__expr = expr

    def __and__(self, other):
        return ORMExpression(f"({self.__expr}) and ({other.__expr})")

    def __or__(self, other):
        return ORMExpression(f"({self.__expr}) or ({other.__expr})")

    def __str__(self):
        return self.__expr