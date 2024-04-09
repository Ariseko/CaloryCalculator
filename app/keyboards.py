from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

first_message_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да!', callback_data='answer_YES_for_fat_question'),
     InlineKeyboardButton(text='Нет(', callback_data='answer_NO_for_fat_question')],
])

gender_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Мужчина', callback_data='Male'),
     InlineKeyboardButton(text='Девушка', callback_data='Female')],
])

activity_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='1', callback_data='1.200'),
     InlineKeyboardButton(text='2', callback_data='1.375')],
    [InlineKeyboardButton(text='3', callback_data='1.550'),
     InlineKeyboardButton(text='4', callback_data='1.725')],
    [InlineKeyboardButton(text='5', callback_data='1.900')],
])

broadcast_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да', callback_data='photo')],
    [InlineKeyboardButton(text='Нет', callback_data='nothing')],

])

