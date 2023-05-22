from server.exceptions.base import BaseServerException


class InvalidPasswordException(BaseServerException):
    pass


class SecretNotFoundException(BaseServerException):
    pass
