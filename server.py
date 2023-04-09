import json
import logging
import os
import textwrap
from asyncio import sleep
from datetime import datetime, timedelta

import aiofiles as aiofiles
from aiogram import Bot, Dispatcher, executor, types


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

start_time = datetime.now()
with open('all_words.json') as f:
    all_words = json.load(f)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer(textwrap.dedent(
        """
        Бот для изучения 3000 самых популярных английских слов.
        Начните сегодня изучать по 15 слов в день и за 2 месяца выучите все слова
        Зная эти слова вы сможете понимать английскую речь около 75% англоговорящих людей  
        """
    ))


@dp.message_handler(commands=['go_study'])
async def send_words(message: types.Message):
    while True:
        today = start_time + timedelta(days=1)
        await sleep(60 * 60 * 61)
        if today.strftime("%H") >= "10":
            known_words = await _get_known_words()
            if message.from_user.id not in known_words:
                await _add_user(message.from_user.id)

            for user in known_words:
                user_known_words = known_words[user]
                words_for_knowing = list(set(all_words) - set(user_known_words))[:10]
                today_words = {}

                for word in words_for_knowing:
                    user_known_words[word] = all_words[word]
                    today_words[word] = all_words[word]

                await _save_words({user: user_known_words})
                words = f'\n'.join(f'\t\t\t\t{en}: {ru}'for en, ru in today_words.items())
                msg = (textwrap.dedent(f"""Слова на сегодня: \n{words}\n"""))
                logging.basicConfig()
                logger.info(f'{msg} for {user}')
                await message.answer(textwrap.dedent(msg))


async def _add_user(user_id: int) -> None:
    known_words = await _get_known_words()
    known_words[user_id] = {}
    await _save_words(known_words)


async def _get_known_words() -> dict[int, dict[str, str]]:
    async with aiofiles.open('known_words.json') as fp:
        return json.loads(await fp.read())


async def _save_words(words: dict[int, dict[str, str]]):
    async with aiofiles.open('known_words.json', mode='w') as fp:
        await fp.write(json.dumps(words, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
