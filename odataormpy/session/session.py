"""
Author: Diego Vaccher <dvaccher99@gmail.com>
Created on: 2025-09-24

Description:
    Provides the base class for HTTP requests in the OData ORM.

Change Log:
    2025-09-24 - Diego Vaccher - Initial creation
"""

from typing import Any, Optional
import requests

from odataormpy.exception import ORMSessionException

class ORMSession:
    """Session object used to interact with the source system in which
    OData services are defined.
    """
    def __init__(self, base_host : str,
                 auth : tuple[str, str],
                 http_proto : str = 'https',
                 http_port : int = 443) -> None:
        """

        :param base_host: Base URL of the OData ORM.
        :param auth: Authentication tuple (username, password).
        :param http_proto: HTTP protocol (http or https). Defaults to https.
        :param http_port: HTTP port (port). Defaults to 443.
        """
        self.__base_host = base_host
        self.__http_proto = http_proto
        self.__http_port = http_port

        if not self.__base_host or len(self.__base_host) < 1:
            raise ORMSessionException("Hostname hasn't been set! Please, verify and try again!")

        self.__base_url = f"{self.__http_proto}://{self.__base_host}:{self.__http_port}"

        self.__session = requests.Session()

        self.__session.auth = auth

        self.__session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json"
        })

    def get(self, endpoint : str, params : Optional[dict, None]) -> requests.Response:
        """Sends GET request to the OData source system.

        :param endpoint: Endpoint of the OData source system.
        :param params: Parameters to be sent to the OData source system.
        :return: Response object.
        """
        req_url : str = f"{self.__base_url}/{endpoint}"

        response : requests.Response = self.__session.get(
            url=req_url,
            params=params
        )

        response.raise_for_status()

        return response

    def post(self, endpoint : str, data : dict[Any, Any] | str | None) -> requests.Response:
        """Sends POST request to the OData source system.

        :param endpoint: Endpoint of the OData source system.
        :param data: Data to be sent to the OData source system.
        :return: Response object.
        """
        req_url : str = f"{self.__base_url}/{endpoint}"

        response : requests.Response = self.__session.post(
            url=req_url,
            data=data if isinstance(data, str) else None,
            json=data if isinstance(data, dict) else None
        )
        response.raise_for_status()

        return response

    def patch(self, endpoint : str, data : dict[Any, Any] | str | None) -> requests.Response:
        """Sends PATCH request to the OData source system.

        :param endpoint: Endpoint of the OData source system.
        :param data: Data to be sent to the OData source system.
        :return: Response object.
        """
        req_url = f"{self.__base_url}/{endpoint}"

        response : requests.Response = self.__session.patch(
            url=req_url,
            data=data if isinstance(data, str) else None,
            json=data if isinstance(data, dict) else None
        )

        response.raise_for_status()

        return response

    def delete(self, endpoint : str) -> requests.Response:
        """Sends DELETE request to the OData source system.

        :param endpoint: Endpoint of the OData source system.
        :return: Response object. DELETE should return an empty response with status code 204,
                 most of the time.
        """
        req_url = f"{self.__base_url}/{endpoint}"

        response : requests.Response = self.__session.delete(
            url=req_url
        )

        response.raise_for_status()

        return response
