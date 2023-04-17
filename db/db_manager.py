import asyncio

from sqlalchemy import Result, select, update
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from db.compressor import Compressor
from db.tables import KnownWords, User
from variables import Vars

cmp = Compressor()


class DBManager:
    async def __aenter__(self):
        v = Vars()
        url = f"postgresql+asyncpg://{v.postgres_user}:{v.postgres_password}@{v.postgres_host}:{v.postgres_port}"
        self._engine = create_async_engine(url, echo=True, )
        self._a_session = async_sessionmaker(self._engine, expire_on_commit=False)
        return self

    async def __aexit__(self, *args, **kwargs):
        await self._engine.dispose()

    async def update_known_words(self, user_id: int, known_words: dict[str, str]) -> None:
        async with self._a_session() as session:
            known_words = cmp.compress(known_words)
            print(f"Updating known words for user {user_id}: {known_words}")

            stmt = update(KnownWords).filter_by(user_id=user_id).values(words=known_words)
            print(stmt.compile())

            await session.execute(stmt)
            await session.commit()

    async def add_user(self, user: dict) -> None:
        async with self._a_session() as session:
            if await self.get_user_by_user_id(user['id']):
                return

            user_table = User(**user)
            session.add(user_table)
            await session.commit()

            known_words_table = KnownWords(user_id=user['id'], words=cmp.compress(b''))
            session.add(known_words_table)
            await session.commit()

    async def get_known_words_by_user_id(self, user_id: int) -> Result:
        async with self._a_session() as session:
            statement = select(KnownWords).where(KnownWords.user_id == user_id)
            result = (await session.execute(statement)).scalar()
            return cmp.decompress(result.words)

    async def get_user_by_user_id(self, user_id: int) -> User | None:
        async with self._a_session() as session:
            result = await session.get(User, user_id)
            return result

    async def get_all_users(self) -> list[User]:
        async with self._a_session() as session:
            result = await session.execute(select(User))
            return result.scalars().all()


async def main():
    async with DBManager() as manager:
        user_values = {'first_name': 'Beta', 'id': 161533572, 'is_bot': False, 'language_code': 'en', 'username': 'insigmo'}
        # user_values2 = {'first_name': 'Beta', 'id': 161533571, 'is_bot': False, 'language_code': 'en', 'username': 'insigmo1'}
        known_words = {
            "the": "определенный артикль",
            "be": "быть, нужно, будь",
            "and": "и",
            "of": "показывает принадлежность",
            "a/an": "неопределённый артикль"
        }
        await manager.add_user(user_values)
        # await manager.add_user(user_values2)
        # await manager.update_known_words(user_values['id'], known_words)
        print(await manager.get_all_users())
        # print(await manager.get_known_words_by_user_id(user_values['id']))


if __name__ == '__main__':
    asyncio.run(main())
