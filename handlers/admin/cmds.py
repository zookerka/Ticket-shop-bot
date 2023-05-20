from aiogram import types
from keyboards.user.ReplyKB import admin_main_menu
from .def_filters import *

HELP = """
Here the comands, whick you can use:
/help
/events
/add_event
"""

async def cmd_help_admin(message: types.Message):
    await message.answer(text=HELP)

async def cmd_add_event_admin(message:types.Message):
    await start_button_clicked(message)

async def cmd_events_admin(message:types.Message):
    await get_data(message)
    
    