from vkbottle import BaseStateGroup, GroupEventType, GroupTypes
from vkbottle.bot import Bot, Message
from vkbottle.dispatch.rules import ABCRule

import asyncio
import random
from vkbottle.modules import json
import logging
import sys
from loguru import logger
from datetime import datetime


from config import *
from markups import *
from workwithdb import workDB

logger.remove()
logger.add(sys.stderr, level="INFO")
logging.getLogger("vkbottle").setLevel(logging.INFO)

DB = workDB('db.db')
bot = Bot(token=VK_TOKEN)

users = DB.get_all('users')

"""Разные функции"""
def time_formatter(sec: int) -> str:
    hour = sec // 3600
    sec = sec % (24 * 3600)
    sec %= 3600
    min = sec // 60
    sec %= 60
    return "%d:%02d:%02d" % (hour, min, sec)

"""Правила"""
class ifin(ABCRule[Message]):
    def __init__(self, lst: list):
        self.lst = lst

    async def check(self, event: Message) -> bool:
        return event.text in self.lst

bot.labeler.custom_rules['ifin'] = ifin

"""Состояния"""
class States(BaseStateGroup):
    EMPTY = ''

    START_STEP_1 = 'START_STEP_1'
    START_STEP_2 = 'START_STEP_2'
    START_STEP_3 = 'START_STEP_3'

    BUILDINGS_MENU = 'BUILDINGS_MENU'
    BUILDINGS_CASTLE = 'BUILDINGS_CASTLE'
    BUILDINGS_SAWMILL = 'BUILDINGS_SAWMILL'
    BUILDINGS_MINE = 'BUILDINGS_MINE'
    BUILDINGS_FARM = 'BUILDINGS_FARM'
    BUILDINGS_CONVOY = 'BUILDINGS_CONVOY'

    WAR_MENU = 'WAR_MENU'
    WAR_INFANTRY = 'WAR_INFANTRY'
    WAR_ARCHERS = 'WAR_ARCHERS'
    WAR_RIDERS = 'WAR_RIDERS'
    WAR_ATTACK = 'WAR_ATTACK'

"""Хендлер на сообщения"""
@bot.on.private_message(text='Начать')
async def start(message: Message):
    global users
    if message.from_id not in users:
        DB.new_user('users', message.from_id)
        users = DB.get_all('users')
        await bot.state_dispenser.set(message.peer_id, States.START_STEP_1)
        await message.answer(msg_start_1, keyboard=keyboard_start(step=1))
    else:
        userinfo = await bot.api.users.get(message.from_id)
        data = users[message.from_id]
        await message.answer('Вижу у тебя есть какие-то проблемы с клавиатурой, вывел меню', keyboard=keyboard_menu(lvl_cas=data[7]))
        await message.answer(f'[id{message.from_id}|{userinfo[0].first_name}], твое королество:\n📖Игровой ID: {data[0]}\n\n💎Кристаллы: {data[2]}\n💰[{data[7]}]Золото: {data[3]}\n🌲[{data[9]}]Дерево: {data[4]}\n⛏[{data[8]}]Руда: {data[5]}\n🍖[{data[10]}]Еда: {data[6]}\n\nТерритория: {data[17]}🌍', keyboard=keyboard_menu(lvl_cas=data[7]))

@bot.on.private_message(text='Основать поселение', state=States.START_STEP_1)
async def start_1(message: Message):
    await bot.state_dispenser.set(message.peer_id, States.START_STEP_2)
    await message.answer(msg_start_2, keyboard=keyboard_start(step=2))

@bot.on.private_message(text='Построить здания', state=States.START_STEP_2)
async def start_1(message: Message):
    await bot.state_dispenser.set(message.peer_id, States.START_STEP_3)
    await message.answer(msg_start_3, keyboard=keyboard_start(step=3))

@bot.on.private_message(text='Начать путь Завоевателя.', state=States.START_STEP_3)
async def start_1(message: Message):
    data = DB.get_row_users(message.from_id)
    await message.answer(msg_start_4)
    asyncio.sleep(2)
    await message.answer(msg_start_5, keyboard=keyboard_menu(lvl_cas=data[7]))

