from enum import Enum
from http import HTTPStatus  # Inherit the HTTPStatus object from the standard library


class HTTPMethod(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    