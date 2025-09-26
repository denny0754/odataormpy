"""
Author: Diego Vaccher <dvaccher99@gmail.com>
Created on: 2025-09-24

Description:
    Provides the main object class to interact with OData using ORM

Change Log:
    2025-09-24 - Diego Vaccher - Initial creation
"""

from functools import lru_cache
import xml.etree.ElementTree as ET

from odataormpy.session import ORMSession
from .orm_metadata import ORMMetadata

class ORM:
    """Defines the actual ORM object used to interact with OData services.
    """
    def __init__(self, session : ORMSession | None) -> None:
        """

        :param session: ORM Session used to interact with OData services/source system.
        """
        self.orm_session = session

        self.__services : dict = { }

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
        if self.orm_session:
            metadata_response = self.orm_session.get(f'{service_endpoint}/$metadata', None)
            if metadata_response.ok:
                self.__services[service_name] = ORMMetadata(metadata_response, lazy_load)
