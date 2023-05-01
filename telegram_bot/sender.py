import asyncio
import json
import logging
import os.path
import textwrap
from datetime import datetime

import uvloop
from db.tables import User
from telegram_bot.helpers import db_add_users, db_get_known_words, db_save_words
from telegram_bot.vars import bot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

words_path = os.path.join(os.path.dirname(__file__), 'all_words.json')
with open(words_path) as f:
    all_words = json.load(f)


async def _send_message(user: User):
    user_known_words = await db_get_known_words(user.id) or {}
    words_for_knowing = list(set(all_words) - set(user_known_words))[:user.words_count]
    today_words = {}

    for word in words_for_knowing:
        user_known_words[word] = all_words[word]
        today_words[word] = all_words[word]

    await db_save_words(user.id, user_known_words)

    today = datetime.now().strftime('%d/%m/%Y')
    words = '\n'.join(f'\t\t\t\t{en}: {ru}'for en, ru in today_words.items())
    msg = (textwrap.dedent(f"""Слова на {today}: \n{words}\n"""))

    logger.debug(f'{msg} for {user.first_name}')
    await bot.send_message(user.id, textwrap.dedent(msg))


async def main():
    users = await db_add_users()
    for user in users:
        if user.enable:
            await _send_message(user)


if __name__ == '__main__':
    uvloop.install()
    asyncio.run(main())
