from aiogram import types
from keyboards.user.ReplyKB import *
from keyboards.user.InlineKB import *
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from models.my_sqlltie3 import *
from loader import dp,bot
from filter.is_admin import IsAdmin
from aiogram.dispatcher.filters import Text
from fsm.admin.booking_state import BookingFSM
from fsm.admin.delete_event_state import  DeleteEventFSM
from fsm.admin.update_state import UpdateFSM






    # Go to user menu 
@dp.message_handler(IsAdmin(), Text("User menu"))
async def go_to_user_menu(message:types.Message):
    menu = await user_menu()
    await message.answer("You've entered in User panel. \n To return to Admin panel, just type:  /return ", reply_markup=menu)


    # Check all events <3

@dp.message_handler(IsAdmin(),Text('Check all events'))
async def get_data(message: types.Message):
    menu = admin_main_menu()
    
    rows = await db_check_all() #db rows of events
    response = "All events:\n"
    if rows is not None:
        #loop for rows
        for row in rows:
            # response  add event 
            response += f"{row[0]}, Cost: {row[1]}, Weekend: {row[2]}, Time: {row[3]}, Additional info: {row[4]}, Places: {row[5]}, Rows: {row[6]}\n ---------------------------------------------------------------------------------------- \n"
        await message.answer(response, reply_markup= await menu)
    else:
        await message.answer("No rows found.", reply_markup= await menu)





    # Create new event FSM
        
# cancel function
@dp.message_handler(commands=['cancel'],state='*')
async def cancel_booking(message: Message, state: FSMContext):
    await message.answer("You have canceled the creating")
    await state.finish()
    # add new event
@dp.message_handler(IsAdmin() ,Text('Add new event'))
async def start_button_clicked(message: types.Message):
    await message.answer("You started the process of creating event. Enter name of event. \n Type /cancel to cancel the creating")
    await BookingFSM.get_name_event.set()


    # cost
@dp.message_handler(state=BookingFSM.get_name_event)
async def process_name_event(message: Message, state: FSMContext):
    async with state.proxy() as data:
        # record data in fsm
        data['name_event'] = message.text
    await message.answer("Enter the cost of ticket")
    await BookingFSM.get_cost_ticket.set()

    # weekend
