from fastapi import status

from server.errors.handlers import BaseHTTPError


class CredentialsError(BaseHTTPError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Could not validate credentials"
    headers = {"WWW-Authenticate": "Bearer"}


class InactiveUserError(BaseHTTPError):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Inactive user"
    headers = {}
