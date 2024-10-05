import base64
import secrets

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from server.adapters.database.requests import secret as db_requests_secret
from server.repo.exceptions import secret as exceptions_secret
from server.repo.models import secret as repo_models_secret
from server.settings import security_settings


def _create_key(password: bytes, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=security_settings.pbkdf2hmac_iterations,
        backend=default_backend(),
    )
    return base64.urlsafe_b64encode(kdf.derive(password))


def encrypt_data(
    create_secret_model: repo_models_secret.CreateSecretModel,
) -> repo_models_secret.SecretInDBModel:
    salt = secrets.token_bytes(security_settings.salt_length)

    key = _create_key(create_secret_model.password, salt)

    fernet = Fernet(key)
    encrypted = fernet.encrypt(create_secret_model.secret_data)

    return repo_models_secret.SecretInDBModel(
        secret_data=encrypted,
        salt=salt,
    )


def decrypt_data(
    password: bytes, secret_in_db_model: repo_models_secret.SecretInDBModel
) -> repo_models_secret.SecretResponseModel:
    key = _create_key(password, secret_in_db_model.salt)

    fernet = Fernet(key)
    try:
        decrypted = fernet.decrypt(secret_in_db_model.secret_data)
    except InvalidToken as exc:
        raise exceptions_secret.InvalidPasswordException() from exc

    return repo_models_secret.SecretResponseModel(
        secret_data=decrypted,
    )


async def save_secret_in_db(
    create_secret_model: repo_models_secret.CreateSecretModel,
) -> repo_models_secret.SecretInDBModel:
    encrypted_data = encrypt_data(create_secret_model)
    secret = await db_requests_secret.create_secret(
        encrypted_data=encrypted_data.secret_data,
        salt=encrypted_data.salt,
    )

    return repo_models_secret.SecretInDBModel.from_orm(secret)


async def get_secret_from_db(
    request_secret_model: repo_models_secret.RequestSecretModel,
) -> repo_models_secret.SecretResponseModel:
    secret = await db_requests_secret.get_secret_by_uuid(request_secret_model.uuid)
    if secret is None:
        raise exceptions_secret.SecretNotFoundException()
    decrypted_data = decrypt_data(
        request_secret_model.password,
        repo_models_secret.SecretInDBModel.from_orm(secret),
    )
    return decrypted_data
