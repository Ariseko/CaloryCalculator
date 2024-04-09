from aiogram import types, F, Router
from aiogram.filters import CommandStart, Command
from aiogram import Bot
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import datetime

from config import TOKEN
from app.keyboards import *
from app.database import Database

import re

router = Router()
bot = Bot(token=TOKEN)
db = Database('database.db')


class Calculator(StatesGroup):
    gender = State()
    height = State()
    weight = State()
    age = State()
    activity = State()


class MessagesAdding(StatesGroup):
    gettext = State()


class Broadcast(StatesGroup):
    get_type = State()
    get_photo = State()
    get_video = State()
    get_text = State()
    waiting_photo = State()
    waiting_video = State()

igor_id = 337652760
photo_ids = []


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer_video_note('DQACAgIAAxkBAAIB_WYS8JntYAUKNBFaM7HqkyceYg7aAAKnSwACLgSZSAUfLxC-lc59NAQ')
    await message.answer('Привет, хочешь расчитать каллории?', reply_markup=first_message_kb)


@router.message(F.video_note)
async def get_id_of_video_note(message: types.Message):
    await message.answer(f'{message.video_note}')


@router.callback_query(F.data == 'answer_NO_for_fat_question')
async def first_answer_no(callback_query: types.CallbackQuery):
    await callback_query.answer('')
    await callback_query.message.edit_text('Очень жаль(\n\n'
                                           'Но если передумаете, используйте команду /start')


