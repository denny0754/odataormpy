"""
Author: Diego Vaccher <dvaccher99@gmail.com>
Created on: 2025-09-24

Description:
    Provides the main object class to interact with OData using ORM

Change Log:
    2025-09-24 - Diego Vaccher - Initial creation
"""

from functools import lru_cache

from odataormpy.session import ORMSession

class ORM:
    """Defines the actual ORM object used to interact with OData services.
    """
    def __init__(self, session : ORMSession | None) -> None:
        """

        :param session: ORM Session used to interact with OData services/source system.
        """
        self.orm_session = session
        '''
            Example __service structure:
            {
                "CorporateAccount": {
                    "attributes": {
                        "endpoint": "/sap/odata/v2",
                        "updatable": True,
                        "creatable": True,
                        "deletable": False
                    },
                    "properties": {
                        "ObjectID": {
                            "key": True,
                            "max_length": 70,
                            "data_type": "Edm.String",
                            "nullable": False
                        }
                    }
                }
            }
        '''
        self.__service : dict = { }

    def __parse_service_metadata(self,
                                 raw_metadata : str,
                                 service_name : str,
                                 lazy_load : bool) -> None:
        """Parses the metadata response and sets up the service structure for
        easy access.

        :param raw_metadata: Raw metadata response from OData service.
        :param service_name: Name of the service requested.
        :return:
        """
        import xml.etree.ElementTree as ET
        #TODO: Update the structure of the service metadata
        #TODO: Use `lazy_load` parameter to disable loading of metadata and store them
        #      as lzma payloads to save space.

        xml_ns = {
            "edmx": "http://schemas.microsoft.com/ado/2007/06/edmx",
            "m": "http://schemas.microsoft.com/ado/2007/08/dataservices/metadata",
            "edm": "http://schemas.microsoft.com/ado/2008/09/edm",
            "sap": "http://www.sap.com/Protocols/SAPData"
        }

        self.__service[service_name] = {
            "entity_props": { },
            "entity_attrs": { }
        }

        xml_root = ET.fromstring(raw_metadata)

        # Getting all entities and their attributes
        entity_container = xml_root.find(".//edm:EntityContainer", xml_ns)
        for entity in entity_container.findall("edm:EntitySet", xml_ns):
            e_name = entity.get("Name")
            e_type = entity.get("EntityType")
            #!TODO: Using the dynamic way, we would get "sap:creatable", "sap:updatable"
            #       and "sap:deletable".
            #       I should map these in a way I'm in charge of the key on my dictionary.
            #       Non priority. This is ok at the moment.
            e_updatable = entity.get('{http://www.sap.com/Protocols/SAPData}updatable')
            e_creatable = entity.get('{http://www.sap.com/Protocols/SAPData}updatable')
            e_deletable = entity.get('{http://www.sap.com/Protocols/SAPData}updatable')
            
            self.__service[service_name]["attributes"][e_name] = {
                "type": e_type,
                "updatable": e_updatable,
                "creatable": e_creatable,
                "deletable": e_deletable
            }
        
        # Getting all entities and their properties
        for entity in xml_root.findall(".//edm:EntityType", xml_ns):
            e_name = entity.attrib.get("Name")

            for prop in entity.findall("edm:Property", xml_ns):
                ep_name = prop.attrib.get("Name")
                self.__service[service_name]["properties"][e_name][ep_name] = {
                    "data_type": prop.attrib.get("Type"),
                    "nullable": prop.attrib.get("Nullable"),
                    "max_length": prop.attrib.get("MaxLength")
                }

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
        #!TODO: lazy_load should be passed to the parser and used to compress
        #       the metadata for the objects. This will save a little bit of
        #       memory space in case the metadata file is huge.
        if self.orm_session:
            metadata_response = self.orm_session.get(f'{service_endpoint}/$metadata', None)
            if metadata_response.ok:
                self.__parse_service_metadata(
                    raw_metadata=metadata_response.content.decode('utf-8'),
                    service_name=service_name,
                    lazy_load=lazy_load
                )
                self.__service[service_name]["endpoint"] = service_endpoint

    @lru_cache(maxsize=256)
    def get_entity_metadata(self, entity : str) -> dict:
        """Returns the metadata for a given entity.

        :param entity: Entity to get metadata for.
        :return: Entity metadata.
        """
        return self.__service.get(entity, { })

    @lru_cache(maxsize=256)
    def list_entities(self, service_name : str) -> list[str]:
        """Returns a list of all entities for a given service name.

        :param service_name: Name of the service requested.
        :return: List of entities.
        """
        entities = list(self.__service.get(service_name, {}).get("attributes",{}).keys())

        return entities
