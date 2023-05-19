from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



async def user_menu ():
    kb = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[
        [KeyboardButton(text='Schedule for today'),
        KeyboardButton(text='Buy a ticket')],
        [KeyboardButton(text='Events'),
         KeyboardButton(text='Event')]

    ])

    return kb

async def keyboard_main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[
        [KeyboardButton(text='Back to main menu')]
    ])
    return kb

async def keyboard_cancel():
    kb = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[
        [KeyboardButton(text='/cancel')]
    ])
    return kb

async def admin_main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text='Add new event'),
         KeyboardButton(text='Change event')],
        [KeyboardButton(text='Delete event'),
         KeyboardButton(text='Check all events')]
    ])
    return kb


async def kb_change_event():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text='name'),
        KeyboardButton(text='cost_event')],
        [KeyboardButton(text='time'),
        KeyboardButton(text='weekday'),
        KeyboardButton(text='additional_info')],
        [KeyboardButton(text='places'),
        KeyboardButton(text='rows')],

    ])
    return kb


