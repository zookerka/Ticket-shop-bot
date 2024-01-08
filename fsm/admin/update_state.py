from aiogram.dispatcher.filters.state import State, StatesGroup


class UpdateFSM(StatesGroup):
    name_event = State()
    data_val = State()        
    