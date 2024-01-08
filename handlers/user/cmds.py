from aiogram import types
from keyboards.user.ReplyKB import *
from handlers.user.message_handlers import *
from loader import dp
from filter.is_user import IsUser


HELP = """
Here the comands, whick you can use:
/start
/help
/events
/eventinfo
/buy

"""

# help 
@dp.message_handler(IsUser(), commands='help')
async def cmd_help(message: types.Message):
    menu = await user_menu()
    await message.answer(text=HELP, reply_markup=menu)


# # check all events
# @dp.message_handler(IsUser(), commands='events')
# async def cmd_event(message: types.Message):
#     await start_TextState(message)


# # buy ticket 
# @dp.message_handler(IsUser(), commands='buy')
# async def cmd_buy(message:types.Message):
#     await start_BuyTicket(message)


# info about event 
@dp.message_handler(IsUser(),commands='eventinfo')
async def cmd_events(message: types.Message):
    await Events_handler(message)
    

