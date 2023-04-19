from db.db_manager import DBManager
from db.tables import User


async def db_add_user(user: dict) -> None:
    async with DBManager() as manager:
        await manager.add_user(user)


async def db_add_users() -> list[User]:
    async with DBManager() as manager:
        return await manager.get_all_users()


async def db_get_known_words(user_id: int) -> dict[str, str]:
    async with DBManager() as manager:
        return await manager.get_known_words_by_user_id(user_id)


async def db_save_words(user_id: int, words: dict[str, str]):
    async with DBManager() as manager:
        return await manager.update_known_words(user_id, words)
