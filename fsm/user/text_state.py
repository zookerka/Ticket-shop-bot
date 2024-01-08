from aiogram.dispatcher.filters.state import State, StatesGroup

class GetEventState(StatesGroup):
    waiting_for_text = State()