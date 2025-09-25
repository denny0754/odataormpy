"""
Author: Diego Vaccher <dvaccher99@gmail.com>
Created on: 2025-09-24

Description:
    Provides the main object class to interact with OData using ORM

Change Log:
    2025-09-24 - Diego Vaccher - Initial creation
"""

from session import ORMSession
from functools import lru_cache

class ORM:

    def __init__(self, session : ORMSession | None) -> None:

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

    def __parse_service_metadata(self, raw_metadata : str, service_name : str) -> None:
        import xml.etree.ElementTree as ET
        #TODO: Update the structure of the service metadata

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
            #!TODO: Using the dynamic way, we would get "sap:creatable", "sap:updatable" and "sap:deletable"
            #       I should map these in a way I'm in charge of the key on my dictionary. Non priority. This is
            #       ok at the moment.
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

    def register_service(self, service_name : str, service_endpoint : str, lazy_load : bool = True) -> None:
        #!TODO: lazy_load should be passed to the parser and used to compress the metadata for the objects.
        #       this will save a little bit of memory space in case the metadata file is huge.

        if self.orm_session:
            metadata_response = self.orm_session.get(f'{service_endpoint}/$metadata')
            if metadata_response.ok:
                self.__parse_service_metadata(metadata_response.content.decode('utf-8'), service_name)
                self.__service[service_name]["endpoint"] = service_endpoint

    @lru_cache(maxsize=None)
    def get_entity_metadata(self, entity : str) -> dict:
        return self.__service.get(entity, { })

    @lru_cache(maxsize=None)
    def list_entities(self, service_name : str) -> list[str]:
        
        entities = list(self.__service.get(service_name, {}).get("attributes",{}).keys())

        return entities