from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel


class CreateSecretModel(BaseModel):
    secret_data: bytes
    password: bytes


class RequestSecretModel(BaseModel):
    password: bytes
    uuid: str


class SecretInDBModel(BaseModel):
    id: UUID | None = None
    secret_data: bytes
    salt: bytes

    class Config:
        orm_mode = True

    def to_response(self) -> SecretResponseModel:
        return SecretResponseModel(secret_data=self.secret_data)


class SecretResponseModel(BaseModel):
    secret_data: bytes
