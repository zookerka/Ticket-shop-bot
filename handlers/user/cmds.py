from aiogram import types
from keyboards.user.ReplyKB import *
from config import ADMINS
from models.my_sqlltie3 import *

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
    await message.answer(text=HELP)

async def cmd_event(message: types.Message):
    pass
async def cmd_buy():
    pass        

async def cmd_events(message: types.Message):
    menu = user_menu()
    
    rows = await db_check_all()
    response = "All events:\n"
    if rows is not None:
        for row in rows:
            response += f"{row[0]}, Cost: {row[1]}, Weekend: {row[2]}, Time: {row[3]}, Additional info: {row[4]}, Places: {row[5]}, Rows: {row[6]}\n ---------------------------------------------------------------------------------------- \n"
        await message.answer(response, reply_markup= await menu)
    else:
        await message.answer("No rows found.", reply_markup= await menu)
