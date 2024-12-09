from sqlalchemy.future import select

from database.db_setup import async_session
from database.models import User


async def register_user(
    telegram_id: int,
    username: str = None,
    first_name: str = None,
    last_name: str = None,
) -> None:
    async with async_session() as session:
        existing_user = await session.get(User, telegram_id)
        if not existing_user:
            new_user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
            )
            session.add(new_user)
            await session.commit()


async def get_user_id_by_username(username: str) -> int:
    async with async_session() as session:
        result = await session.execute(
            select(User.telegram_id).where(User.username == username)
        )
        user_id = result.scalar()
        return user_id
