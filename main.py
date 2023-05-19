from aiogram import executor
from handlers.user.cmds import *
from loader import dp
from handlers.user.filters_kb import *
from aiogram.dispatcher.filters import Text
from models.my_sqlltie3 import db_connect
from handlers.admin.def_filters import *
from filter.is_admin import IsAdmin

async def on_startup(_):
    await db_connect()
    print("Подключение прошло успешно")

# User
dp.register_message_handler(cmd_start, commands='start')
dp.register_message_handler(cmd_event, commands='event')
dp.register_message_handler(cmd_events, commands='events')
dp.register_message_handler(cmd_buy, commands='buy')
dp.register_message_handler(cmd_help, commands='help')

dp.register_message_handler(Schedule_handler, Text('Schedule for today'))
dp.register_message_handler(main_menu, Text('Back to main menu'))
dp.register_message_handler(Events_handler, Text('Events'))


fsm_text = TextState()
dp.register_message_handler(fsm_text.button_handler,commands=['start'] ,state='*')
dp.register_message_handler(fsm_text.print_name_event, state=TextState.waiting_for_text)


dp.register_message_handler(start_TextState, Text('Event'))

fsm_buy = BuyTicket()
dp.register_message_handler(fsm_buy.cancel_buy,commands=['cancel'],state='*')
dp.register_message_handler(fsm_buy.start_geting, commands=['start'], state='*')
dp.register_message_handler(fsm_buy.data_name_event, state=BuyTicket.event_name)

dp.register_message_handler(start_BuyTicket, Text('Buy a ticket'))


# Admin



dp.register_message_handler(start_button_clicked, IsAdmin() ,Text('Add new event'))

dp.register_message_handler(get_data, IsAdmin(),Text('Check all events'))
dp.register_message_handler(select_changes,IsAdmin(), Text('Change event'))




fsm = BookingFSM()
dp.register_message_handler(fsm.start, commands=['start'], state='*')
dp.register_message_handler(fsm.cancel_booking, commands=['cancel'],state='*')
dp.register_message_handler(fsm.process_name_event, state=BookingFSM.get_name_event)
dp.register_message_handler(fsm.process_cost_ticket, state=BookingFSM.get_cost_ticket)
dp.register_message_handler(fsm.process_weekday_event, state=BookingFSM.get_weekday_event)
dp.register_message_handler(fsm.process_time_event, state=BookingFSM.get_time_event)
dp.register_message_handler(fsm.process_add_info_event, state=BookingFSM.get_add_info_event)
dp.register_message_handler(fsm.process_places_event, state=BookingFSM.get_places_event)
dp.register_message_handler(fsm.process_rows_event, state=BookingFSM.get_rows_event)




 

fsm_update = UpdateFSM()
dp.register_message_handler(fsm_update.start_changes, commands=['start'], state='*')
dp.register_message_handler(fsm_update.cancel_changing, commands=['cancel'],state='*')
dp.register_message_handler(fsm_update.check_name, state=UpdateFSM.name_event)
dp.register_message_handler(fsm_update.change_data_value, state=UpdateFSM.data_val)
    
dp.register_message_handler(changes_name_event, Text('name'))
dp.register_message_handler(changes_cost_event, Text('cost_event'))
dp.register_message_handler(changes_time_event, Text('time'))
dp.register_message_handler(changes_weekend_event, Text('weekday'))
dp.register_message_handler(changes_add_info_event, Text('add_info'))
dp.register_message_handler(changes_places_event, Text('places'))
dp.register_message_handler(changes_rows_event, Text('rows'))



fsm_del = DeleteEventFSM()
dp.register_message_handler(fsm_del.cancel_deleting,commands=['cancel'],state='*')
dp.register_message_handler(fsm_del.name_deletable_event,commands=['start'], state='*')
dp.register_message_handler(fsm_del.delete_event, state=DeleteEventFSM.name_del_event)

dp.register_message_handler(confidance_del, IsAdmin(),Text('Delete event'))





if __name__ == '__main__':

    executor.start_polling(dp, skip_updates=False,
                           on_startup=on_startup)


