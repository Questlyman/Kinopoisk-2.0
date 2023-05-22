from fastapi import status

from server.errors.base import BaseHTTPError


class MethodNotAllowedError(BaseHTTPError):
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    detail = "Method not allowed"


class TooManyRequestsError(BaseHTTPError):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    detail = "Too many requests"
