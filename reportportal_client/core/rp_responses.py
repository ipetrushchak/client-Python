"""This module contains models for the RP response objects.

Detailed information about responses wrapped up in that module
can be found by the following link:
https://github.com/reportportal/documentation/blob/master/src/md/src/DevGuides/reporting.md
"""

#  Copyright (c) 2022 EPAM Systems
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License

import logging
from typing import Any, Optional, Generator, Mapping, Tuple, Protocol

from aiohttp import ClientResponse
from requests import Response

from reportportal_client.static.defines import NOT_FOUND

logger = logging.getLogger(__name__)


def _iter_json_messages(json: Any) -> Generator[str, None, None]:
    if not isinstance(json, Mapping):
        return
    data = json.get('responses', [json])
    for chunk in data:
        message = chunk.get('message', chunk.get('error_code'))
        if message:
            yield message


class RPResponse(Protocol):
    """Class representing RP API response."""
    _resp: Response
    __json: Any

    def __init__(self, data: Response) -> None:
        """Initialize instance attributes.

        :param data: requests.Response object
        """
        self._resp = data
        self.__json = None

    @property
    def id(self) -> Optional[str]:
        """Get value of the 'id' key."""
        return self.json.get('id', NOT_FOUND)

    @property
    def is_success(self) -> bool:
        """Check if response to API has been successful."""
        return self._resp.ok

    @property
    def json(self) -> Any:
        """Get the response in dictionary."""
        if not self.__json:
            self.__json = self._resp.json()
        return self.__json

    @property
    def message(self) -> Optional[str]:
        """Get value of the 'message' key."""
        return self.json.get('message')

    @property
    def messages(self) -> Tuple[str, ...]:
        """Get list of messages received."""
        return tuple(_iter_json_messages(self.json))


class AsyncRPResponse:
    """Class representing RP API response."""
    _resp: ClientResponse
    __json: Any

    def __init__(self, data: ClientResponse) -> None:
        """Initialize instance attributes.

        :param data: requests.Response object
        """
        self._resp = data
        self.__json = None

    @property
    async def id(self) -> Optional[str]:
        """Get value of the 'id' key."""
        return (await self.json).get('id', NOT_FOUND)

    @property
    def is_success(self) -> bool:
        """Check if response to API has been successful."""
        return self._resp.ok

    @property
    async def json(self) -> Any:
        """Get the response in dictionary."""
        if not self.__json:
            self.__json = await self._resp.json()
        return self.__json

    @property
    async def message(self) -> Optional[str]:
        """Get value of the 'message' key."""
        return (await self.json).get('message')

    @property
    async def messages(self) -> Tuple[str, ...]:
        """Get list of messages received."""
        return tuple(_iter_json_messages(await self.json))
