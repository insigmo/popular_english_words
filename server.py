import json
import logging
import os
import textwrap
from asyncio import sleep
from datetime import datetime, timedelta

import aiofiles as aiofiles
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.webhook import SendMessage

from db.db_manager import DBManager
from db.tables import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

with open('all_words.json') as f:
    all_words = json.load(f)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer(textwrap.dedent(
        """
        Бот для изучения 3000 самых популярных английских слов.
        Начните сегодня изучать по 10 слов в день и за 10 месяцев выучите все слова
        Вам станут доступны 95% текстов общей тематики, а остальные 5% вы поймёте интуитивно. Успехов в изучении!
        Для начала нажмите или введите /go_study
        """
    ))


@dp.message_handler(commands=['go_study'])
async def send_words(message: types.Message):
    while True:
        start_time = datetime.now()
        today = start_time + timedelta(days=1)
        # await sleep(60 * 60 * 61)
        await sleep(3)

        if today.strftime("%H") == "23":
            await _add_user(message.from_user.values)

            for user in await _get_users():
                user_known_words = await _get_known_words(user.id) or {}
                words_for_knowing = list(set(all_words) - set(user_known_words))[:10]
                today_words = {}

                for word in words_for_knowing:
                    user_known_words[word] = all_words[word]
                    today_words[word] = all_words[word]

                await _save_words(user.id, user_known_words)
                words = '\n'.join(f'\t\t\t\t{en}: {ru}'for en, ru in today_words.items())
                msg = (textwrap.dedent(f"""Слова на {start_time.strftime('%d/%m/%Y')}: \n{words}\n"""))
                logging.basicConfig()
                logger.debug(f'{msg} for {user.first_name}')
                await bot.send_message(user.id, textwrap.dedent(msg))


async def _add_user(user: dict) -> None:
    async with DBManager() as manager:
        await manager.add_user(user)


async def _get_users() -> list[User]:
    async with DBManager() as manager:
        return await manager.get_all_users()


async def _get_known_words(user_id: int) -> dict[str, str]:
    async with DBManager() as manager:
        return await manager.get_known_words_by_user_id(user_id)


async def _save_words(user_id: int, words: dict[str, str]):
    async with DBManager() as manager:
        return await manager.update_known_words(user_id, words)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