@bot.on.private_message(text='🕍Здания')
async def war(message: Message):
    data = DB.get_row_users(message.from_id)
    await bot.state_dispenser.set(message.peer_id, States.BUILDINGS_MENU)
    lst = [
        DB.get_row_event('up_mine', data[1]),
        DB.get_row_event('up_farm', data[1]),
        DB.get_row_event('up_castle', data[1]),
        DB.get_row_event('up_sawmill', data[1]),
        DB.get_row_event('up_convoy', data[1])
    ]
    s = ''
    for i in lst:
        if i:
            s = f"\n\nВедётся улучшение здания {buildings_info[i[0][1].split('_')[1]][0]} ещё {time_formatter(i[0][2])}"
            break
    if s:
        await message.answer(f'Твои постройки:\n\n🕍Замок: ур. {data[7]}\n🌻Ферма: ур. {data[10]}\n🌲Лесопилка: ур. {data[9]}\n⛏Шахта: ур. {data[8]}\n⚖Караван: ур. {data[11]}' + s, keyboard=keyboard_btn(menu='buildings', lvl_cas=data[7], skip=i[0][2] // 180 + 1))
    else:
        await message.answer(f'Твои постройки:\n\n🕍Замок: ур. {data[7]}\n🌻Ферма: ур. {data[10]}\n🌲Лесопилка: ур. {data[9]}\n⛏Шахта: ур. {data[8]}\n⚖Караван: ур. {data[11]}', keyboard=keyboard_btn(menu='buildings', lvl_cas=data[7]))

@bot.on.private_message(text='👈Назад', state=States.BUILDINGS_MENU)
async def war(message: Message):
    userinfo = await bot.api.users.get(message.from_id)
    data = DB.get_row_users(message.from_id)
    await bot.state_dispenser.set(message.peer_id, States.EMPTY)
    await message.answer(f'[id{message.from_id}|{userinfo[0].first_name}], твое королество:\n📖Игровой ID: {data[0]}\n\n💎Кристаллы: {data[2]}\n💰[{data[7]}]Золото: {data[3]}\n🌲[{data[9]}]Дерево: {data[4]}\n⛏[{data[8]}]Руда: {data[5]}\n🍖[{data[10]}]Еда: {data[6]}\n\nТерритория: {data[17]}🌍', keyboard=keyboard_menu(lvl_cas=data[7]))

@bot.on.private_message(text='📜Помощь', state=States.BUILDINGS_MENU)
async def war(message: Message):
    data = DB.get_row_users(message.from_id)
    lst = [
        DB.get_row_event('up_mine', data[1]),
        DB.get_row_event('up_farm', data[1]),
        DB.get_row_event('up_castle', data[1]),
        DB.get_row_event('up_sawmill', data[1]),
        DB.get_row_event('up_convoy', data[1])
    ]
    s = ''
    for i in lst:
        if i:
            s = i[0][2]
            break
    if s:
        await message.answer(msg_buildings_help, keyboard=keyboard_btn(menu='buildings', lvl_cas=data[7], skip=s // 180 + 1))
    else:
        await message.answer(msg_buildings_help, keyboard=keyboard_btn(menu='buildings', lvl_cas=data[7]))

@bot.on.private_message(text='🕍Замок', state=States.BUILDINGS_MENU)
async def castle(message: Message):
    build = 'castle'
    await bot.state_dispenser.set(message.peer_id, States.BUILDINGS_CASTLE)
    data = DB.get_row_users(message.from_id)
    building_data = DB.get_row('economic', buildings_info[build][1] + data[7])
    if data[7] < 30:
        if data[3] - building_data[4] < 0:
            gold = '❌'
        else:
            gold = '✅'
        if data[4] - building_data[5] < 0:
            wood = '❌'
        else:
            wood = '✅'
        if data[5] - building_data[6] < 0:
            ore = '❌'
        else:
            ore = '✅'
        next_income = DB.get_row('economic', buildings_info[build][1] + data[7] + 1)[3]
        re_lst, to_lst = ['bname', 'blevel', 'income', 'next_gold', 'next_wood', 'next_ore', 'next_income', 'time'], [buildings_info[build][0], data[7], str(building_data[3]) + buildings_info[build][2], gold + str(building_data[4]), wood + str(building_data[5]), ore + str(building_data[6]), str(next_income) + buildings_info[build][2], time_formatter(building_data[9])]
        msg_to_re = msg_buildings
    else:
        re_lst, to_lst = ['bname', 'blevel', 'income'], [buildings_info[build][0], data[7], str(building_data[3]) + buildings_info[build][2]]
        msg_to_re = msg_build_max_level
    for i, j in zip(re_lst, to_lst):
        msg_to_re = msg_to_re.replace(i, str(j), 1)
    await message.answer(msg_to_re, keyboard=keyboard_btn(buildings_info[build][0], lvl_cas=data[7]))

@bot.on.private_message(text='⚒Улучшить', state=States.BUILDINGS_CASTLE)
async def castle(message: Message):
    build = 'castle'
    data = DB.get_row_users(message.from_id)
    building_data = DB.get_row('economic', buildings_info[build][1] + data[7])
    if data[7] < 30:
        if data[15]:
            if data[3] >= building_data[4] and data[4] >= building_data[5] and data[5] >= building_data[6]:
                DB.set_cell('users', data[1], 'res_gol', data[3] - building_data[4])
                DB.set_cell('users', data[1], 'res_wod', data[4] - building_data[5])
                DB.set_cell('users', data[1], 'res_ore', data[5] - building_data[6])
                DB.new_event('up_castle', data[1], building_data[9])
                DB.set_cell('users', data[1], 'builders', data[15] - 1)
                await message.answer('Улучшение началось!', keyboard=keyboard_btn(buildings_info[build][0], lvl_cas=data[7]))
            else:
                s = 'Не хватает для улучшения:\n\n'
                if data[3] - building_data[4] < 0:
                    s += f'💰Золото: {abs(data[3] - building_data[4])}'
                if data[4] - building_data[5] < 0:
                    s += f'🌲Дерево: {abs(data[4] - building_data[5])}'
                if data[5] - building_data[6] < 0:
                    s += f'⛏Руда: {abs(data[5] - building_data[6])}'
                await message.answer(s, keyboard=keyboard_btn(buildings_info[build][0], lvl_cas=data[7]))
        else:
            r = [DB.get_row_event('up_convoy', data[1]), DB.get_row_event('up_farm', data[1]), DB.get_row_event('up_sawmill', data[1]), DB.get_row_event('up_castle', data[1]), DB.get_row_event('up_mine', data[1])]
            for i in r:
                if i:
                    r = i[0]
                    break
            if r[1] == 'up_convoy':
                s = f"На данный момент все строители заняты.\n\n⚒Идет строительство:\n⚖Караван ур. {data[11] + 1}\n⏳Осталось: {time_formatter(r[2])}\n\nТы можешь ускорить строительство за кристаллы, или купить еще одного строителя на 🎪Рынке в 🔮Лавке, чтобы строить сразу несколько зданий."
            elif r[1] == 'up_farm':
                s = f"На данный момент все строители заняты.\n\n⚒Идет строительство:\n🌻Ферма ур. {data[10] + 1}\n⏳Осталось: {time_formatter(r[2])}\n\nТы можешь ускорить строительство за кристаллы, или купить еще одного строителя на 🎪Рынке в 🔮Лавке, чтобы строить сразу несколько зданий."
            elif r[1] == 'up_sawmill':
                s = f"На данный момент все строители заняты.\n\n⚒Идет строительство:\n🌲Лесопилка ур. {data[9] + 1}\n⏳Осталось: {time_formatter(r[2])}\n\nТы можешь ускорить строительство за кристаллы, или купить еще одного строителя на 🎪Рынке в 🔮Лавке, чтобы строить сразу несколько зданий."
            elif r[1] == 'up_castle':
                s = f"На данный момент все строители заняты.\n\n⚒Идет строительство:\n🕍Замок ур. {data[7] + 1}\n⏳Осталось: {time_formatter(r[2])}\n\nТы можешь ускорить строительство за кристаллы, или купить еще одного строителя на 🎪Рынке в 🔮Лавке, чтобы строить сразу несколько зданий."
            elif r[1] == 'up_mine':
                s = f"На данный момент все строители заняты.\n\n⚒Идет строительство:\n⛏Шахта ур. {data[8] + 1}\n⏳Осталось: {time_formatter(r[2])}\n\nТы можешь ускорить строительство за кристаллы, или купить еще одного строителя на 🎪Рынке в 🔮Лавке, чтобы строить сразу несколько зданий."
            await message.answer(s, keyboard=keyboard_btn(buildings_info[build][0], lvl_cas=data[7]))
    else:
        await message.answer('Здание улучшено на максимум', keyboard=keyboard_btn(buildings_info[build][0], lvl_cas=data[7]))

@bot.on.private_message(text='👈Назад', state=States.BUILDINGS_CASTLE)
async def war(message: Message):
    data = DB.get_row_users(message.from_id)
    await bot.state_dispenser.set(message.peer_id, States.BUILDINGS_MENU)
    lst = [
        DB.get_row_event('up_mine', data[1]),
        DB.get_row_event('up_farm', data[1]),
        DB.get_row_event('up_castle', data[1]),
        DB.get_row_event('up_sawmill', data[1]),
        DB.get_row_event('up_convoy', data[1])
    ]
    s = ''
    for i in lst:
        if i:
            s = f"\n\nВедётся улучшение здания {buildings_info[i[0][1].split('_')[1]][0]} ещё {time_formatter(i[0][2])}"
            break
    if s:
        await message.answer(f'Твои постройки:\n\n🕍Замок: ур. {data[7]}\n🌻Ферма: ур. {data[10]}\n🌲Лесопилка: ур. {data[9]}\n⛏Шахта: ур. {data[8]}\n⚖Караван: ур. {data[11]}' + s, keyboard=keyboard_btn(menu='buildings', lvl_cas=data[7], skip=i[0][2] // 180 + 1))
    else:
        await message.answer(f'Твои постройки:\n\n🕍Замок: ур. {data[7]}\n🌻Ферма: ур. {data[10]}\n🌲Лесопилка: ур. {data[9]}\n⛏Шахта: ур. {data[8]}\n⚖Караван: ур. {data[11]}', keyboard=keyboard_btn(menu='buildings', lvl_cas=data[7]))

@bot.on.private_message(text='📖Инфо', state=States.BUILDINGS_CASTLE)
async def war(message: Message):
    build = 'castle'
    data = DB.get_row_users(message.from_id)
    building_data = DB.get_row('economic', buildings_info[build][1] + data[7])
    if data[7] < 30:
        if data[3] - building_data[4] < 0:
            gold = '❌'
        else:
            gold = '✅'
        if data[4] - building_data[5] < 0:
            wood = '❌'
        else:
            wood = '✅'
        if data[5] - building_data[6] < 0:
            ore = '❌'
        else:
            ore = '✅'
        next_income = DB.get_row('economic', buildings_info[build][1] + data[7] + 1)[3]
        re_lst, to_lst = ['bname', 'blevel', 'income', 'next_gold', 'next_wood', 'next_ore', 'next_income', 'time'], [buildings_info[build][0], data[7], str(building_data[3]) + buildings_info[build][2], gold + str(building_data[4]), wood + str(building_data[5]), ore + str(building_data[6]), str(next_income) + buildings_info[build][2], time_formatter(building_data[9])]
        msg_to_re = msg_buildings
    else:
        re_lst, to_lst = ['bname', 'blevel', 'income'], [buildings_info[build][0], data[7], str(building_data[3]) + buildings_info[build][2]]
        msg_to_re = msg_build_max_level
    for i, j in zip(re_lst, to_lst):
        msg_to_re = msg_to_re.replace(i, str(j), 1)
    await message.answer(msg_to_re, keyboard=keyboard_btn(buildings_info[build][0], lvl_cas=data[7]))

@bot.on.private_message(text='📜Помощь', state=States.BUILDINGS_CASTLE)
async def war(message: Message):
    build = 'castle'
    data = DB.get_row_users(message.from_id)
    await message.answer(msg_castle_help, keyboard=keyboard_btn(menu=buildings_info[build][0], lvl_cas=data[7]))

@bot.on.private_message(text='⛏Шахта', state=States.BUILDINGS_MENU)
async def castle(message: Message):
    build = 'mine'
    await bot.state_dispenser.set(message.peer_id, States.BUILDINGS_MINE)
    data = DB.get_row_users(message.from_id)
    building_data = DB.get_row('economic', buildings_info[build][1] + data[8])
    if data[8] < 30:
        if data[3] - building_data[4] < 0:
            gold = '❌'
        else:
            gold = '✅'
        if data[4] - building_data[5] < 0:
            wood = '❌'
        else:
            wood = '✅'
        if data[5] - building_data[6] < 0:
            ore = '❌'
        else:
            ore = '✅'
        next_income = DB.get_row('economic', buildings_info[build][1] + data[8] + 1)[3]
        re_lst, to_lst = ['bname', 'blevel', 'income', 'next_gold', 'next_wood', 'next_ore', 'next_income', 'time'], [buildings_info[build][0], data[8], str(building_data[3]) + buildings_info[build][2], gold + str(building_data[4]), wood + str(building_data[5]), ore + str(building_data[6]), str(next_income) + buildings_info[build][2], time_formatter(building_data[9])]
        msg_to_re = msg_buildings
    else:
        re_lst, to_lst = ['bname', 'blevel', 'income'], [buildings_info[build][0], data[8], str(building_data[3]) + buildings_info[build][2]]
        msg_to_re = msg_build_max_level
    for i, j in zip(re_lst, to_lst):
        msg_to_re = msg_to_re.replace(i, str(j), 1)
    await message.answer(msg_to_re, keyboard=keyboard_btn(buildings_info[build][0], lvl_cas=data[7]))

@bot.on.private_message(text='⚒Улучшить', state=States.BUILDINGS_MINE)
async def castle(message: Message):
    build = 'mine'
    data = DB.get_row_users(message.from_id)
    building_data = DB.get_row('economic', buildings_info[build][1] + data[8])
    if data[8] < 30:
        if data[15]:
            if data[3] >= building_data[4] and data[4] >= building_data[5] and data[5] >= building_data[6]:
                DB.set_cell('users', data[1], 'res_gol', data[3] - building_data[4])
                DB.set_cell('users', data[1], 'res_wod', data[4] - building_data[5])
                DB.set_cell('users', data[1], 'res_ore', data[5] - building_data[6])
                DB.new_event('up_mine', data[1], building_data[9])
                DB.set_cell('users', data[1], 'builders', data[15] - 1)
                await message.answer('Улучшение началось!', keyboard=keyboard_btn(buildings_info[build][0], lvl_cas=data[7]))
            else:
                s = 'Не хватает для улучшения:\n\n'
                if data[3] - building_data[4] < 0:
                    s += f'💰Золото: {abs(data[3] - building_data[4])}'
                if data[4] - building_data[5] < 0:
                    s += f'🌲Дерево: {abs(data[4] - building_data[5])}'
                if data[5] - building_data[6] < 0:
                    s += f'⛏Руда: {abs(data[5] - building_data[6])}'
                await message.answer(s, keyboard=keyboard_btn(buildings_info[build][0], lvl_cas=data[7]))
        else:
            r = [DB.get_row_event('up_convoy', data[1]), DB.get_row_event('up_farm', data[1]), DB.get_row_event('up_sawmill', data[1]), DB.get_row_event('up_castle', data[1]), DB.get_row_event('up_mine', data[1])]
            for i in r:
                if i:
                    r = i[0]
                    break
            if r[1] == 'up_convoy':
                s = f"На данный момент все строители заняты.\n\n⚒Идет строительство:\n⚖Караван ур. {data[11] + 1}\n⏳Осталось: {time_formatter(r[2])}\n\nТы можешь ускорить строительство за кристаллы, или купить еще одного строителя на 🎪Рынке в 🔮Лавке, чтобы строить сразу несколько зданий."
            elif r[1] == 'up_farm':
                s = f"На данный момент все строители заняты.\n\n⚒Идет строительство:\n🌻Ферма ур. {data[10] + 1}\n⏳Осталось: {time_formatter(r[2])}\n\nТы можешь ускорить строительство за кристаллы, или купить еще одного строителя на 🎪Рынке в 🔮Лавке, чтобы строить сразу несколько зданий."
            elif r[1] == 'up_sawmill':
                s = f"На данный момент все строители заняты.\n\n⚒Идет строительство:\n🌲Лесопилка ур. {data[9] + 1}\n⏳Осталось: {time_formatter(r[2])}\n\nТы можешь ускорить строительство за кристаллы, или купить еще одного строителя на 🎪Рынке в 🔮Лавке, чтобы строить сразу несколько зданий."
            elif r[1] == 'up_castle':
                s = f"На данный момент все строители заняты.\n\n⚒Идет строительство:\n🕍Замок ур. {data[7] + 1}\n⏳Осталось: {time_formatter(r[2])}\n\nТы можешь ускорить строительство за кристаллы, или купить еще одного строителя на 🎪Рынке в 🔮Лавке, чтобы строить сразу несколько зданий."
            elif r[1] == 'up_mine':
                s = f"На данный момент все строители заняты.\n\n⚒Идет строительство:\n⛏Шахта ур. {data[8] + 1}\n⏳Осталось: {time_formatter(r[2])}\n\nТы можешь ускорить строительство за кристаллы, или купить еще одного строителя на 🎪Рынке в 🔮Лавке, чтобы строить сразу несколько зданий."
            await message.answer(s, keyboard=keyboard_btn(buildings_info[build][0], lvl_cas=data[7]))
    else:
        await message.answer('Здание улучшено на максимум', keyboard=keyboard_btn(buildings_info[build][0], lvl_cas=data[7]))

@bot.on.private_message(text='👈Назад', state=States.BUILDINGS_MINE)
async def war(message: Message):
    data = DB.get_row_users(message.from_id)
    await bot.state_dispenser.set(message.peer_id, States.BUILDINGS_MENU)
    lst = [
        DB.get_row_event('up_mine', data[1]),
        DB.get_row_event('up_farm', data[1]),
        DB.get_row_event('up_castle', data[1]),
        DB.get_row_event('up_sawmill', data[1]),
        DB.get_row_event('up_convoy', data[1])
    ]
    s = ''
    for i in lst:
        if i:
            s = f"\n\nВедётся улучшение здания {buildings_info[i[0][1].split('_')[1]][0]} ещё {time_formatter(i[0][2])}"
            break
    if s:
        await message.answer(f'Твои постройки:\n\n🕍Замок: ур. {data[7]}\n🌻Ферма: ур. {data[10]}\n🌲Лесопилка: ур. {data[9]}\n⛏Шахта: ур. {data[8]}\n⚖Караван: ур. {data[11]}' + s, keyboard=keyboard_btn(menu='buildings', lvl_cas=data[7], skip=i[0][2] // 180 + 1))
    else:
        await message.answer(f'Твои постройки:\n\n🕍Замок: ур. {data[7]}\n🌻Ферма: ур. {data[10]}\n🌲Лесопилка: ур. {data[9]}\n⛏Шахта: ур. {data[8]}\n⚖Караван: ур. {data[11]}', keyboard=keyboard_btn(menu='buildings', lvl_cas=data[7]))

@bot.on.private_message(text='📖Инфо', state=States.BUILDINGS_MINE)
async def war(message: Message):
    build = 'mine'
    data = DB.get_row_users(message.from_id)
    building_data = DB.get_row('economic', buildings_info[build][1] + data[8])
    if data[8] < 30:
        if data[3] - building_data[4] < 0:
            gold = '❌'
        else:
            gold = '✅'
        if data[4] - building_data[5] < 0:
            wood = '❌'
        else:
            wood = '✅'
        if data[5] - building_data[6] < 0:
            ore = '❌'
        else:
            ore = '✅'
        next_income = DB.get_row('economic', buildings_info[build][1] + data[7] + 1)[3]
        re_lst, to_lst = ['bname', 'blevel', 'income', 'next_gold', 'next_wood', 'next_ore', 'next_income', 'time'], [buildings_info[build][0], data[8], str(building_data[3]) + buildings_info[build][2], str(building_data[4]) + gold, str(building_data[5]) + wood, str(building_data[6]) + ore, str(next_income) + buildings_info[build][2], time_formatter(building_data[9])]
        msg_to_re = msg_buildings
    else:
        re_lst, to_lst = ['bname', 'blevel', 'income'], [buildings_info[build][0], data[8], str(building_data[3]) + buildings_info[build][2]]
        msg_to_re = msg_build_max_level
    for i, j in zip(re_lst, to_lst):
        msg_to_re = msg_to_re.replace(i, str(j), 1)
    await message.answer(msg_to_re, keyboard=keyboard_btn(buildings_info[build][0], lvl_cas=data[7]))

@bot.on.private_message(text='📜Помощь', state=States.BUILDINGS_MINE)
async def war(message: Message):
    build = 'mine'
    data = DB.get_row_users(message.from_id)
    await message.answer(msg_mine_help, keyboard=keyboard_btn(menu=buildings_info[build][0], lvl_cas=data[7]))

@bot.on.private_message(text='🌲Лесопилка', state=States.BUILDINGS_MENU)
async def castle(message: Message):
    build = 'sawmill'
    await bot.state_dispenser.set(message.peer_id, States.BUILDINGS_SAWMILL)
    data = DB.get_row_users(message.from_id)
    building_data = DB.get_row('economic', buildings_info[build][1] + data[9])
    if data[9] < 30:
        if data[3] - building_data[4] < 0:
            gold = '❌'
        else:
            gold = '✅'
        if data[4] - building_data[5] < 0:
            wood = '❌'
        else:
            wood = '✅'
        if data[5] - building_data[6] < 0:
            ore = '❌'
        else:
            ore = '✅'
        next_income = DB.get_row('economic', buildings_info[build][1] + data[9] + 1)[3]
        re_lst, to_lst = ['bname', 'blevel', 'income', 'next_gold', 'next_wood', 'next_ore', 'next_income', 'time'], [buildings_info[build][0], data[9], str(building_data[3]) + buildings_info[build][2], gold + str(building_data[4]), wood + str(building_data[5]), ore + str(building_data[6]), str(next_income) + buildings_info[build][2], time_formatter(building_data[9])]
        msg_to_re = msg_buildings
    else:
        re_lst, to_lst = ['bname', 'blevel', 'income'], [buildings_info[build][0], data[9], str(building_data[3]) + buildings_info[build][2]]
        msg_to_re = msg_build_max_level
    for i, j in zip(re_lst, to_lst):
        msg_to_re = msg_to_re.replace(i, str(j), 1)
    await message.answer(msg_to_re, keyboard=keyboard_btn(buildings_info[build][0], lvl_cas=data[7]))

@bot.on.private_message(text='⚒Улучшить', state=States.BUILDINGS_SAWMILL)
async def castle(message: Message):
    build = 'sawmill'
    data = DB.get_row_users(message.from_id)
    building_data = DB.get_row('economic', buildings_info[build][1] + data[9])
    if data[9] < 30:
        if data[15]:
            if data[3] >= building_data[4] and data[4] >= building_data[5] and data[5] >= building_data[6]:
                DB.set_cell('users', data[1], 'res_gol', data[3] - building_data[4])
                DB.set_cell('users', data[1], 'res_wod', data[4] - building_data[5])
                DB.set_cell('users', data[1], 'res_ore', data[5] - building_data[6])
                DB.new_event('up_sawmill', data[1], building_data[9])
                DB.set_cell('users', data[1], 'builders', data[15] - 1)
                await message.answer('Улучшение началось!', keyboard=keyboard_btn(buildings_info[build][0], lvl_cas=data[7]))
            else:
                s = 'Не хватает для улучшения:\n\n'
                if data[3] - building_data[4] < 0:
                    s += f'💰Золото: {abs(data[3] - building_data[4])}'
                if data[4] - building_data[5] < 0:
                    s += f'🌲Дерево: {abs(data[4] - building_data[5])}'
                if data[5] - building_data[6] < 0:
                    s += f'⛏Руда: {abs(data[5] - building_data[6])}'
                await message.answer(s, keyboard=keyboard_btn(buildings_info[build][0], lvl_cas=data[7]))
        else:
            r = [DB.get_row_event('up_convoy', data[1]), DB.get_row_event('up_farm', data[1]), DB.get_row_event('up_sawmill', data[1]), DB.get_row_event('up_castle', data[1]), DB.get_row_event('up_mine', data[1])]
            for i in r:
                if i:
                    r = i[0]
                    break
            if r[1] == 'up_convoy':
                s = f"На данный момент все строители заняты.\n\n⚒Идет строительство:\n⚖Караван ур. {data[11] + 1}\n⏳Осталось: {time_formatter(r[2])}\n\nТы можешь ускорить строительство за кристаллы, или купить еще одного строителя на 🎪Рынке в 🔮Лавке, чтобы строить сразу несколько зданий."
            elif r[1] == 'up_farm':
                s = f"На данный момент все строители заняты.\n\n⚒Идет строительство:\n🌻Ферма ур. {data[10] + 1}\n⏳Осталось: {time_formatter(r[2])}\n\nТы можешь ускорить строительство за кристаллы, или купить еще одного строителя на 🎪Рынке в 🔮Лавке, чтобы строить сразу несколько зданий."
            elif r[1] == 'up_sawmill':
                s = f"На данный момент все строители заняты.\n\n⚒Идет строительство:\n🌲Лесопилка ур. {data[9] + 1}\n⏳Осталось: {time_formatter(r[2])}\n\nТы можешь ускорить строительство за кристаллы, или купить еще одного строителя на 🎪Рынке в 🔮Лавке, чтобы строить сразу несколько зданий."
            elif r[1] == 'up_castle':
                s = f"На данный момент все строители заняты.\n\n⚒Идет строительство:\n🕍Замок ур. {data[7] + 1}\n⏳Осталось: {time_formatter(r[2])}\n\nТы можешь ускорить строительство за кристаллы, или купить еще одного строителя на 🎪Рынке в 🔮Лавке, чтобы строить сразу несколько зданий."
            elif r[1] == 'up_mine':
                s = f"На данный момент все строители заняты.\n\n⚒Идет строительство:\n⛏Шахта ур. {data[8] + 1}\n⏳Осталось: {time_formatter(r[2])}\n\nТы можешь ускорить строительство за кристаллы, или купить еще одного строителя на 🎪Рынке в 🔮Лавке, чтобы строить сразу несколько зданий."
            await message.answer(s, keyboard=keyboard_btn(buildings_info[build][0], lvl_cas=data[7]))
    else:
        await message.answer('Здание улучшено на максимум', keyboard=keyboard_btn(buildings_info[build][0], lvl_cas=data[7]))

@bot.on.private_message(text='👈Назад', state=States.BUILDINGS_SAWMILL)
async def war(message: Message):
    data = DB.get_row_users(message.from_id)
    await bot.state_dispenser.set(message.peer_id, States.BUILDINGS_MENU)
    lst = [
        DB.get_row_event('up_mine', data[1]),
        DB.get_row_event('up_farm', data[1]),
        DB.get_row_event('up_castle', data[1]),
        DB.get_row_event('up_sawmill', data[1]),
        DB.get_row_event('up_convoy', data[1])
    ]
    s = ''
    for i in lst:
        if i:
            s = f"\n\nВедётся улучшение здания {buildings_info[i[0][1].split('_')[1]][0]} ещё {time_formatter(i[0][2])}"
            break
    if s:
        await message.answer(f'Твои постройки:\n\n🕍Замок: ур. {data[7]}\n🌻Ферма: ур. {data[10]}\n🌲Лесопилка: ур. {data[9]}\n⛏Шахта: ур. {data[8]}\n⚖Караван: ур. {data[11]}' + s, keyboard=keyboard_btn(menu='buildings', lvl_cas=data[7], skip=i[0][2] // 180 + 1))
    else:
        await message.answer(f'Твои постройки:\n\n🕍Замок: ур. {data[7]}\n🌻Ферма: ур. {data[10]}\n🌲Лесопилка: ур. {data[9]}\n⛏Шахта: ур. {data[8]}\n⚖Караван: ур. {data[11]}', keyboard=keyboard_btn(menu='buildings', lvl_cas=data[7]))

@bot.on.private_message(text='📖Инфо', state=States.BUILDINGS_SAWMILL)
async def war(message: Message):
    build = 'sawmill'
    data = DB.get_row_users(message.from_id)
    building_data = DB.get_row('economic', buildings_info[build][1] + data[9])
    if data[9] < 30:
        if data[3] - building_data[4] < 0:
            gold = '❌'
        else:
            gold = '✅'
        if data[4] - building_data[5] < 0:
            wood = '❌'
        else:
            wood = '✅'
        if data[5] - building_data[6] < 0:
            ore = '❌'
        else:
            ore = '✅'
        next_income = DB.get_row('economic', buildings_info[build][1] + data[9] + 1)[3]
        re_lst, to_lst = ['bname', 'blevel', 'income', 'next_gold', 'next_wood', 'next_ore', 'next_income', 'time'], [buildings_info[build][0], data[9], str(building_data[3]) + buildings_info[build][2], gold + str(building_data[4]), wood + str(building_data[5]), ore + str(building_data[6]), str(next_income) + buildings_info[build][2], time_formatter(building_data[9])]
        msg_to_re = msg_buildings
    else:
        re_lst, to_lst = ['bname', 'blevel', 'income'], [buildings_info[build][0], data[9], str(building_data[3]) + buildings_info[build][2]]
        msg_to_re = msg_build_max_level
    for i, j in zip(re_lst, to_lst):
        msg_to_re = msg_to_re.replace(i, str(j), 1)
    await message.answer(msg_to_re, keyboard=keyboard_btn(buildings_info[build][0], lvl_cas=data[7]))

@bot.on.private_message(text='📜Помощь', state=States.BUILDINGS_SAWMILL)
async def war(message: Message):
    build = 'sawmill'
    data = DB.get_row_users(message.from_id)
    await message.answer(msg_sawmill_help, keyboard=keyboard_btn(menu=buildings_info[build][0], lvl_cas=data[7]))

@bot.on.private_message(text='🌻Ферма', state=States.BUILDINGS_MENU)
async def castle(message: Message):
    data = DB.get_row_users(message.from_id)
    if data[7] < 4:
        await message.answer(msg_farm_den, keyboard=keyboard_btn(menu='buildings', lvl_cas=data[7]))
    else:
        build = 'farm'
        await bot.state_dispenser.set(message.peer_id, States.BUILDINGS_FARM)
        building_data = DB.get_row('economic', buildings_info[build][1] + data[10])
        if data[10] < 30:
            if data[3] - building_data[4] < 0:
                gold = '❌'
            else:
                gold = '✅'
            if data[4] - building_data[5] < 0:
                wood = '❌'
            else:
                wood = '✅'
            if data[5] - building_data[6] < 0:
                ore = '❌'
            else:
                ore = '✅'
            next_income = DB.get_row('economic', buildings_info[build][1] + data[10] + 1)[3]
            re_lst, to_lst = ['bname', 'blevel', 'income', 'next_gold', 'next_wood', 'next_ore', 'next_income', 'time'], [buildings_info[build][0], data[10], str(building_data[3]) + buildings_info[build][2], gold + str(building_data[4]), wood + str(building_data[5]), ore + str(building_data[6]), str(next_income) + buildings_info[build][2], time_formatter(building_data[9])]
            msg_to_re = msg_buildings
        else:
            re_lst, to_lst = ['bname', 'blevel', 'income'], [buildings_info[build][0], data[10], str(building_data[3]) + buildings_info[build][2]]
            msg_to_re = msg_build_max_level
        for i, j in zip(re_lst, to_lst):
            msg_to_re = msg_to_re.replace(i, str(j), 1)
        await message.answer(msg_to_re, keyboard=keyboard_btn(buildings_info[build][0], lvl_cas=data[7]))

@bot.on.private_message(text='⚒Улучшить', state=States.BUILDINGS_FARM)
async def castle(message: Message):
    build = 'farm'
    data = DB.get_row_users(message.from_id)
    building_data = DB.get_row('economic', buildings_info[build][1] + data[10])
    if data[10] < 30:
        if data[15]:
            if data[3] >= building_data[4] and data[4] >= building_data[5] and data[5] >= building_data[6]:
                DB.set_cell('users', data[1], 'res_gol', data[3] - building_data[4])
                DB.set_cell('users', data[1], 'res_wod', data[4] - building_data[5])
                DB.set_cell('users', data[1], 'res_ore', data[5] - building_data[6])
                DB.new_event('up_farm', data[1], building_data[9])
                DB.set_cell('users', data[1], 'builders', data[15] - 1)
                await message.answer('Улучшение началось!', keyboard=keyboard_btn(buildings_info[build][0], lvl_cas=data[7]))
            else:
                s = 'Не хватает для улучшения:\n\n'
                if data[3] - building_data[4] < 0:
                    s += f'💰Золото: {abs(data[3] - building_data[4])}'
                if data[4] - building_data[5] < 0:
                    s += f'🌲Дерево: {abs(data[4] - building_data[5])}'
                if data[5] - building_data[6] < 0:
                    s += f'⛏Руда: {abs(data[5] - building_data[6])}'
                await message.answer(s, keyboard=keyboard_btn(buildings_info[build][0], lvl_cas=data[7]))
        else:
            r = [DB.get_row_event('up_convoy', data[1]), DB.get_row_event('up_farm', data[1]), DB.get_row_event('up_sawmill', data[1]), DB.get_row_event('up_castle', data[1]), DB.get_row_event('up_mine', data[1])]
            for i in r:
                if i:
                    r = i[0]
                    break
            if r[1] == 'up_convoy':
                s = f"На данный момент все строители заняты.\n\n⚒Идет строительство:\n⚖Караван ур. {data[11] + 1}\n⏳Осталось: {time_formatter(r[2])}\n\nТы можешь ускорить строительство за кристаллы, или купить еще одного строителя на 🎪Рынке в 🔮Лавке, чтобы строить сразу несколько зданий."
            elif r[1] == 'up_farm':
                s = f"На данный момент все строители заняты.\n\n⚒Идет строительство:\n🌻Ферма ур. {data[10] + 1}\n⏳Осталось: {time_formatter(r[2])}\n\nТы можешь ускорить строительство за кристаллы, или купить еще одного строителя на 🎪Рынке в 🔮Лавке, чтобы строить сразу несколько зданий."
            elif r[1] == 'up_sawmill':
                s = f"На данный момент все строители заняты.\n\n⚒Идет строительство:\n🌲Лесопилка ур. {data[9] + 1}\n⏳Осталось: {time_formatter(r[2])}\n\nТы можешь ускорить строительство за кристаллы, или купить еще одного строителя на 🎪Рынке в 🔮Лавке, чтобы строить сразу несколько зданий."
            elif r[1] == 'up_castle':
                s = f"На данный момент все строители заняты.\n\n⚒Идет строительство:\n🕍Замок ур. {data[7] + 1}\n⏳Осталось: {time_formatter(r[2])}\n\nТы можешь ускорить строительство за кристаллы, или купить еще одного строителя на 🎪Рынке в 🔮Лавке, чтобы строить сразу несколько зданий."
            elif r[1] == 'up_mine':
                s = f"На данный момент все строители заняты.\n\n⚒Идет строительство:\n⛏Шахта ур. {data[8] + 1}\n⏳Осталось: {time_formatter(r[2])}\n\nТы можешь ускорить строительство за кристаллы, или купить еще одного строителя на 🎪Рынке в 🔮Лавке, чтобы строить сразу несколько зданий."
            await message.answer(s, keyboard=keyboard_btn(buildings_info[build][0], lvl_cas=data[7]))
    else:
        await message.answer('Здание улучшено на максимум', keyboard=keyboard_btn(buildings_info[build][0], lvl_cas=data[7]))

@bot.on.private_message(text='👈Назад', state=States.BUILDINGS_FARM)
async def war(message: Message):
    data = DB.get_row_users(message.from_id)
    await bot.state_dispenser.set(message.peer_id, States.BUILDINGS_MENU)
    lst = [
        DB.get_row_event('up_mine', data[1]),
        DB.get_row_event('up_farm', data[1]),
        DB.get_row_event('up_castle', data[1]),
        DB.get_row_event('up_sawmill', data[1]),
        DB.get_row_event('up_convoy', data[1])
    ]
    s = ''
    for i in lst:
        if i:
            s = f"\n\nВедётся улучшение здания {buildings_info[i[0][1].split('_')[1]][0]} ещё {time_formatter(i[0][2])}"
            break
    if s:
        await message.answer(f'Твои постройки:\n\n🕍Замок: ур. {data[7]}\n🌻Ферма: ур. {data[10]}\n🌲Лесопилка: ур. {data[9]}\n⛏Шахта: ур. {data[8]}\n⚖Караван: ур. {data[11]}' + s, keyboard=keyboard_btn(menu='buildings', lvl_cas=data[7], skip=i[0][2] // 180 + 1))
    else:
        await message.answer(f'Твои постройки:\n\n🕍Замок: ур. {data[7]}\n🌻Ферма: ур. {data[10]}\n🌲Лесопилка: ур. {data[9]}\n⛏Шахта: ур. {data[8]}\n⚖Караван: ур. {data[11]}', keyboard=keyboard_btn(menu='buildings', lvl_cas=data[7]))

@bot.on.private_message(text='📖Инфо', state=States.BUILDINGS_FARM)
async def war(message: Message):
    build = 'farm'
    data = DB.get_row_users(message.from_id)
    building_data = DB.get_row('economic', buildings_info[build][1] + data[10])
    if data[10] < 30:
        if data[3] - building_data[4] < 0:
            gold = '❌'
        else:
            gold = '✅'
        if data[4] - building_data[5] < 0:
            wood = '❌'
        else:
            wood = '✅'
        if data[5] - building_data[6] < 0:
            ore = '❌'
        else:
            ore = '✅'
        next_income = DB.get_row('economic', buildings_info[build][1] + data[10] + 1)[3]
        re_lst, to_lst = ['bname', 'blevel', 'income', 'next_gold', 'next_wood', 'next_ore', 'next_income', 'time'], [buildings_info[build][0], data[10], str(building_data[3]) + buildings_info[build][2], gold + str(building_data[4]), wood + str(building_data[5]), ore + str(building_data[6]), str(next_income) + buildings_info[build][2], time_formatter(building_data[9])]
        msg_to_re = msg_buildings
    else:
        re_lst, to_lst = ['bname', 'blevel', 'income'], [buildings_info[build][0], data[10], str(building_data[3]) + buildings_info[build][2]]
        msg_to_re = msg_build_max_level
    for i, j in zip(re_lst, to_lst):
        msg_to_re = msg_to_re.replace(i, str(j), 1)
    await message.answer(msg_to_re, keyboard=keyboard_btn(buildings_info[build][0], lvl_cas=data[7]))

@bot.on.private_message(text='📜Помощь', state=States.BUILDINGS_FARM)
async def war(message: Message):
    build = 'farm'
    data = DB.get_row_users(message.from_id)
    await message.answer(msg_farm_help, keyboard=keyboard_btn(menu=buildings_info[build][0], lvl_cas=data[7]))

@bot.on.private_message(text='⚖Караван', state=States.BUILDINGS_MENU)
async def castle(message: Message):
    data = DB.get_row_users(message.from_id)
    if data[7] < 5:
        await message.answer(msg_con_den, keyboard=keyboard_btn(menu='buildings', lvl_cas=data[7]))
    else:
        build = 'convoy'
        await bot.state_dispenser.set(message.peer_id, States.BUILDINGS_CONVOY)
        building_data = DB.get_row('economic', buildings_info[build][1] + data[11])
        if data[11] < 30:
            if data[3] - building_data[4] < 0:
                gold = '❌'
            else:
                gold = '✅'
            if data[4] - building_data[5] < 0:
                wood = '❌'
            else:
                wood = '✅'
            if data[5] - building_data[6] < 0:
                ore = '❌'
            else:
                ore = '✅'
            next_income = DB.get_row('economic', buildings_info[build][1] + data[11] + 1)[3]
            re_lst, to_lst = ['bname', 'blevel', 'income', 'next_gold', 'next_wood', 'next_ore', 'next_income', 'time'], [buildings_info[build][0], data[11], str(building_data[3]) + buildings_info[build][2], gold + str(building_data[4]), wood + str(building_data[5]), ore + str(building_data[6]), str(next_income) + buildings_info[build][2], time_formatter(building_data[9])]
            msg_to_re = msg_buildings
        else:
            re_lst, to_lst = ['bname', 'send_today', 'blevel', 'income', 'limit'], [buildings_info[build][0], data[22], data[11], str(building_data[3]) + buildings_info[build][2], building_data[10]]
            msg_to_re = msg_convoy_max_level
        for i, j in zip(re_lst, to_lst):
            msg_to_re = msg_to_re.replace(i, str(j), 1)
        await message.answer(msg_to_re, keyboard=keyboard_btn(buildings_info[build][0], lvl_cas=data[7]))

@bot.on.private_message(text='⚒Улучшить', state=States.BUILDINGS_CONVOY)
async def castle(message: Message):
    build = 'convoy'
    data = DB.get_row_users(message.from_id)
    building_data = DB.get_row('economic', buildings_info[build][1] + data[11])
    if data[11] < 30:
        if data[15]:
            if data[3] >= building_data[4] and data[4] >= building_data[5] and data[5] >= building_data[6]:
                DB.set_cell('users', data[1], 'res_gol', data[3] - building_data[4])
                DB.set_cell('users', data[1], 'res_wod', data[4] - building_data[5])
                DB.set_cell('users', data[1], 'res_ore', data[5] - building_data[6])
                DB.new_event('up_convoy', data[1], building_data[9])
                DB.set_cell('users', data[1], 'builders', data[15] - 1)
                await message.answer('Улучшение началось!', keyboard=keyboard_btn(buildings_info[build][0], lvl_cas=data[7]))
            else:
                s = 'Не хватает для улучшения:\n\n'
                if data[3] - building_data[4] < 0:
                    s += f'💰Золото: {abs(data[3] - building_data[4])}'
                if data[4] - building_data[5] < 0:
                    s += f'🌲Дерево: {abs(data[4] - building_data[5])}'
                if data[5] - building_data[6] < 0:
                    s += f'⛏Руда: {abs(data[5] - building_data[6])}'
                await message.answer(s, keyboard=keyboard_btn(buildings_info[build][0], lvl_cas=data[7]))
        else:
            r = [DB.get_row_event('up_convoy', data[1]), DB.get_row_event('up_farm', data[1]), DB.get_row_event('up_sawmill', data[1]), DB.get_row_event('up_castle', data[1]), DB.get_row_event('up_mine', data[1])]
            for i in r:
                if i:
                    r = i[0]
                    break
            if r[1] == 'up_convoy':
                s = f"На данный момент все строители заняты.\n\n⚒Идет строительство:\n⚖Караван ур. {data[11] + 1}\n⏳Осталось: {time_formatter(r[2])}\n\nТы можешь ускорить строительство за кристаллы, или купить еще одного строителя на 🎪Рынке в 🔮Лавке, чтобы строить сразу несколько зданий."
            elif r[1] == 'up_farm':
                s = f"На данный момент все строители заняты.\n\n⚒Идет строительство:\n🌻Ферма ур. {data[10] + 1}\n⏳Осталось: {time_formatter(r[2])}\n\nТы можешь ускорить строительство за кристаллы, или купить еще одного строителя на 🎪Рынке в 🔮Лавке, чтобы строить сразу несколько зданий."
            elif r[1] == 'up_sawmill':
                s = f"На данный момент все строители заняты.\n\n⚒Идет строительство:\n🌲Лесопилка ур. {data[9] + 1}\n⏳Осталось: {time_formatter(r[2])}\n\nТы можешь ускорить строительство за кристаллы, или купить еще одного строителя на 🎪Рынке в 🔮Лавке, чтобы строить сразу несколько зданий."
            elif r[1] == 'up_castle':
                s = f"На данный момент все строители заняты.\n\n⚒Идет строительство:\n🕍Замок ур. {data[7] + 1}\n⏳Осталось: {time_formatter(r[2])}\n\nТы можешь ускорить строительство за кристаллы, или купить еще одного строителя на 🎪Рынке в 🔮Лавке, чтобы строить сразу несколько зданий."
            elif r[1] == 'up_mine':
                s = f"На данный момент все строители заняты.\n\n⚒Идет строительство:\n⛏Шахта ур. {data[8] + 1}\n⏳Осталось: {time_formatter(r[2])}\n\nТы можешь ускорить строительство за кристаллы, или купить еще одного строителя на 🎪Рынке в 🔮Лавке, чтобы строить сразу несколько зданий."
            await message.answer(s, keyboard=keyboard_btn(buildings_info[build][0], lvl_cas=data[7]))
    else:
        await message.answer('Здание улучшено на максимум', keyboard=keyboard_btn(buildings_info[build][0], lvl_cas=data[7]))

@bot.on.private_message(text='👈Назад', state=States.BUILDINGS_CONVOY)
async def war(message: Message):
    data = DB.get_row_users(message.from_id)
    await bot.state_dispenser.set(message.peer_id, States.BUILDINGS_MENU)
    lst = [
        DB.get_row_event('up_mine', data[1]),
        DB.get_row_event('up_farm', data[1]),
        DB.get_row_event('up_castle', data[1]),
        DB.get_row_event('up_sawmill', data[1]),
        DB.get_row_event('up_convoy', data[1])
    ]
    s = ''
    for i in lst:
        if i:
            s = f"\n\nВедётся улучшение здания {buildings_info[i[0][1].split('_')[1]][0]} ещё {time_formatter(i[0][2])}"
            break
    if s:
        await message.answer(f'Твои постройки:\n\n🕍Замок: ур. {data[7]}\n🌻Ферма: ур. {data[10]}\n🌲Лесопилка: ур. {data[9]}\n⛏Шахта: ур. {data[8]}\n⚖Караван: ур. {data[11]}' + s, keyboard=keyboard_btn(menu='buildings', lvl_cas=data[7], skip=i[0][2] // 180 + 1))
    else:
        await message.answer(f'Твои постройки:\n\n🕍Замок: ур. {data[7]}\n🌻Ферма: ур. {data[10]}\n🌲Лесопилка: ур. {data[9]}\n⛏Шахта: ур. {data[8]}\n⚖Караван: ур. {data[11]}', keyboard=keyboard_btn(menu='buildings', lvl_cas=data[7]))

@bot.on.private_message(text='📖Инфо', state=States.BUILDINGS_CONVOY)
async def war(message: Message):
    build = 'convoy'
    data = DB.get_row_users(message.from_id)
    building_data = DB.get_row('economic', buildings_info[build][1] + data[11])
    if data[11] < 30:
        if data[3] - building_data[4] < 0:
            gold = '❌'
        else:
            gold = '✅'
        if data[4] - building_data[5] < 0:
            wood = '❌'
        else:
            wood = '✅'
        if data[5] - building_data[6] < 0:
            ore = '❌'
        else:
            ore = '✅'
        next_income = DB.get_row('economic', buildings_info[build][1] + data[11] + 1)[3]
        re_lst, to_lst = ['bname', 'blevel', 'income', 'next_gold', 'next_wood', 'next_ore', 'next_income', 'time'], [buildings_info[build][0], data[11], str(building_data[3]) + buildings_info[build][2], gold + str(building_data[4]), wood + str(building_data[5]), ore + str(building_data[6]), str(next_income) + buildings_info[build][2], time_formatter(building_data[9])]
        msg_to_re = msg_buildings
    else:
        re_lst, to_lst = ['bname', 'blevel', 'income'], [buildings_info[build][0], data[11], str(building_data[3]) + buildings_info[build][2]]
        msg_to_re = msg_build_max_level
    for i, j in zip(re_lst, to_lst):
        msg_to_re = msg_to_re.replace(i, str(j), 1)
    await message.answer(msg_to_re, keyboard=keyboard_btn(buildings_info[build][0], lvl_cas=data[7]))

@bot.on.private_message(text='📜Помощь', state=States.BUILDINGS_CONVOY)
async def war(message: Message):
    build = 'convoy'
    data = DB.get_row_users(message.from_id)
    await message.answer(msg_con_help, keyboard=keyboard_btn(menu=buildings_info[build][0], lvl_cas=data[7]))

@bot.on.private_message(state=States.BUILDINGS_CONVOY)
async def start_1(message: Message):
    build = 'convoy'
    data = DB.get_row_users(message.from_id)
    userinfo = await bot.api.users.get(message.from_id)
    building_data = DB.get_row('economic', buildings_info[build][1] + data[11])
    if message.text == '🏕Домой':
        await bot.state_dispenser.set(message.peer_id, States.EMPTY)
        await message.answer(f'[id{message.from_id}|{userinfo[0].first_name}], твое королество:\n📖Игровой ID: {data[0]}\n\n💎Кристаллы: {data[2]}\n💰[{data[7]}]Золото: {data[3]}\n🌲[{data[9]}]Дерево: {data[4]}\n⛏[{data[8]}]Руда: {data[5]}\n🍖[{data[10]}]Еда: {data[6]}\n\nТерритория: {data[17]}🌍', keyboard=keyboard_menu(lvl_cas=data[7]))
    else:
        s = message.text.lower()
        if 'отправить' in s:
            try:
                s = s.split()
                user_to = DB.get_row('users', int(s[3]))
                if s[2] == 'золота':
                    s[1] = int(s[1])
                    if s[1] <= data[3]:
                        if data[22] + s[1] <= building_data[10]:
                            DB.set_cell('users', user_to[1], 'res_gol', user_to[3] + s[1])
                            DB.set_cell('users', data[1], 'res_gol', data[3] - s[1])
                            DB.set_cell('users', data[1], 'send_today', data[22] + s[1])
                            await message.answer('Ресурсы отправлены!', keyboard=keyboard_btn(menu=buildings_info[build][0], lvl_cas=data[7]))
                            await bot.api.messages.send(peer_id=user_to[1], message=f'Игрок [id{message.from_id}|{userinfo[0].first_name}] прислал вам {s[1]}💰 золота', random_id=0)
                        else:
                            await message.answer(msg_convoy_limit, keyboard=keyboard_btn(menu=buildings_info[build][0], lvl_cas=data[7]))
                    else:
                        await message.answer(msg_convoy_needmore, keyboard=keyboard_btn(menu=buildings_info[build][0], lvl_cas=data[7]))
                elif s[2] == 'дерева':
                    s[1] = int(s[1])
                    if s[1] <= data[4]:
                        if data[22] + s[1] <= building_data[10]:
                            DB.set_cell('users', user_to[1], 'res_wod', user_to[4] + s[1])
                            DB.set_cell('users', data[1], 'res_wod', data[4] - s[1])
                            DB.set_cell('users', data[1], 'send_today', data[22] + s[1])
                            await message.answer('Ресурсы отправлены!', keyboard=keyboard_btn(menu=buildings_info[build][0], lvl_cas=data[7]))
                            await bot.api.messages.send(peer_id=user_to[1], message=f'Игрок [id{message.from_id}|{userinfo[0].first_name}] прислал вам {s[1]}🌲 дерева', random_id=0)
                        else:
                            await message.answer(msg_convoy_limit, keyboard=keyboard_btn(menu=buildings_info[build][0], lvl_cas=data[7]))
                    else:
                        await message.answer(msg_convoy_needmore, keyboard=keyboard_btn(menu=buildings_info[build][0], lvl_cas=data[7]))
                elif s[2] == 'руды':
                    s[1] = int(s[1])
                    if s[1] <= s[1]:
                        if data[22] + data[5] <= building_data[10]:
                            DB.set_cell('users', user_to[1], 'res_ore', user_to[5] + s[1])
                            DB.set_cell('users', data[1], 'res_ore', data[5] - s[1])
                            DB.set_cell('users', data[1], 'send_today', data[22] + s[1])
                            await message.answer('Ресурсы отправлены!', keyboard=keyboard_btn(menu=buildings_info[build][0], lvl_cas=data[7]))
                            await bot.api.messages.send(peer_id=user_to[1], message=f'Игрок [id{message.from_id}|{userinfo[0].first_name}] прислал вам {s[1]}⛏ руды', random_id=0)
                        else:
                            await message.answer(msg_convoy_limit, keyboard=keyboard_btn(menu=buildings_info[build][0], lvl_cas=data[7]))
                    else:
                        await message.answer(msg_convoy_needmore, keyboard=keyboard_btn(menu=buildings_info[build][0], lvl_cas=data[7]))
                elif s[2] == 'еды':
                    s[1] = int(s[1])
                    if s[1] <= s[1]:
                        if data[22] + data[6] <= building_data[10]:
                            DB.set_cell('users', user_to[1], 'res_fod', user_to[6] + s[1])
                            DB.set_cell('users', data[1], 'res_fod', data[6] - s[1])
                            DB.set_cell('users', data[1], 'send_today', data[22] + s[1])
                            await message.answer('Ресурсы отправлены!', keyboard=keyboard_btn(menu=buildings_info[build][0], lvl_cas=data[7]))
                            await bot.api.messages.send(peer_id=user_to[1], message=f'Игрок [id{message.from_id}|{userinfo[0].first_name}] прислал вам {s[1]}🍖 еды', random_id=0)
                        else:
                            await message.answer(msg_convoy_limit, keyboard=keyboard_btn(menu=buildings_info[build][0], lvl_cas=data[7]))
                    else:
                        await message.answer(msg_convoy_needmore, keyboard=keyboard_btn(menu=buildings_info[build][0], lvl_cas=data[7]))
            except Exception as e:
                print(f'--------- {repr(e)} -----------')
                await message.answer(msg_convoy_error, keyboard=keyboard_btn(menu=buildings_info[build][0], lvl_cas=data[7]))
        else:
            await bot.state_dispenser.set(message.peer_id, States.EMPTY)
            userinfo = await bot.api.users.get(message.from_id)
            await message.answer(msg_error, keyboard=keyboard_menu(lvl_cas=data[7]))
            await message.answer(f'[id{message.from_id}|{userinfo[0].first_name}], твое королество:\n📖Игровой ID: {data[0]}\n\n💎Кристаллы: {data[2]}\n💰[{data[7]}]Золото: {data[3]}\n🌲[{data[9]}]Дерево: {data[4]}\n⛏[{data[8]}]Руда: {data[5]}\n🍖[{data[10]}]Еда: {data[6]}\n\nТерритория: {data[17]}🌍', keyboard=keyboard_menu(lvl_cas=data[7]))

@bot.on.private_message(state=States.BUILDINGS_MENU)
async def castle(message: Message):
    data = DB.get_row_users(message.from_id)
    if 'Пропустить за ' in message.text:
        lst = [
            DB.get_row_event('up_mine', data[1]),
            DB.get_row_event('up_farm', data[1]),
            DB.get_row_event('up_castle', data[1]),
            DB.get_row_event('up_sawmill', data[1]),
            DB.get_row_event('up_convoy', data[1])
        ]
        for i in lst:
            if i:
                s = f"Строительство здания {buildings_info[i[0][1].split('_')[1]][0]} ускорено за {i[0][2] // 180 + 1}💎"
                if data[2] >= i[0][2] // 180 + 1:
                    DB.set_cell_event('time', 3, data[1], i[0][1])
                    DB.set_cell('users', data[1], 'res_cry', data[2] - (i[0][2] // 180 + 1))
                    await message.answer(s, keyboard=keyboard_btn(menu='buildings', lvl_cas=data[7]))
                else:
                    await message.answer('Недостаточно 💎Кристаллов для ускорения', keyboard=keyboard_btn(menu='buildings', lvl_cas=data[7], skip=i[0][2] // 180 + 1))
                break
        
    else:
        userinfo = await bot.api.users.get(message.from_id)
        if message.text == '🏕Домой':
            await bot.state_dispenser.set(message.peer_id, States.EMPTY)
            await message.answer(f'[id{message.from_id}|{userinfo[0].first_name}], твое королество:\n📖Игровой ID: {data[0]}\n\n💎Кристаллы: {data[2]}\n💰[{data[7]}]Золото: {data[3]}\n🌲[{data[9]}]Дерево: {data[4]}\n⛏[{data[8]}]Руда: {data[5]}\n🍖[{data[10]}]Еда: {data[6]}\n\nТерритория: {data[17]}🌍', keyboard=keyboard_menu(lvl_cas=data[7]))
        else:
            await message.answer(msg_error, keyboard=keyboard_menu(lvl_cas=data[7]))
            await message.answer(f'[id{message.from_id}|{userinfo[0].first_name}], твое королество:\n📖Игровой ID: {data[0]}\n\n💎Кристаллы: {data[2]}\n💰[{data[7]}]Золото: {data[3]}\n🌲[{data[9]}]Дерево: {data[4]}\n⛏[{data[8]}]Руда: {data[5]}\n🍖[{data[10]}]Еда: {data[6]}\n\nТерритория: {data[17]}🌍', keyboard=keyboard_menu(lvl_cas=data[7]))
            await bot.state_dispenser.set(message.peer_id, States.EMPTY)

@bot.on.private_message(text='🔥Война')
async def war(message: Message):
    data = DB.get_row_users(message.from_id)
    if data[7] < 8:
        await message.answer(msg_war_den, keyboard=keyboard_menu(lvl_cas=data[7]))
    else:
        await bot.state_dispenser.set(message.peer_id, States.WAR_MENU)
        await message.answer(f'Побед: {data[16]}🎖\nТерритория: {data[17]}🌍\n\n⚔Пехоты: {data[18]}\n🏹Лучники: {data[19]}\n🏇Конницы: {data[20]}\n\n🔥Всего войск: {data[18] + data[19] + data[20]}', keyboard=keyboard_btn(menu='war', lvl_cas=data[7]))

@bot.on.private_message(text='⚔Пехота', state=States.WAR_MENU)
async def war(message: Message):
    data = DB.get_row_users(message.from_id)
    await bot.state_dispenser.set(message.peer_id, States.WAR_INFANTRY)
    await message.answer(f'🍖Еды: {data[6]}\n💰Золота: {data[3]}\n⚔Пехоты: {data[18]}\n\nЦена найма одного воина: 400🍖 и 150💰\nСколько ⚔Пехоты нужно нанять? Доступен ручной ввод', keyboard=keyboard_btn(menu='war_enemy', lvl_cas=data[7], enemy='⚔'))

@bot.on.private_message(text='👈Назад', state=States.WAR_INFANTRY)
async def war(message: Message):
    data = DB.get_row_users(message.from_id)
    await bot.state_dispenser.set(message.peer_id, States.WAR_MENU)
    await message.answer(f'Побед: {data[16]}🎖\nТерритория: {data[17]}🌍\n\n⚔Пехоты: {data[18]}\n🏹Лучники: {data[19]}\n🏇Конницы: {data[20]}\n\n🔥Всего войск: {data[18] + data[19] + data[20]}', keyboard=keyboard_btn(menu='war', lvl_cas=data[7]))

@bot.on.private_message(text='📜Помощь', state=States.WAR_INFANTRY)
async def war(message: Message):
    data = DB.get_row_users(message.from_id)
    await message.answer(msg_war_help, keyboard=keyboard_btn(menu='war_enemy', lvl_cas=data[7], enemy='⚔'))

@bot.on.private_message(state=States.WAR_INFANTRY)
async def war(message: Message):
    data = DB.get_row_users(message.from_id)
    s = message.text.replace('⚔', '')
    if s.isdigit():
        num = int(s)
        if num * 400 <= data[6] and num * 150 <= data[3]:
            DB.set_cell('users', data[1], 'res_fod', data[6] - num * 400)
            DB.set_cell('users', data[1], 'res_gol', data[4] - num * 150)
            DB.set_cell('users', data[1], 'infantry', data[18] + num)
            await message.answer('Войска наняты', keyboard=keyboard_btn(menu='war_enemy', lvl_cas=data[7], enemy='⚔'))
            dt = datetime.now()
            if dt.weekday() < 5 and not(dt.hour > 21 and dt.weekday() == 4) and not(dt.hour < 8 and not dt.weekday()):
                DB.set_cell('users', data[1], 'points', data[34] + num)
        else:
            await message.answer('Недостаточно еды или золота для найма', keyboard=keyboard_btn(menu='war_enemy', lvl_cas=data[7], enemy='⚔'))
    else:
        userinfo = await bot.api.users.get(message.from_id)
        if message.text == '🏕Домой':
            await bot.state_dispenser.set(message.peer_id, States.EMPTY)
            await message.answer(f'[id{message.from_id}|{userinfo[0].first_name}], твое королество:\n📖Игровой ID: {data[0]}\n\n💎Кристаллы: {data[2]}\n💰[{data[7]}]Золото: {data[3]}\n🌲[{data[9]}]Дерево: {data[4]}\n⛏[{data[8]}]Руда: {data[5]}\n🍖[{data[10]}]Еда: {data[6]}\n\nТерритория: {data[17]}🌍', keyboard=keyboard_menu(lvl_cas=data[7]))
        else:
            await message.answer(msg_error, keyboard=keyboard_menu(lvl_cas=data[7]))
            await message.answer(f'[id{message.from_id}|{userinfo[0].first_name}], твое королество:\n📖Игровой ID: {data[0]}\n\n💎Кристаллы: {data[2]}\n💰[{data[7]}]Золото: {data[3]}\n🌲[{data[9]}]Дерево: {data[4]}\n⛏[{data[8]}]Руда: {data[5]}\n🍖[{data[10]}]Еда: {data[6]}\n\nТерритория: {data[17]}🌍', keyboard=keyboard_menu(lvl_cas=data[7]))
            await bot.state_dispenser.set(message.peer_id, States.EMPTY)

@bot.on.private_message(text='🏹Лучники', state=States.WAR_MENU)
async def war(message: Message):
    data = DB.get_row_users(message.from_id)
    await bot.state_dispenser.set(message.peer_id, States.WAR_ARCHERS)
    await message.answer(f'🍖Еды: {data[6]}\n💰Золота: {data[3]}\n🏹Лучников: {data[19]}\n\nЦена найма одного воина: 400🍖 и 150💰\nСколько 🏹Лучников нужно нанять? Доступен ручной ввод', keyboard=keyboard_btn(menu='war_enemy', lvl_cas=data[7], enemy='🏹'))

@bot.on.private_message(text='👈Назад', state=States.WAR_ARCHERS)
async def war(message: Message):
    userinfo = await bot.api.users.get(message.from_id)
    data = DB.get_row_users(message.from_id)
    await bot.state_dispenser.set(message.peer_id, States.WAR_MENU)
    await message.answer(f'Побед: {data[16]}🎖\nТерритория: {data[17]}🌍\n\n⚔Пехоты: {data[18]}\n🏹Лучники: {data[19]}\n🏇Конницы: {data[20]}\n\n🔥Всего войск: {data[18] + data[19] + data[20]}', keyboard=keyboard_btn(menu='war', lvl_cas=data[7]))

@bot.on.private_message(text='📜Помощь', state=States.WAR_ARCHERS)
async def war(message: Message):
    data = DB.get_row_users(message.from_id)
    await message.answer(msg_war_help, keyboard=keyboard_btn(menu='war_enemy', lvl_cas=data[7], enemy='🏹'))

@bot.on.private_message(state=States.WAR_ARCHERS)
async def war(message: Message):
    data = DB.get_row_users(message.from_id)
    s = message.text.replace('🏹', '')
    if s.isdigit():
        num = int(s)
        if num * 400 <= data[6] and num * 150 <= data[3]:
            DB.set_cell('users', data[1], 'res_fod', data[6] - num * 400)
            DB.set_cell('users', data[1], 'res_gol', data[4] - num * 150)
            DB.set_cell('users', data[1], 'archers', data[19] + num)
            await message.answer('Войска наняты', keyboard=keyboard_btn(menu='war_enemy', lvl_cas=data[7], enemy='🏹'))
            dt = datetime.now()
            if dt.weekday() < 5 and not(dt.hour > 21 and dt.weekday() == 4) and not(dt.hour < 8 and not dt.weekday()):
                DB.set_cell('users', data[1], 'points', data[34] + num)
        else:
            await message.answer('Недостаточно еды или золота для найма', keyboard=keyboard_btn(menu='war_enemy', lvl_cas=data[7], enemy='🏹'))
    else:
        userinfo = await bot.api.users.get(message.from_id)
        if message.text == '🏕Домой':
            await bot.state_dispenser.set(message.peer_id, States.EMPTY)
            await message.answer(f'[id{message.from_id}|{userinfo[0].first_name}], твое королество:\n📖Игровой ID: {data[0]}\n\n💎Кристаллы: {data[2]}\n💰[{data[7]}]Золото: {data[3]}\n🌲[{data[9]}]Дерево: {data[4]}\n⛏[{data[8]}]Руда: {data[5]}\n🍖[{data[10]}]Еда: {data[6]}\n\nТерритория: {data[17]}🌍', keyboard=keyboard_menu(lvl_cas=data[7]))
        else:
            await message.answer(msg_error, keyboard=keyboard_menu(lvl_cas=data[7]))
            await message.answer(f'[id{message.from_id}|{userinfo[0].first_name}], твое королество:\n📖Игровой ID: {data[0]}\n\n💎Кристаллы: {data[2]}\n💰[{data[7]}]Золото: {data[3]}\n🌲[{data[9]}]Дерево: {data[4]}\n⛏[{data[8]}]Руда: {data[5]}\n🍖[{data[10]}]Еда: {data[6]}\n\nТерритория: {data[17]}🌍', keyboard=keyboard_menu(lvl_cas=data[7]))
            await bot.state_dispenser.set(message.peer_id, States.EMPTY)

@bot.on.private_message(text='🏇Конница', state=States.WAR_MENU)
async def war(message: Message):
    data = DB.get_row_users(message.from_id)
    await bot.state_dispenser.set(message.peer_id, States.WAR_RIDERS)
    await message.answer(f'🍖Еды: {data[6]}\n💰Золота: {data[3]}\n🏇Конницы: {data[20]}\n\nЦена найма одного воина: 400🍖 и 150💰\nСколько 🏇Конницы нужно нанять? Доступен ручной ввод', keyboard=keyboard_btn(menu='war_enemy', lvl_cas=data[7], enemy='🏇'))

@bot.on.private_message(text='👈Назад', state=States.WAR_RIDERS)
async def war(message: Message):
    data = DB.get_row_users(message.from_id)
    await bot.state_dispenser.set(message.peer_id, States.WAR_MENU)
    await message.answer(f'Побед: {data[16]}🎖\nТерритория: {data[17]}🌍\n\n⚔Пехоты: {data[18]}\n🏹Лучники: {data[19]}\n🏇Конницы: {data[20]}\n\n🔥Всего войск: {data[18] + data[19] + data[20]}', keyboard=keyboard_btn(menu='war', lvl_cas=data[7]))

@bot.on.private_message(text='📜Помощь', state=States.WAR_RIDERS)
async def war(message: Message):
    data = DB.get_row_users(message.from_id)
    await message.answer(msg_war_help, keyboard=keyboard_btn(menu='war_enemy', lvl_cas=data[7], enemy='🏇'))

@bot.on.private_message(state=States.WAR_RIDERS)
async def war(message: Message):
    data = DB.get_row_users(message.from_id)
    s = message.text.replace('🏇', '')
    if s.isdigit():
        num = int(s)
        if num * 400 <= data[6] and num * 150 <= data[3]:
            DB.set_cell('users', data[1], 'res_fod', data[6] - num * 400)
            DB.set_cell('users', data[1], 'res_gol', data[4] - num * 150)
            DB.set_cell('users', data[1], 'riders', data[20] + num)
            await message.answer('Войска наняты', keyboard=keyboard_btn(menu='war_enemy', lvl_cas=data[7], enemy='🏇'))
            dt = datetime.now()
            if dt.weekday() < 5 and not(dt.hour > 21 and dt.weekday() == 4) and not(dt.hour < 8 and not dt.weekday()):
                DB.set_cell('users', data[1], 'points', data[34] + num)
        else:
            await message.answer('Недостаточно еды или золота для найма', keyboard=keyboard_btn(menu='war_enemy', lvl_cas=data[7], enemy='🏇'))
    else:
        userinfo = await bot.api.users.get(message.from_id)
        if message.text == '🏕Домой':
            await bot.state_dispenser.set(message.peer_id, States.EMPTY)
            await message.answer(f'[id{message.from_id}|{userinfo[0].first_name}], твое королество:\n📖Игровой ID: {data[0]}\n\n💎Кристаллы: {data[2]}\n💰[{data[7]}]Золото: {data[3]}\n🌲[{data[9]}]Дерево: {data[4]}\n⛏[{data[8]}]Руда: {data[5]}\n🍖[{data[10]}]Еда: {data[6]}\n\nТерритория: {data[17]}🌍', keyboard=keyboard_menu(lvl_cas=data[7]))
        else:
            await message.answer(msg_error, keyboard=keyboard_menu(lvl_cas=data[7]))
            await message.answer(f'[id{message.from_id}|{userinfo[0].first_name}], твое королество:\n📖Игровой ID: {data[0]}\n\n💎Кристаллы: {data[2]}\n💰[{data[7]}]Золото: {data[3]}\n🌲[{data[9]}]Дерево: {data[4]}\n⛏[{data[8]}]Руда: {data[5]}\n🍖[{data[10]}]Еда: {data[6]}\n\nТерритория: {data[17]}🌍', keyboard=keyboard_menu(lvl_cas=data[7]))
            await bot.state_dispenser.set(message.peer_id, States.EMPTY)

@bot.on.private_message(text='🔎Разведка (1000💰)', state=States.WAR_MENU)
async def war(message: Message):
    data = DB.get_row_users(message.from_id)
    if data[3] >= 1000:
        DB.set_cell('users', data[1], 'res_gol', data[3] - 1000)
        u = [i for i in DB.get_all('users', ret='lst') if i[7] >= 8 and i[1] != data[1] and not i[23] and i[17] * 0.9 <= data[17] <= i[17] * 1.1]
        if not u:
            s = 'Завоевателей для аттаки нет...'
            await message.answer(s, keyboard=keyboard_btn(menu='war', lvl_cas=data[7]))
        else:
            defenser = random.choice(u)
            userinfo = await bot.api.users.get(defenser[1])
            enemies = defenser[18] + defenser[19] + defenser[20]
            if enemies < 100:
                e = 'Меньше 100'
            elif 100 <= enemies < 1000:
                e = 'Меньше 1000'
            elif 1000 <= enemies < 2000:
                e = 'Меньше 2000'
            elif 2000 <= enemies < 5000:
                e = 'Меньше 5000'
            elif 5000 <= enemies < 10000:
                e = 'Меньше 10000'
            elif 10000 <= enemies < 100000:
                e = 'Меньше 100000'
            else:
                e = 'Очень много'
            if defenser[3] >= data[3]:
                s = f"Разведчиками найден Завоеватель [id{defenser[1]}|{userinfo[0].first_name}]:\n\n⚔Войск: {e}\n💰Золота: больше чем у вас\n\nНе медлите! Иначе Завоеватель может скрыться."
            else:
                s = f"Разведчиками найден Завоеватель [id{defenser[1]}|{userinfo[0].first_name}]:\n\n⚔Войск: {e}\n💰Золота: меньше чем у вас\n\nНе медлите! Иначе Завоеватель может скрыться."
            await bot.state_dispenser.set(message.peer_id, States.WAR_ATTACK)
            await message.answer(s, keyboard=keyboard_btn(menu='war_attack', lvl_cas=data[7], war=defenser[1]))
    else:
        await message.answer('Недостаточно золота для разведки', keyboard=keyboard_btn(menu='war', lvl_cas=data[7]))

@bot.on.private_message(text='🔎Разведка (1000💰)', state=States.WAR_ATTACK)
async def war(message: Message):
    data = DB.get_row_users(message.from_id)
    if data[3] >= 1000:
        DB.set_cell('users', data[1], 'res_gol', data[3] - 1000)
        u = [i for i in DB.get_all('users', ret='lst') if i[7] >= 8 and i[1] != data[1] and not i[23] and i[17] * 0.9 <= data[17] <= i[17] * 1.1]
        if not u:
            s = 'Завоевателей для атаки нет...'
        else:
            defenser = random.choice(u)
            userinfo = await bot.api.users.get(defenser[1])
            enemies = defenser[18] + defenser[19] + defenser[20]
            if enemies < 100:
                e = 'Меньше 100'
            elif 100 <= enemies < 1000:
                e = 'Меньше 1000'
            elif 1000 <= enemies < 2000:
                e = 'Меньше 2000'
            elif 2000 <= enemies < 5000:
                e = 'Меньше 5000'
            elif 5000 <= enemies < 10000:
                e = 'Меньше 10000'
            elif 10000 <= enemies < 100000:
                e = 'Меньше 100000'
            else:
                e = 'Очень много'
            if defenser[3] >= data[3]:
                s = f"Разведчиками найден Завоеватель [id{defenser[1]}|{userinfo[0].first_name}]:\n\n⚔Войск: {e}\n💰Золота: больше чем у вас\n\nНе медлите! Иначе Завоеватель может скрыться."
            else:
                s = f"Разведчиками найден Завоеватель [id{defenser[1]}|{userinfo[0].first_name}]:\n\n⚔Войск: {e}\n💰Золота: меньше чем у вас\n\nНе медлите! Иначе Завоеватель может скрыться."
            await bot.state_dispenser.set(message.peer_id, States.WAR_ATTACK)
            await message.answer(s, keyboard=keyboard_btn(menu='war_attack', lvl_cas=data[7], war=defenser[1]))
    else:
        await message.answer('Недостаточно золота для разведки', keyboard=keyboard_btn(menu='war', lvl_cas=data[7]))

@bot.on.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=GroupTypes.MessageEvent)
async def war(event: GroupTypes.MessageEvent):
    defenser = DB.get_row_users(event.object.payload['cmd'])
    attacker = DB.get_row_users(event.object.user_id)

    DB.set_cell('users', attacker[1], 'shild', 0)

    kd = DB.get_row_event('attack_kd', attacker[1])
    if kd:
        kd = kd[0]
        await bot.api.messages.send(peer_id=attacker[1], message=f'Нападение возможно только через {time_formatter(kd[2])}', random_id=0, keyboard=keyboard_btn(menu='war', lvl_cas=attacker[7]))
        await bot.api.messages.send_message_event_answer(
            event_id=event.object.event_id,
            peer_id=event.object.peer_id,
            user_id=event.object.user_id,
            event_data=json.dumps({"type": "show_snackbar", "text": f"Ожидайте!"})
        )
    else:

        army_def = {'infantry': defenser[18], 'archers': defenser[19], 'riders': defenser[20]}
        army_att = {'infantry': attacker[18], 'archers': attacker[19], 'riders': attacker[20]}

        if army_def['infantry'] and not army_att['archers']:
            army_att['archers'] *= 0.5
        if army_def['archers'] and not army_att['riders']:
            army_att['riders'] *= 0.5
        if army_def['riders'] and not army_att['infantry']:
            army_att['infantry'] *= 0.5
    
        sumd, suma = army_def['infantry'] + army_def['archers'] + army_def['riders'], army_att['archers'] + army_att['riders'] + army_att['infantry']

        if sumd >= suma:
            s = f'Ваши потери:\n\n⚔Пехота: {int(suma // 3)}\n🏹Лучники: {int(suma // 3)}\n🏇Конница: {int(suma // 3)}\n\nПотери противника:\n\n⚔Пехота: {attacker[18]}\n🏹Лучники: {attacker[19]}\n🏇Конница: {attacker[20]}'
            s1 = f'Ваши потери:\n\n⚔Пехота: {attacker[18]}\n🏹Лучники: {attacker[19]}\n🏇Конница: {attacker[20]}\n\nПотери противника:\n\n⚔Пехота: {int(suma // 3)}\n🏹Лучники: {int(suma // 3)}\n🏇Конница: {int(suma // 3)}'
            DB.set_cell('users', attacker[1], 'shild', 0)
            DB.set_cell('users', attacker[1], 'infantry', 0)
            DB.set_cell('users', attacker[1], 'riders', 0)
            DB.set_cell('users', attacker[1], 'archers', 0)
            DB.set_cell('users', defenser[1], 'infantry', defenser[18] - int(suma // 3))
            DB.set_cell('users', defenser[1], 'riders', defenser[20] - int(suma // 3))
            DB.set_cell('users', defenser[1], 'archers', defenser[19] - int(suma // 3))
            DB.set_cell('users', defenser[1], 'wins', int(defenser[16] + 1))
            at = await bot.api.users.get(attacker[1])
            await bot.api.messages.send(peer_id=defenser[1], message=f'Завоеватель [id{attacker[1]}|{at[0].first_name}] напал на Вас. Ваши войска выстояли\n\n' + s, random_id=0)
            await bot.api.messages.send(peer_id=attacker[1], message=f'Нападение провалено\n\n' + s1, random_id=0, keyboard=keyboard_btn(menu='war', lvl_cas=attacker[7]))
            DB.new_event('attack_kd', attacker[1], 600)    
        else:
            a = f'\n\nПотери противника:\n\n⚔Пехота: {int(attacker[18] - sumd // 3)}\n🏹Лучники: {int(attacker[19] - sumd // 3)}\n🏇Конница: {int(attacker[20] - sumd // 3)}'
            s = f'Ваши потери:\n\n⚔Пехота: {defenser[18]}\n🏹Лучники: {defenser[19]}\n🏇Конница: {defenser[20]}\n💰Золото: {int(defenser[3] * 0.1)}\n⛏Руда: {int(defenser[5] * 0.1)}\n🌲Дерево: {int(defenser[4] * 0.1)}\n🍖Еда: {int(defenser[6] * 0.1)}\n🌍Территории: {int(defenser[17] * 0.1)}' + a
            s1 = f'Вы получили:\n\n💰Золото: {int(defenser[3] * 0.1)}\n⛏Руда: {int(defenser[5] * 0.1)}\n🌲Дерево: {int(defenser[4] * 0.1)}\n🍖Еда: {int(defenser[6] * 0.1)}\n🌍Территории: {int(defenser[17] * 0.1)}\n\nВаши потери:\n\n⚔Пехота: {int(attacker[18] - sumd // 3)}\n🏹Лучники: {int(attacker[19] - sumd // 3)}\n🏇Конница: {int(attacker[20] - sumd // 3)}'
            DB.set_cell('users', attacker[1], 'infantry', int(attacker[18] - sumd // 3))
            DB.set_cell('users', attacker[1], 'riders', int(attacker[20] - sumd // 3))
            DB.set_cell('users', attacker[1], 'archers', int(attacker[19] - sumd // 3))
            DB.set_cell('users', attacker[1], 'wins', int(attacker[16] + 1))
            DB.set_cell('users', attacker[1], 'territory', int(attacker[17] + defenser[17] * 0.1))
            DB.set_cell('users', defenser[1], 'territory', int(defenser[17] * 0.9))
            DB.set_cell('users', attacker[1], 'res_gol', int(attacker[3] + defenser[3] * 0.1))
            DB.set_cell('users', defenser[1], 'res_gol', int(defenser[3] * 0.9))
            DB.set_cell('users', attacker[1], 'res_wod', int(attacker[4] + defenser[4] * 0.1))
            DB.set_cell('users', defenser[1], 'res_wod', int(defenser[4] * 0.9))
            DB.set_cell('users', attacker[1], 'res_ore', int(attacker[5] + defenser[5] * 0.1))
            DB.set_cell('users', defenser[1], 'res_ore', int(defenser[5] * 0.9))
            DB.set_cell('users', attacker[1], 'res_fod', int(attacker[6] + defenser[6] * 0.1))
            DB.set_cell('users', defenser[1], 'res_fod', int(defenser[6] * 0.9))
            DB.set_cell('users', defenser[1], 'infantry', 0)
            DB.set_cell('users', defenser[1], 'riders', 0)
            DB.set_cell('users', defenser[1], 'archers', 0)
            DB.set_cell('users', defenser[1], 'shild', 3600)
            dt = datetime.now()
            if dt.weekday() < 5 and not(dt.hour > 21 and dt.weekday() == 4) and not(dt.hour < 8 and not dt.weekday()):
                num = defenser[18] + defenser[19] + defenser[20]
                DB.set_cell('users', attacker[1], 'points', attacker[34] + num)
            at = await bot.api.users.get(attacker[1])
            await bot.api.messages.send(peer_id=defenser[1], message=f'Завоеватель [id{attacker[1]}|{at[0].first_name}] напал на Вас. Ваши войска не выстояли\n\n' + s, random_id=0)
            await bot.api.messages.send(peer_id=attacker[1], message=f'Нападение успешно!\n\n' + s1, random_id=0, keyboard=keyboard_btn(menu='war', lvl_cas=attacker[7]))
            DB.new_event('attack_kd', attacker[1], 600)  

        await bot.api.messages.send_message_event_answer(
            event_id=event.object.event_id,
            peer_id=event.object.peer_id,
            user_id=event.object.user_id,
            event_data=json.dumps({"type": "show_snackbar", "text": f"Завоеватель атакован!"})
        )

@bot.on.private_message(text='👈Назад', state=States.WAR_ATTACK)
async def war(message: Message):
    userinfo = await bot.api.users.get(message.from_id)
    data = DB.get_row_users(message.from_id)
    await bot.state_dispenser.set(message.peer_id, States.WAR_MENU)
    await message.answer(f'Побед: {data[16]}🎖\nТерритория: {data[17]}🌍\n\n⚔Пехоты: {data[18]}\n🏹Лучники: {data[19]}\n🏇Конницы: {data[20]}\n\n🔥Всего войск: {data[18] + data[19] + data[20]}', keyboard=keyboard_btn(menu='war', lvl_cas=data[7]))

@bot.on.private_message(text='📜Помощь', state=States.WAR_ATTACK)
async def war(message: Message):
    data = DB.get_row_users(message.from_id)
    await message.answer(msg_war_help, keyboard=keyboard_btn(menu='war', lvl_cas=data[7]))

@bot.on.private_message(text='👈Назад', state=States.WAR_MENU)
async def war(message: Message):
    userinfo = await bot.api.users.get(message.from_id)
    data = DB.get_row_users(message.from_id)
    await bot.state_dispenser.set(message.peer_id, States.EMPTY)
    await message.answer(f'[id{message.from_id}|{userinfo[0].first_name}], твое королество:\n📖Игровой ID: {data[0]}\n\n💎Кристаллы: {data[2]}\n💰[{data[7]}]Золото: {data[3]}\n🌲[{data[9]}]Дерево: {data[4]}\n⛏[{data[8]}]Руда: {data[5]}\n🍖[{data[10]}]Еда: {data[6]}\n\nТерритория: {data[17]}🌍', keyboard=keyboard_menu(lvl_cas=data[7]))

@bot.on.private_message(text='📜Помощь', state=States.WAR_MENU)
async def war(message: Message):
    data = DB.get_row_users(message.from_id)
    await message.answer(msg_war_help, keyboard=keyboard_btn(menu='war', lvl_cas=data[7]))

@bot.on.private_message(text='🥇Рейтинг')
async def top(message: Message):
    data = DB.get_row_users(message.from_id)
    if data[7] < 8:
        await message.answer(msg_top_den, keyboard=keyboard_menu(lvl_cas=data[7]))
    else:
        top = sorted(DB.get_all('users', ret='lst'), key=lambda x: -x[17])
        s = ''
        for i, j in enumerate(top[:10]):
            userinfo = await bot.api.users.get(j[1])
            if j[21]:
                union = DB.get_row('unions', j[21])[1]
                s += f'{i + 1}. [{union}] [id{j[1]}|{userinfo[0].first_name}] {j[17]}🌍\n'
            else:
                s += f'{i + 1}. [id{j[1]}|{userinfo[0].first_name}] {j[17]}🌍\n'
        await message.answer(s, keyboard=keyboard_menu(lvl_cas=data[7]))

@bot.on.private_message(ifin=['📖Инфо', '🏕Домой'])
async def info(message: Message):
    await bot.state_dispenser.set(message.peer_id, States.EMPTY)
    userinfo = await bot.api.users.get(message.from_id)
    data = DB.get_row_users(message.from_id)
    await message.answer(f'[id{message.from_id}|{userinfo[0].first_name}], твое королество:\n📖Игровой ID: {data[0]}\n\n💎Кристаллы: {data[2]}\n💰[{data[7]}]Золото: {data[3]}\n🌲[{data[9]}]Дерево: {data[4]}\n⛏[{data[8]}]Руда: {data[5]}\n🍖[{data[10]}]Еда: {data[6]}\n\nТерритория: {data[17]}🌍', keyboard=keyboard_menu(lvl_cas=data[7]))

@bot.on.private_message(text='📜Помощь')
async def start_1(message: Message):
    data = DB.get_row_users(message.from_id)
    await message.answer(msg_help, keyboard=keyboard_menu(lvl_cas=data[7]))

@bot.on.private_message()
async def start_1(message: Message):
    await bot.state_dispenser.set(message.peer_id, States.EMPTY)
    data = DB.get_row_users(message.from_id)
    if data[12] == 'admin':
        try:
            s = message.text.split()
            if s[0] == '!установить':
                DB.set_cell('users', s[1], s[2], s[3])
                await message.answer('Установлено!', keyboard=keyboard_menu(lvl_cas=data[7]))
        except:
            await message.answer('Ошибка в команде', keyboard=keyboard_menu(lvl_cas=data[7]))
    else:
        userinfo = await bot.api.users.get(message.from_id)
        await message.answer(msg_error, keyboard=keyboard_menu(lvl_cas=data[7]))
        await message.answer(f'[id{message.from_id}|{userinfo[0].first_name}], твое королество:\n📖Игровой ID: {data[0]}\n\n💎Кристаллы: {data[2]}\n💰[{data[7]}]Золото: {data[3]}\n🌲[{data[9]}]Дерево: {data[4]}\n⛏[{data[8]}]Руда: {data[5]}\n🍖[{data[10]}]Еда: {data[6]}\n\nТерритория: {data[17]}🌍', keyboard=keyboard_menu(lvl_cas=data[7]))

if __name__ == '__main__':
    bot.run_forever()
