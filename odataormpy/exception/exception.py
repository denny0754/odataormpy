"""
Author: Diego Vaccher <dvaccher99@gmail.com>
Created on: 2025-09-24

Description:
    Provides the base class for ORM Session Exception

Change Log:
    2025-09-24 - Diego Vaccher - Initial creation
"""

class ORMException(Exception):
    pass

class ORMSessionException(ORMException):
    pass

class ORMExpressionException(ORMException):
    pass

class ORMRuntimeException(ORMException):
    pass