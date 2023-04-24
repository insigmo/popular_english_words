import re
import textwrap

import uvloop
from aiogram import Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardMarkup
from telegram_bot.helpers import db_add_user
from telegram_bot.vars import dp


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
async def go_study(message: types.Message) -> None:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["10 слов -- Easy", "15 слов -- Medium", "20 слов -- Hard"]
    keyboard.add(*buttons)

    await message.answer(textwrap.dedent(
        '''
        Вам нужно будет выбрать количество слов, сколько будете изучать каждый день
             10 слов -- easy
             15 слов -- medium
             20 слов -- hard
        Количество слов можно поменять в любое время через /go_study
        Пожалуйста напишите сколько слов вы хотели бы изучить? (пример -- 10)
        '''))


@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message) -> None:
    message.from_user.values['enable'] = False
    await db_add_user(message.from_user.values)

    await message.answer('Вы были отписаны от ежедневного обучения слов. \n'
                         'Для возобновления нажмите или введите /go_study')


@dp.message_handler(Text(contains=""))
async def add_user(message: Message):
    words_count = int(re.match(r'\w{1,2}', message.text).group())
    message.from_user.values['words_count'] = words_count
    message.from_user.values['what_hour'] = 9
    message.from_user.values['enable'] = True

    await db_add_user(message.from_user.values)
    await message.answer('Вы были подписаны на ежедневное обучение наиболее используемых английских слов. \n'
                         f'Каждый день в 9 утра вы будете получать по {words_count} слов. \nУдачи!')


@dp.message_handler()
async def echo_message(msg: types.Message):
    await msg.answer(
        textwrap.dedent("""
        Не знаю такой команды. Вам доступны только следующие:
            /start
            /go_study
            /unsubscribe
            /help
        """)
    )


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    uvloop.install()
    executor.start_polling(dp, skip_updates=False, on_shutdown=shutdown)
