from fastapi import APIRouter, Depends, status

from server.errors import base as base_errors
from server.errors import secret_errors
from server.repo.exceptions import secret as repo_exceptions_secret
from server.repo.models import secret as repo_models_secret
from server.repo.requests import secret as repo_requests_secret
from server.routes.models import secret as models_secret


router = APIRouter()


@router.get(
    "/secrets/{secret_key}",
    responses={
        status.HTTP_200_OK: {
            "model": models_secret.ReadSecretResponseModel,
            "description": "Response with secret data",
        },
    }
    | base_errors.BaseHTTPError.generate_responses(  # type: ignore[operator]
        secret_errors.SecretNotFoundError, secret_errors.InvalidPasswordError
    ),
)
async def get_secret_data(
    secret_key: str,
    read_secret_request: models_secret.ReadSecretRequestModel = Depends(),
) -> models_secret.ReadSecretResponseModel:
    """
    Get the decrypted secret data
    """
    request_secret_repo_model = repo_models_secret.RequestSecretModel(
        password=read_secret_request.password.encode(), uuid=secret_key
    )
    try:
        secret_response = await repo_requests_secret.get_secret_from_db(
            request_secret_repo_model
        )
    except repo_exceptions_secret.InvalidPasswordException as exc:
        raise secret_errors.InvalidPasswordError() from exc
    except repo_exceptions_secret.SecretNotFoundException as exc:
        raise secret_errors.SecretNotFoundError() from exc
    return models_secret.ReadSecretResponseModel(
        secret_data=secret_response.secret_data,
    )


@router.post(
    "/generate",
    responses={
        status.HTTP_200_OK: {
            "model": models_secret.CreateSecretResponseModel,
            "description": "Response with uuid of secret data",
        },
    },
)
async def generate_secret_data(
    create_secret_request: models_secret.CreateSecretRequestModel,
) -> models_secret.CreateSecretResponseModel:
    """
    Generate secret data encrypted by password
    """
    create_secret_repo_model = repo_models_secret.CreateSecretModel(
        secret_data=create_secret_request.secret_data.encode(),
        password=create_secret_request.password.encode(),
    )
    secret_in_db = await repo_requests_secret.save_secret_in_db(
        create_secret_repo_model
    )
    return models_secret.CreateSecretResponseModel(
        secret_key=str(secret_in_db.id),
    )
