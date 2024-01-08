from aiogram import types
from keyboards.user.ReplyKB import admin_main_menu
from handlers.admin.message_handlers_admin import *
from loader import dp
from filter.is_admin import IsAdmin

HELP = """
Here the comands, whick you can use:
/help
/events
/add_event
"""

# help
@dp.message_handler(IsAdmin(), commands=['help'])
async def cmd_help_admin(message: types.Message):
    await message.answer(text=HELP)

# add event
@dp.message_handler(IsAdmin(), commands=['addevent'])
async def cmd_add_event_admin(message:types.Message):
    await start_button_clicked(message)

# check all events
@dp.message_handler(IsAdmin(), commands=['events'])
async def cmd_check_events_admin(message:types.Message):
    await get_data(message)
    
    
# return to admin panel
@dp.message_handler(IsAdmin(), commands=['return'])
async def cmd_return_to_admin_panel (message:types.Message):
    menu = await admin_main_menu()
    await message.answer("You've returned to admin panel", reply_markup=menu)
