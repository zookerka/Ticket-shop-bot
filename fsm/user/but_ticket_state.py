from aiogram.dispatcher.filters.state import State, StatesGroup

class BuyTicket(StatesGroup):
    event_name = State()