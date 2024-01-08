from aiogram.dispatcher.filters.state import State, StatesGroup


class BookingFSM(StatesGroup):
    get_name_event = State()
    get_cost_ticket = State()
    get_weekday_event = State()
    get_time_event = State()
    get_add_info_event = State()
    get_places_event = State()
    get_rows_event = State()
    cancel_state = State()