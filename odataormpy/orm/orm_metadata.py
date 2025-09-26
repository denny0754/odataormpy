"""
Author: Diego Vaccher <dvaccher99@gmail.com>
Created on: 2025-09-26

Description:
    Provides a storage class OData service metadata.

Change Log:
    2025-09-26 - Diego Vaccher - Initial creation
"""

from typing import Union
import xml.etree.ElementTree as ET
import lzma
import json

class ORMMetadata:
    """ORM Metadata storage.

    """
    def __init__(self, xml, lazy_load : bool = True) -> None:
        """

        :param xml: Raw XML data to parse
        :param lazy_load: Lazy loads metadata from XML.
        """
        self.__xml_data : str = xml

        self.__xml_namespaces : dict = {
            "edmx": "http://schemas.microsoft.com/ado/2007/06/edmx",
            "m": "http://schemas.microsoft.com/ado/2007/08/dataservices/metadata",
            "edm": "http://schemas.microsoft.com/ado/2008/09/edm",
            "sap": "http://www.sap.com/Protocols/SAPData"
        }

        self.__lazy_load : bool = lazy_load
        self.__entities : dict = { }

        self.__parse_xml()

    def __parse_attribute(self, entity_attribute):
        """Parses all attributes of the current entity.

        :param entity_attribute: XML attributes to parse.
        :return:
        """
        entity_name = entity_attribute.get("Name", "")

        if entity_name in self.__entities or entity_name == "":
            return

        self.__entities[entity_name] = {
            "attributes": {}
        }

        entity_type = entity_attribute.get("Type", "")

        self.__entities[entity_name]["attributes"] = {
            "type": entity_type,
            "updatable": entity_attribute.get(
                '{http://www.sap.com/Protocols/SAPData}updatable', False),
            "creatable": entity_attribute.get(
                '{http://www.sap.com/Protocols/SAPData}creatable', False),
            "deletable": entity_attribute.get(
                '{http://www.sap.com/Protocols/SAPData}deletable', False),
        }

    def __parse_property(self, entity_property):
        """Parses all properties of the current entity.

        :param entity_property: XML property to parse.
        :return:
        """
        entity_name = entity_property.attrib.get("Name")
        for prop in entity_property.findall("edm:Property", self.__xml_namespaces):
            ep_name = prop.attrib.get("Name")
            self.__entities[entity_name]["properties"][ep_name] = {
                "data_type": prop.attrib.get("Type"),
                "nullable": prop.attrib.get("Nullable"),
                "max_length": prop.attrib.get("MaxLength")
            }

    def __compress_lazy(self) -> None:
        """Compresses all entities using LZMA compression.

        :return:
        """
        for key, value in self.__entities.items():
            data = json.dumps(value)
            compress_data = lzma.compress(data.encode('utf-8'))
            value.pop("attributes")
            value.pop("properties")
            self.__entities[key] = {
                "__lazy_loaded": compress_data
            }

    def __decompress_lazy(self, entity_name) -> None:
        """Decompress lazy data for the given entity.

        :param entity_name: Entity name to decompress
        :return:
        """
        if entity_name in self.__entities:
            data = self.__entities[entity_name]["__lazy_loaded"]
            decompressed_data = lzma.decompress(data)
            self.__entities[entity_name].pop("__lazy_loaded")
            self.__entities[entity_name] = json.loads(decompressed_data)

    def __parse_xml(self):
        """Parses the XML raw data and saves it on this storage class.

        :return: None
        """
        xml_root = ET.fromstring(self.__xml_data)

        entity_container = xml_root.find(".//edm:EntityContainer", self.__xml_namespaces)

        for entity in entity_container.findall("edm:EntitySet", self.__xml_namespaces):
            self.__parse_attribute(entity)

        for entity in xml_root.findall(".//edm:EntityType", self.__xml_namespaces):
            self.__parse_property(entity)

        if self.__lazy_load:
            self.__compress_lazy()

    def get(self, entity_name) -> Union[dict, None]:
        """Returns the entity metadata. If not found, None is returned.

        :param entity_name: Entity name to get.
        :return:
        """
        if entity_name in self.__entities:
            self.__decompress_lazy(entity_name)
            return self.__entities[entity_name]
        return None

    def __getitem__(self, key: str):
        """Allow read-only access to entities using ['entity_name'].

        :param key: Entity name
        """
        # Check if the key exists in the entities
        if key in self.__entities:
            # If lazy-loaded, decompress before returning
            if "__lazy_loaded" in self.__entities[key]:
                self.__decompress_lazy(key)
            return self.__entities[key]
        raise KeyError(f"Entity '{key}' not found.")

    def __repr__(self) -> str:
        """String representation of an entity

        :return: A string representation of the object.
        """
        return json.dumps(self.__entities, indent=4)
