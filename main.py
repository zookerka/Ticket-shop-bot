from aiogram import executor
from loader import dp
from models.my_sqlltie3 import db_connect
from config import ADMINS
from aiogram import types
import handlers
from keyboards.user.ReplyKB import user_menu, admin_main_menu

async def on_startup(_):
    await db_connect()
    print("Successful connection")

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    if message.from_user.id != ADMINS[0]:
        keyboard = await user_menu()
        await message.bot.send_message(chat_id=message.chat.id,text='Welocome to Ticket Sale bot!\nHere you can to buy a ticket for an event', reply_markup=keyboard)
    else:
        keyboard = await admin_main_menu()
        await message.bot.send_message(chat_id=message.chat.id, text='Welcome to Admin panel!', reply_markup=keyboard)


if __name__ == '__main__':

    executor.start_polling(dp, skip_updates=False,
                           on_startup=on_startup)



