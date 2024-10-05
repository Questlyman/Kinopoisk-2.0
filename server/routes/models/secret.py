from pydantic import BaseModel


class CreateSecretRequestModel(BaseModel):
    secret_data: str
    password: str


class CreateSecretResponseModel(BaseModel):
    secret_key: str


class ReadSecretRequestModel(BaseModel):
    password: str


class ReadSecretResponseModel(BaseModel):
    secret_data: str
