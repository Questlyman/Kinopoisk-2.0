from server.adapters.database.models import Secret
from server.adapters.database.session import get_session


async def get_secret_by_uuid(uuid: str) -> Secret | None:
    async with get_session() as session:
        return await Secret.get(session, id=uuid)


async def create_secret(
    *,
    encrypted_data: bytes,
    salt: bytes,
) -> Secret:
    async with get_session() as session:
        secret = Secret(
            secret_data=encrypted_data,
            salt=salt,
        )

        session.add(secret)
        await session.commit()
        await session.refresh(secret)
        return secret
