"""
Author: Diego Vaccher <dvaccher99@gmail.com>
Created on: 2025-09-24

Description:
    Provides the main object class to interact with OData using ORM

Change Log:
    2025-09-24 - Diego Vaccher - Initial creation
"""
from json import JSONDecodeError
from typing import Union

from .orm_object import ORMObject

from ..exception import ORMException
from ..session import ORMSession
from .orm_metadata import ORMMetadata

class ORM:
    """Defines the actual ORM object used to interact with OData services.
    """
    def __init__(self, session : ORMSession | None) -> None:
        """

        :param session: ORM Session used to interact with OData services/source system.
        """
        self.__orm_session = session

        self.__services : dict = { }
        self.__service_endpoints : dict = { }

    def register_service(self,
                         service_name : str,
                         service_endpoint : str,
                         lazy_load : bool = True) -> None:
        """Registers a service using the given service name and endpoint.
        If the service already exists, it will be updated.
        If lazy-load is enabled, the structure won't be fully created/updated.
        It will as objects are requested.

        :param service_name: Name of the service requested - Can be anything.
                             It's used to map the endpoint to a meaningful name.
        :param service_endpoint: Endpoint to be registered.
        :param lazy_load: Lazy-loading of the metadata structure.
        :return: None
        """
        if self.__orm_session:
            metadata_response = self.__orm_session.get(f'{service_endpoint}/$metadata', None)
            if metadata_response.ok:
                self.__services[service_name] = ORMMetadata(metadata_response, lazy_load)
                for key in self.__services[service_name].keys():
                    self.__services[service_name][key]["__service"] = service_name
                self.__service_endpoints[service_name] = service_endpoint

    def get_object(self, entity_name : str, service_name : str = "") -> ORMObject:
        """Returns an ORMObject for the given entity name.

        :param entity_name: Entity name to retrieve.
        :param service_name: Service name to retrieve. If not set, and only one is defined,
               the first will be used. If multiple are found and this is not set,
               an error will be thrown.
        :return: An empty instance of ORMObject.
        """
        if service_name not in self.__services and service_name != "":
            raise ORMException(f"Unknown service requested. {service_name}")

        entity_metadata = self.__services[service_name].get(entity_name)
        if entity_metadata is None:
            raise ORMException(f"Unknown entity requested. {entity_name}")

        orm_object : ORMObject = ORMObject(entity_name, entity_metadata)

        return orm_object

    def fetch(self, orm_object : ORMObject) -> Union[list[ORMObject], int]:
        """Fetches the given object from the ORM.

        :param orm_object: ORMObject to be fetched.
        :return: List of ORMObject objects.
        """
        params : dict = orm_object.get_parameters()
        endpoint = self.__service_endpoints.get(orm_object.get_service_name(), "")
        entity_name = orm_object.get_entity_name()
        service_name = orm_object.get_service_name()
        if not endpoint:
            raise ORMException(f"Unknown service. {orm_object.get_service_name()}")

        if params.get("$count", False):
            # Special case for $count operation
            response = self.__orm_session.get(
                endpoint=f'{endpoint}/{orm_object.get_entity_name()}/$count',
                params=None
            )
            if response.ok:
                try:
                    return int(response.content)
                except ValueError as exc:
                    raise ORMException(f"Invalid response from {endpoint}") from exc
            else:
                raise ORMException(f"Invalid response from {endpoint}")

        params.pop("$count")
        # For now, we hard code "json" as the default format accepted as response.
        params['$format'] = "json"
        response = self.__orm_session.get(
            endpoint=f'{endpoint}/{orm_object.get_entity_name()}',
            params=params
        )

        if not response.ok:
            return []
        try:
            orm_objects : list[ORMObject] = []
            j_result = response.json().get("d", { }).get("results", { })
            for obj_data in j_result:
                orm_object_loc : ORMObject = ORMObject(
                    entity_name,
                    self.__services[service_name][entity_name])

                for key in obj_data.keys():
                    try:
                        orm_object_loc[key] = obj_data[key]
                    except KeyError as exc:
                        raise ORMException(
                            f"Invalid field name returned from {endpoint}. {key}") from exc
                orm_objects.append(orm_object_loc)
        except JSONDecodeError as exc:
            raise ORMException(f"Invalid response from {endpoint}") from exc
        return orm_objects

    def fetch_many(self, orm_objects : list[ORMObject]) -> list[Union[ORMObject, int]]:
        """Fetches the given ORMObjects from the ORM. Uses `ORM.fetch()`
        to fetch the list of ORMObjects.

        :param orm_objects: List of ORMObjects to fetch.
        """
        output_list : list[Union[ORMObject, int]] = []
        for orm_object in orm_objects:
            output_list.append(self.fetch(orm_object))
        return output_list
