"""
Author: Diego Vaccher <dvaccher99@gmail.com>
Created on: 2025-09-24

Description:
    Provides the template object class to interact with OData entities

Change Log:
    2025-09-24 - Diego Vaccher - Initial creation
"""
from orm_expression import ORMExpression
from orm import ORM
from ..exception.exception import ORMExpressionException, ORMRuntimeException

from typing import Union
from requests import Response, JSONDecodeError


class ORMObject:

    def __init__(self, orm_session : ORM, entity : str):
        self.__orm_session = orm_session
        self.__entity = entity

        self.__filter = []
        self.__select = []
        self.__orderby = []

        self.__format = "json"

        self.__skip = None
        self.__top = None

    def filter(self, *expression) -> "ORMObject":
        for expr in expression:
            if isinstance(expr, ORMExpression):
                self.__filter.append(expr)
            else:
                raise ORMExpressionException(f"Unknown expression type or format. Received {type(expr)} - {expr}")
        return self

    def select(self, *fields) -> "ORMObject":
        self.__select.extend(fields)
        return self

    def top(self, count) -> "ORMObject":
        self.__top = count
        return self

    def skip(self, count) -> "ORMObject":
        self.__skip = count
        return self

    def format(self, fmt : str = "json") -> "ORMObject":
        self.__format = fmt
        return self

    def __build_params(self):
        params : dict = { }
        if self.__orderby:
            params["$orderby"] = self.__orderby
        if self.__skip:
            params["$skip"] = self.__skip
        if self.__filter:
            #TODO: Are filters being parsed already? If so, this is ok!
            params["$filter"] = self.__filter
        if self.__select:
            params["$select"] = self.__select
        if self.__format:
            params["$format"] = self.__format
        return params

    def execute(self) -> Union[list["ORMObject"], "ORMObject"]:
        entity_metadata = self.__orm_session.get_entity_metadata(self.__entity)

        endpoint = entity_metadata.get("attributes", { }).get("endpoint", None)

        if endpoint is None:
            raise ORMRuntimeException(f"Invalid endpoint. Unable to continue. {self}")

        params = self.__build_params()

        response : Response = self.__orm_session.orm_session.get(
            endpoint=endpoint,
            params=params
        )

        try:
            json_data = response.json()
            obj_data = json_data.get('d', { }).get('results', [ ])
            if len(obj_data) == 0:
                return []

            objects : list["ORMObject"] = []
            for obj in obj_data:
                objects.append(ORMObject.__from_json(self.__orm_session, self.__entity, obj))

            if len(objects) == 1:
                return objects[0]

            return objects

        except JSONDecodeError:
            raise ORMRuntimeException("Unable to parse response.")

    def update(self) -> None:
        #TODO: Implement update logic
        pass

    def create(self) -> None:
        #TODO: Implement creation logic
        pass

    @staticmethod
    def __from_json(orm_session: ORM, entity: str, json_data: dict) -> "ORMObject":
        #TODO: Parse the json object and add attributes in the class.
        #      This way, data is accessed and update directly from the instance returned.
        #      Example:
        #      customers = orm.Customers.top(100).execute()
        #      customers[0].Name = "Diego"
        #      customers[0].update()
        obj = ORMObject(orm_session, entity)
        obj._data = json_data

        # Dynamically create attributes from JSON
        for key, value in json_data.items():
            setattr(obj, key, value)

        return obj