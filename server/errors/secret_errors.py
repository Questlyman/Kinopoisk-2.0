from fastapi import status

from server.errors.base import BaseHTTPError


class InvalidPasswordError(BaseHTTPError):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Invalid password for this secret"


class SecretNotFoundError(BaseHTTPError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Secret was not found"
