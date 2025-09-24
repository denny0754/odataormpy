"""
Author: Diego Vaccher <dvaccher99@gmail.com>
Created on: 2025-09-24

Description:
    Provides the base class for HTTP requests in the OData ORM.

Change Log:
    2025-09-24 - Diego Vaccher - Initial creation
"""

import requests
from typing import Any

from exception.exception import ORMSessionException

class ORMSession:

    def __init__(self, base_host : str,
                 auth : tuple[str, str],
                 http_proto : str = 'https',
                 http_port : int = 443) -> None:

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

    def get(self, endpoint : str, params : dict = { }) -> requests.Response:
        
        req_url : str = f"{self.__base_url}/{endpoint}"

        response : requests.Response = self.__session.get(
            url=req_url,
            params=params
        )

        response.raise_for_status()

        return response

    def post(self, endpoint : str, data : dict[Any, Any] | str | None) -> requests.Response:

        req_url : str = f"{self.__base_url}/{endpoint}"

        response : requests.Response = self.__session.post(
            url=req_url,
            data=data if isinstance(data, str) else None,
            json=data if isinstance(data, dict) else None
        )
        
        response.raise_for_status()

        return response
    
    def patch(self, endpoint : str, data : dict[Any, Any] | str | None) -> requests.Response:

        req_url = f"{self.__base_url}/{endpoint}"

        response : requests.Response = self.__session.patch(
            url=req_url,
            data=data if isinstance(data, str) else None,
            json=data if isinstance(data, dict) else None
        )

        response.raise_for_status()

        return response
    
    def delete(self, endpoint : str) -> requests.Response:

        req_url = f"{self.__base_url}/{endpoint}"

        response : requests.Response = self.__session.delete(
            url=req_url
        )

        response.raise_for_status()

        return response