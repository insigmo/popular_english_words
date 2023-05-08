import re
import textwrap

import uvloop
from aiogram import Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardMarkup
from telegram_bot.helpers import db_add_or_update_user
from telegram_bot.vars import dp


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer(textwrap.dedent(
        """
        Бот для изучения 3000 самых популярных английских слов.
        Начните сегодня изучать, например, по 10 слов в день и за 10 месяцев выучите все слова
        Вам станут доступны 95% текстов общей тематики, а остальные 5% вы поймёте интуитивно. Успехов в изучении!
        Для начала нажмите или введите /go_study
        
        Вам доступны следующие команды:
            /start - запуск бота
            /go_study -- запуск обучения или возобновление обучения
            /unsubscribe -- отписаться от ежедневного изучения слов
        """
    ))


@dp.message_handler(commands=['go_study'])
async def go_study(message: types.Message) -> None:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["10 слов -- Easy", "15 слов -- Medium", "20 слов -- Hard"]
    keyboard.add(*buttons)

    await message.answer(textwrap.dedent(
        '''
        Вам нужно будет выбрать количество слов, которые вы будете изучать каждый день
             10 слов -- easy   #(10 месяцев)
             15 слов -- medium # ( месяцев)
             20 слов -- hard   # ( месяцев)
        Количество слов можно поменять в любое время через /go_study
        Пожалуйста напишите сколько слов вы хотели бы изучить? (например -- 10)
        '''))


@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message) -> None:
    message.from_user.values['enable'] = False
    await db_add_or_update_user(message.from_user.values)

    await message.answer('Вы были отписаны от ежедневного обучения слов. \n'
                         'Для возобновления нажмите или введите /go_study')


@dp.message_handler(lambda m: m.text.startswith('/change_time'))
async def change_time(message: types.Message) -> None:
    hour = re.findall(r'\d+', message.text)
    if not hour:
        await message.reply('Извините, но вы не ввели в какой час времени хотите получать уведомления.\n'
                            'Пожалуйста введите "/change_time <hour>" без кавычек. Например /change_time 13')
        return

    hour = int(hour[0])

    message.from_user.values['what_hour'] = hour
    await db_add_or_update_user(message.from_user.values)

    await message.answer(f'Вы теперь будете получать уведомления в {hour} часов. \nСчастливого вам дня!')


@dp.message_handler(Text(contains=""))
async def add_user(message: Message):
    words_count = int(re.match(r'\w{1,2}', message.text).group())
    user_data = message.from_user

    user_data.values['words_count'] = words_count
    user_data.values['what_hour'] = 9
    user_data.values['enable'] = True

    await db_add_or_update_user(user_data.values)
    await message.answer('Вы были подписаны на ежедневное обучение наиболее используемых английских слов. \n'
                         f'Каждый день в 9 утра вы будете получать по {words_count} слов.\n'
                         'Если вы хотите выбрать другое время оповещения в 24-часовом формате'
                         'введите "/change_time <hour>" без кавычек. Например /change_time 13')


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    uvloop.install()
    executor.start_polling(dp, skip_updates=False, on_shutdown=shutdown)
