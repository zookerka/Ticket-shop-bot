from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_in_keyboard ():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Buy ticket', callback_data='buy')],
        [InlineKeyboardButton(text='Places', callback_data='place')]
    ])
    return ikb


