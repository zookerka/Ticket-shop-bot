from aiogram import Bot, Dispatcher
from config import BOT_API_TOKEN
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
bot = Bot(BOT_API_TOKEN)
dp = Dispatcher(bot=bot, storage=storage)