@router.callback_query(F.data == 'answer_YES_for_fat_question')
async def first_answer_yes(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer('')
    await callback_query.message.edit_text('👱‍♂️ Кто ты? 👱‍♀️',
                                           reply_markup=gender_kb)
    await state.set_state(Calculator.gender)


@router.callback_query(Calculator.gender)
async def get_gender(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer('')
    if callback_query.data == 'Male':
        await state.update_data(gender='male')
    elif callback_query.data == 'Female':
        await state.update_data(gender='female')

    await bot.send_message(callback_query.from_user.id, '<b>Какой ваш рост в сантиметрах?</b> 📏 \n'
                                                        '<i>Десятые части пишите через запятую.</i>\n'
                                                        '<i>Пример: 170,5</i>', parse_mode='html')
    await state.set_state(Calculator.height)


@router.message(Calculator.height)
async def get_activity(message: types.Message, state: FSMContext):
    await state.update_data(height=message.text)
    await state.set_state(Calculator.weight)
    await message.answer('<b>Напишите свой актуальный вес в кг ⚖️</b>\n'
                         '<i>Десятые части пишите через запятую.</i> \n'
                         '<i>Например: 68,9</i>', parse_mode='html')
    print(message.entities)


@router.message(Calculator.weight)
async def get_age(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await state.set_state(Calculator.age)
    await message.answer('<b>Сколько вам лет?</b> 🗓 ', parse_mode='html')


@router.message(Calculator.age)
async def get_height(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Calculator.activity)
    await message.answer('⛹️ <b>Сколько вы двигаетесь?</b> ⛹️‍♀️\n\n'
                         '1️⃣ <b>Активности почти нет</b>: <i>до 8к шагов в день</i>. 🎮\n\n'
                         '<b>2️⃣Умеренная активность: </b><i>8-10к шагов каждый день или 7-8к шагов + 2-3 легкие тренировки по часу. 🎳</i>\n\n'
                         '<b>3️⃣Оптимальная активность: </b><i>8-10к шагов каждый день + 3 тренировки минимум по часу. 🏌️‍♂️</i>\n\n'
                         '<b>4️⃣Высокая активность: </b><i>10-15к шагов каждый день плюс 3-4 тренировки по полтора-два часа. 🏄‍♂️</i>\n\n'
                         '<b>5️⃣Экстремальная активность:</b> <i>12-20к шагов каждый день плюс 4-6 тренировок по полтора-два часа.</i> 🧗\n\n',
                         reply_markup=activity_kb, parse_mode='html')


@router.callback_query(Calculator.activity)
async def get_weight(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(activity=callback_query.data)
    data = await state.get_data()

    gender = data['gender']
    age = int(data['age'])
    height = float(str(data['height']).replace(',', '.').replace(' ', ''))
    weight = float(str(data['weight']).replace(',', '.').replace(' ', ''))
    activity = float(data['activity'])

    baseMetabolismFirst = (9.99 * weight) + (6.25 * height) - (4.92 * age)

    if gender == "male":
        baseMetabolismMale = baseMetabolismFirst + 5
        calloryMale = baseMetabolismMale * activity

        await bot.send_message(callback_query.from_user.id,
                               f'▪️<b>Ваш базовый метаболизм равен:</b>\n⬇️<i>Это калории, которые сжигаются, когда вы находитесь в покое, и энергия тратится на обеспечение процессов дыхания, кровообращения, поддержание температуры тела и т.д.</i> ⬇️\n\n<b>{round(baseMetabolismMale)}\n\n\n</b>'
                               f'▪️Ваша норма калорий для поддержания веса (вы не худеете и не набираете вес) с текущей физической активностью равна:\n\n<b>{round(calloryMale)}</b>\n\n\n'
                               f'▪️ <b>Рекомендованный дефицит калорий:</b>\n'
                               f'10% - {round(calloryMale * 0.9)} ККАЛ\n'
                               f'15% - {round(calloryMale * 0.85)} ККАЛ\n\n'
                               f'▪️<b>Экстремальное снижение веса:</b>\n'
                               f'20% - {round(calloryMale * 0.8)} ККАЛ\n'
                               f'25% - {round(calloryMale * 0.75)} ККАЛ\n\n'
                               f'🔻Оптимальная скорость снижения веса: до 1% от собственного веса в неделю',
                               parse_mode='html')

    elif gender == "female":
        baseMetabolismFemale = baseMetabolismFirst - 161
        calloryFemale = baseMetabolismFemale * activity
        await bot.send_message(callback_query.from_user.id,
                               f'▪️<b>Ваш базовый метаболизм равен:</b>\n⬇️<i>Это калории, которые сжигаются, когда вы находитесь в покое, и энергия тратится на обеспечение процессов дыхания, кровообращения, поддержание температуры тела и т.д.</i> ⬇️\n\n<b>{round(baseMetabolismFemale)}\n\n\n</b>'
                               f'️Ваша норма калорий для поддержания веса (вы не худеете и не набираете вес) с текущей физической активностью равна:\n\n<b>{round(calloryFemale)}</b>\n\n\n'
                               f'▪️ <b>Рекомендованный дефицит калорий:</b>\n'
                               f'10% - {round(calloryFemale * 0.9)} ККАЛ\n'
                               f'15% - {round(calloryFemale * 0.85)} ККАЛ\n\n'
                               f'▪️<b>Экстремальное снижение веса:</b>\n'
                               f'20% - {round(calloryFemale * 0.8)} ККАЛ\n'
                               f'25% - {round(calloryFemale * 0.75)} ККАЛ\n\n'
                               f'🔻Оптимальная скорость снижения веса: до 1% от собственного веса в неделю',
                               parse_mode='html')

    await bot.send_message(callback_query.from_user.id,
                           f'Если хотите еще раз посчитать каллории, используйте команду /start')

    message_entitie = db.get_messages()
    input_string = message_entitie[1]
    input_string = input_string[1:-1]
    entity_list = []

    regex = r"MessageEntity\(type='(\w+)', offset=(\d+), length=(\d+), url=(\w+), user=(\w+), language=(\w+), custom_emoji_id=(\w+)\)"

    matches = re.findall(regex, input_string)
    for match in matches:
        entity_list.append(
            types.MessageEntity(
                type=f'{match[0]}',
                offset=match[1],
                length=match[2],
                url=f'{match[3]}',
            )
        )

    await bot.send_message(callback_query.from_user.id, message_entitie[0], entities=entity_list)

    if not db.user_exists(callback_query.from_user.id):
        db.add_user(callback_query.from_user.id, callback_query.from_user.username, datetime.today())
        await bot.send_message(337652760, f'Пользователь @{callback_query.from_user.username} посчитал свои каллории\n\n'
                                           f'<b>Пол</b>: {gender}\n'
                                           f'<b>Возраст</b>: {age}\n'
                                           f'<b>Вес</b>: {weight}\n'
                                           f'<b>Рост</b>: {height}\n'
                                           f'<b>Активность</b>: {activity}',parse_mode='html')

    await state.clear()


@router.message(Command('edit'))
async def edit_last_message(message: types.Message, state: FSMContext):
    await message.answer('Введи текст')
    await state.set_state(MessagesAdding.gettext)


@router.message(MessagesAdding.gettext)
async def cmd_sad(message: types.Message, state: FSMContext):
    await state.clear()
    text = message.text
    entities = message.entities
    entities_str = str(entities)
    db.update_message(text, entities_str)


@router.message(Command('sendAll'))
async def send_all(message: types.Message, state: FSMContext):
    await message.answer("Напиши текст для рассылки")
    await state.set_state(Broadcast.get_text)


@router.message(Broadcast.get_text)
async def broadcast(message: types.Message, state: FSMContext):
    text = message.text
    entities = message.entities
    entities_str = str(entities)
    db.update_message_for_broadcast(text, entities_str)

    await message.answer('Нужно добавить фото?', reply_markup=broadcast_kb)
    await state.set_state(Broadcast.get_type)


@router.callback_query(Broadcast.get_type)
async def broadcast_type(callbackquery: types.CallbackQuery, state: FSMContext):
    await callbackquery.answer()
    if callbackquery.data == 'video':
        await bot.send_message(callbackquery.from_user.id, 'Отправь видео')
        await state.set_state(Broadcast.get_video)
    elif callbackquery.data == 'photo':
        await bot.send_message(callbackquery.from_user.id, 'Отправь фото')
        await state.set_state(Broadcast.get_photo)
    elif callbackquery.data == 'nothing':
        await callbackquery.message.answer('Ok, начинаю рассылку')

        message_entitie_for_broadcast = db.get_messages_for_broadcast()
        input_string_for_broadcast = message_entitie_for_broadcast[1]
        input_string_for_broadcast = input_string_for_broadcast[1:-1]
        entity_list = []

        regex = r"MessageEntity\(type='(\w+)', offset=(\d+), length=(\d+), url=(\w+), user=(\w+), language=(\w+), custom_emoji_id=(\w+)\)"

        matches = re.findall(regex, input_string_for_broadcast)
        for match in matches:
            entity_list.append(
                types.MessageEntity(
                    type=f'{match[0]}',
                    offset=match[1],
                    length=match[2],
                    url=f'{match[3]}',
                )
            )

        all_users = db.get_users()
        for user in all_users:
            await bot.send_message(user[0], message_entitie_for_broadcast[0], entities=entity_list)

        await state.clear()


@router.message(Broadcast.get_photo, F.photo)
async def get_photo(message: types.Message, state: FSMContext):
    photo_data = message.photo[-1]
    await message.answer('Начало рассылки')

    message_entitie_for_broadcast = db.get_messages_for_broadcast()
    input_string_for_broadcast = message_entitie_for_broadcast[1]
    input_string_for_broadcast = input_string_for_broadcast[1:-1]
    entity_list = []

    regex = r"MessageEntity\(type='(\w+)', offset=(\d+), length=(\d+), url=(\w+), user=(\w+), language=(\w+), custom_emoji_id=(\w+)\)"

    matches = re.findall(regex, input_string_for_broadcast)
    for match in matches:
        entity_list.append(
            types.MessageEntity(
                type=f'{match[0]}',
                offset=match[1],
                length=match[2],
                url=f'{match[3]}',
            )
        )

    all_users = db.get_users()
    for user in all_users:
        await bot.send_photo(chat_id=user[0],
                             photo=photo_data.file_id,
                             caption=message_entitie_for_broadcast[0],
                             caption_entities=entity_list)

    await message.answer('Рассылка окончена')
    await state.clear()


