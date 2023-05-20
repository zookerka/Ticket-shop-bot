from aiogram import types
from keyboards.user.ReplyKB import *
from config import ADMINS
from models.my_sqlltie3 import *
from .filters_kb import *
HELP = """
Here the comands, whick you can use:
/start
/help
/events
/event
/buy

"""
# async def on_startup(_) -> None:
#     await db_connect()
#     print('Подключение к Базе Данных прошло успешно!')




async def cmd_start(message: types.Message):
    if message.from_user.id != ADMINS[0]:
        keyboard = await user_menu()
        await message.bot.send_message(chat_id=message.chat.id,text='Welocome to Ticket Sale bot!\nHere you can to buy a ticket for an event', reply_markup=keyboard)
    else:
        keyboard = await admin_main_menu()
        await message.answer(text='Welcome to Admin panel!', reply_markup=keyboard)

async def cmd_help(message: types.Message):
    menu = await user_menu()
    await message.answer(text=HELP, reply_markup=menu)

async def cmd_event(message: types.Message):
    await start_TextState(message)
async def cmd_buy(message:types.Message):
    await start_BuyTicket(message)

async def cmd_events(message: types.Message):
    await Events_handler(message)
    

