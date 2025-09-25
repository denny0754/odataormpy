"""
Author: Diego Vaccher <dvaccher99@gmail.com>
Created on: 2025-09-24

Description:
    Provides the base class for ORM Session Exception

Change Log:
    2025-09-24 - Diego Vaccher - Initial creation
"""

class ORMException(Exception):
    """
    Generic ORM Exception
    """

class ORMSessionException(ORMException):
    """
    ORM Session Exception
    """

class ORMExpressionException(ORMException):
    """
    ORM Expression Exception
    """

class ORMRuntimeException(ORMException):
    """
    ORM Runtime Exception
    """
