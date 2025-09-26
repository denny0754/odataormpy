"""
Author: Diego Vaccher <dvaccher99@gmail.com>
Created on: 2025-09-24

Description:
    Provides the template object class to interact with OData entities

Change Log:
    2025-09-24 - Diego Vaccher - Initial creation
"""

from typing import Union, Any

from ..exception import ORMException

class ORMObject: # pylint: disable=too-many-instance-attributes
    """Generic ORM Object. Helps in querying, creating or updating entities.
    Dynamically generated for each individual entity record when an execution is performed.
    """
    def __init__(self, entity_name : str, entity_metadata : dict):
        self.__entity = entity_name
        self.__metadata = entity_metadata
        self.__parameters : dict = { }
        self.__dirty = False
        self.__load_metadata()

    def __load_metadata(self) -> None:
        """Loads the metadata and builds the attributes based on it.

        :return: None
        """
        for key in self.__metadata.get("properties", {}).keys():
            # Setting to None by default.
            setattr(self, key, None)

    def top(self, count : int) -> "ORMObject":
        """Sets the maximum number of results to return.

        :param count: Maximum number of entities to return.
        :return:
        """
        self.__parameters["$top"] = count

        return self

    def select(self, *fields) -> "ORMObject":
        """Sets the fields to be selected when calling the OData.

        :param fields: Fields to be selected.
        :return:
        """
        self.__parameters["$select"].extend(fields)

        return self

    def format(self, fmt : str = "json") -> "ORMObject":
        """Sets the format of the returned objects.

        :param fmt: Format to use.
        :return:
        """
        # Does it make actual sense to let the user decide which format to use?
        # The actual response won't be available to the user, and in order
        # to manage it, we need to decider whether to use json or xml.
        # JSON is easier to parse.
        if fmt not in ["json", "xml"]:
            raise ORMException("Format must be 'json' or 'xml'")
        self.__parameters["$format"] = fmt

        return self

    def count(self) -> "ORMObject":
        """Sets the number of results to return.

        :return: None
        """
        # This parameter is special, as it doesn't require any value assignment
        # but all other parameters should not be set.
        # So, when set, the others needs to be ignored(deleted) from the
        # HTTP query request.
        self.__parameters["$count"] = True

        return self

    def __getitem__(self, key : str) -> Union[Any, None]:
        """Retrieve a field using the brackets.

        :param key: Field to retrieve from this instance
        :return:
        """
        if getattr(self, key) is None or key not in self.__metadata.get("properties", { }).keys():
            raise ORMException(f"Field {key} requested does not exists or is invalid. {key}")
        return getattr(self, key)

    def __setitem__(self, key : str, value : Union[Any, None]):
        """Set a field using the brackets.

        :param key: Field to set a value for.
        :param value: Fields's value to set.
        :return:
        """
        if getattr(self, key) is None or key not in self.__metadata.get("properties", { }).keys():
            raise ORMException(f"Field {key} requested does not exists or is invalid. {key}")
        setattr(self, key, value)
        self.__dirty = True

    def get_parameters(self) -> dict:
        """Returns parameters for the HTTP request.

        """
        return self.__parameters

    def get_service_name(self) -> str:
        """Returns the service name for the HTTP request.

        """
        return self.__metadata.get("__service", "")

    def get_entity_name(self) -> str:
        """Returns the entity name for the HTTP request.

        """
        return self.__entity

    def dirty(self) -> bool:
        """Returns True if the records has been tampered.

        :return: True if the records has been tampered. False otherwise.
        """
        return self.__dirty