@dp.message_handler(state=BookingFSM.get_cost_ticket)
async def process_cost_ticket(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['cost_ticket'] = message.text
    await message.answer("Enter the weekend of event")
    await BookingFSM.get_weekday_event.set()
    # time
@dp.message_handler(state=BookingFSM.get_weekday_event)
async def process_weekday_event(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['weekday_event'] = message.text
    await message.answer("Enter the time of event")
    await BookingFSM.get_time_event.set()

    # add info
@dp.message_handler(state=BookingFSM.get_time_event)
async def process_time_event(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['time_event'] = message.text
    await message.answer("Enter an additional info of event")
    await BookingFSM.get_add_info_event.set()

    # places
@dp.message_handler(state=BookingFSM.get_add_info_event)
async def process_add_info_event(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['add_info_event'] = message.text
    await message.answer("Enter how many places will be on event")
    await BookingFSM.get_places_event.set()


    # rows
@dp.message_handler(state=BookingFSM.get_places_event)
async def process_places_event(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['places_event'] = message.text
    await message.answer("Enter how many rows will be")
    await BookingFSM.get_rows_event.set()

    # result
@dp.message_handler(state=BookingFSM.get_rows_event)
async def process_rows_event(message: Message, state: FSMContext):
    menu = admin_main_menu()
    async with state.proxy() as data:
        data['rows_event'] = message.text
        await db_create_event(data)
    await state.finish()
    await message.answer(f"You have create: {data['name_event']} (cost: {data['cost_ticket']}, weekday: {data['weekday_event']}, time: {data['time_event']}, places:{data['places_event']}, rows: {data['rows_event']})", reply_markup= await menu)


    # Delete event FSM
        
# cancel
@dp.message_handler(commands=['cancel'],state='*')
async def cancel_deleting(message: types.Message, state: FSMContext):
    await message.answer(text='You have canceled deleting')
    await state.finish()


@dp.message_handler(IsAdmin(),Text('Delete event'))   
async def name_deletable_event(message: types.Message):
    await message.answer(text='Type the name of the event you want to delete') 
    await DeleteEventFSM.name_del_event.set() # get name of deletable event


# delete event process
@dp.message_handler(state=DeleteEventFSM.name_del_event)
async def delete_event(message: types.Message, state: FSMContext):
    kb = admin_main_menu()
    async with state.proxy() as data:   
        data['name_del_event'] = message.text
    await db_delete_event(data['name_del_event']) #delete event from db by name from FSM
    await message.answer(text='Event was deleted', reply_markup=await kb)
    await state.finish()










    
    # Update event FSM 

# sill cancel function
@dp.message_handler(commands=['cancel'],state='*')
async def cancel_changing(message:types.Message, state: FSMContext):
    await message.answer(text='You have canceled changes')
    await state.finish()

@dp.message_handler(IsAdmin(), Text('Change event'))
async def select_changes(message: types.Message):
    ikb_change = ikb_change_event()
    await message.answer('Choose what do you want to change', reply_markup= await ikb_change) #select the value to be changed




#  get event by name and change value
@dp.message_handler(state=UpdateFSM.data_val)                
async def change_data_value (message:types.Message, state: FSMContext):
    async with state.proxy() as data:   
        data['data_val'] = message.text
    await state.finish()
    await db_update_value(changing_value, data['name_event'], data['data_val'])
    await message.answer(f"for event {data['name_event']}, {changing_value} now is {data['data_val']}")
        



  # Values change x_x
    
    # name
@dp.callback_query_handler(lambda c: c.data.startswith('name'))
async def changes_name_event(callback: types.CallbackQuery):
    global changing_value
    changing_value ='name'
    chat_id = callback.message.chat.id
    await bot.send_message(chat_id,'Type name of event that you want to change, and than enter new name of event.\n type /cancel to cancel changing')
    fsm = UpdateFSM()
    await fsm.name_event.set()

    # cost
@dp.callback_query_handler(lambda c: c.data.startswith('cost'))
async def changes_cost_event(callback: types.CallbackQuery):
    global changing_value
    changing_value ='cost_event'
    chat_id = callback.message.chat.id
    await bot.send_message(chat_id,'Type name of event that you want to change, and than enter new cost of event.\n type /cancel to cancel changing')
    fsm = UpdateFSM()
    await fsm.name_event.set()
    
    # time
@dp.callback_query_handler(lambda c: c.data.startswith('time'))
async def changes_time_event(callback: types.CallbackQuery):
    global changing_value
    changing_value ='time'
    chat_id = callback.message.chat.id
    await bot.send_message(chat_id,'Type name of event that you want to change, and than enter new time of event.\n type /cancel to cancel changing')
    fsm = UpdateFSM()
    await fsm.name_event.set()

    # weekday
@dp.callback_query_handler(lambda c: c.data.startswith('weekday'))
async def changes_weekend_event(callback: types.CallbackQuery):
    global changing_value
    changing_value ='weekday'
    chat_id = callback.message.chat.id
    await bot.send_message(chat_id,'Type name of event that you want to change, and than enter the new day of week.\n type /cancel to cancel changing')
    fsm = UpdateFSM()
    await fsm.name_event.set()
   
#    add_info
@dp.callback_query_handler(lambda c: c.data.startswith('add_info'))
async def changes_add_info_event(callback: types.CallbackQuery):
    global changing_value
    changing_value ='additional_info'
    chat_id = callback.message.chat.id
    await bot.send_message(chat_id,'Type name of event that you want to change, and than enter new additional info.\n type /cancel to cancel changing')
    fsm = UpdateFSM()
    await fsm.name_event.set()

    # places
@dp.callback_query_handler(lambda c: c.data.startswith('places'))
async def changes_places_event(callback: types.CallbackQuery):
    global changing_value
    changing_value ='places'
    chat_id = callback.message.chat.id
    await bot.send_message(chat_id,'Type name of event that you want to change, and than enter new value of places.\n type /cancel to cancel changing')
    fsm = UpdateFSM()
    await fsm.name_event.set()

    # rows
@dp.callback_query_handler(lambda c: c.data.startswith('rows'))
async def changes_rows_event(callback: types.CallbackQuery):
    global changing_value
    changing_value ='rows'
    chat_id = callback.message.chat.id
    await bot.send_message(chat_id,'Type name of event that you want to change, and than enter new value of rows.\n type /cancel to cancel changing')
    fsm = UpdateFSM()
    await fsm.name_event.set()

    
@dp.message_handler(state=UpdateFSM.name_event)
async def check_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_event'] = message.text
    names = await db_check_names(message.text)
    if names:
        await message.answer("Enter the new value for this event")
        await UpdateFSM.data_val.set() # set new value for event
    else:
        await message.answer(text='There are no events with this name')
        await state.finish()