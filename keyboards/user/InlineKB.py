from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_in_keyboard ():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Buy ticket', callback_data='buy')],
        [InlineKeyboardButton(text='Places', callback_data='place')]
    ])
    return ikb


async def ikb_change_event():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='name',callback_data='name'),
        InlineKeyboardButton(text='event price',callback_data='cost')],
        [InlineKeyboardButton(text='time', callback_data='time'),
        InlineKeyboardButton(text='weekday', callback_data='weekday'),
        InlineKeyboardButton(text='additional_info', callback_data='add_info')],
        [InlineKeyboardButton(text='places', callback_data='places'),
        InlineKeyboardButton(text='rows', callback_data='rows')],


    ])
    return ikb