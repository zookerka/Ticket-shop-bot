from aiogram import types
from keyboards.user.ReplyKB import get_keyboard


HELP = """
Here the comands, whick you can use:
/start
/help
/events
/event
/buy

"""

async def cmd_help(message: types.Message):
    await message.answer(text=HELP)

async def cmd_add_event(message:types.Message):
    pass