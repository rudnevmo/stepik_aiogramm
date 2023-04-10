token1: str = '6118629512:AAFNkxQkACEG_sCoJpbYEpbUH9Oa1OVDANw'

import random

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Text, Command

bot: Bot = Bot(token1)
dp: Dispatcher = Dispatcher()

attempts: int = 5

users: dict = {}


def get_random_number() -> int:
    return random.randint(1, 100)


@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer('Привіт\nДавай зіграємо\nЩоб отримати правила та дізнатись список команд - /help\n'
                         'Щоб зіграти - погодься не гру')
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False,
                                        'secret_number': None,
                                        'attempts': None,
                                        'total_games': 0,
                                        'wins': 0}


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(f'Я загадую число - ти відгадуєш, є 5 спроб.\nУ тебе наразі {attempts} спроб\n'
                         f'Правила гри - /help\n'
                         f'Вийти з гри - /cancel\n'
                         f'Статистика ігор - /stat\n'
                         f'Зіграємо?')


@dp.message(Command(commands=['stat']))
async def process_stat_command(message: Message):
    await message.answer(f'Всього зіграно: {users[message.from_user.id]["total_games"]}\n'
                         f'З них переможних: {users[message.from_user.id]["wins"]}')


@dp.message(Command(commands=['cancel']))
async def process_cancel_command(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer('Ви вийшли з гри.')
        users[message.from_user.id]['in_game'] = False
    else:
        await message.answer('Ми і так не граємо')


@dp.message(Text(text=['Так', 'Давай', 'Звісно', 'Граємо', 'Т'], ignore_case=True))
async def process_negative_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer('Супер! Я вже загадав число')
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]["secret_number"] = get_random_number()
        users[message.from_user.id]['attempts'] = attempts
    else:
        await message.answer('Поки ми граємо я реагую тільки на числа від 1 до 100')


@dp.message(Text(text=['Ні', 'Не хочу', 'Н', 'Наступного разу'], ignore_case=True))
async def process_negative_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer('Шкода :(\nЯкщо захочеш зіграти - знаєш де мене знайти')
    else:
        await message.answer('Ми вже граємо, присилай число :)')


@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            await message.answer('Вітаю, ти відгадав число!\nБажаєш зіграти ще?')
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            await message.answer('Моє число менше')
            users[message.from_user.id]['attempts'] -= 1
        elif int(message.text) < users[message.from_user.id]['secret_number']:
            await message.answer('Моє число більше')
            users[message.from_user.id]['attempts'] -= 1

        if users[message.from_user.id]['attempts'] == 0:
            await message.answer(f'Нажаль, ти програв, скінчились усі спроби\nМоє число було'
                                 f' {users[message.from_user.id]["secret_number"]}\n'
                                 f'Бажаєш заграти ще раз?')
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
    else:
        await message.answer('Ми ще не почали грате, бажаєш?')


@dp.message()
async def process_other_text_answer(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer('Ми вже граємо, пиши своє число)')
    else:
        await message.answer('Я вмію тільки грати в цю гру(')

if __name__ == '__main__':
    dp.run_polling(bot)
