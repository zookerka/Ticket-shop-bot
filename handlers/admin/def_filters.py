from aiogram import types
from keyboards.user.ReplyKB import *
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from models.my_sqlltie3 import *


class BookingFSM(StatesGroup):
    get_name_event = State()
    get_cost_ticket = State()
    get_weekday_event = State()
    get_time_event = State()
    get_add_info_event = State()
    get_places_event = State()
    get_rows_event = State()
    cancel_state = State()


    async def cancel_booking(self, message: Message, state: FSMContext):
        await message.answer("You have canceled the creating")
        await state.finish()
        
    async def start(self, message: Message):
        await message.answer("Type the name of event")
        await BookingFSM.get_name_event.set()

    async def process_name_event(self, message: Message, state: FSMContext):
        async with state.proxy() as data:
            data['name_event'] = message.text
        await message.answer("Type the cost of ticket")
        await BookingFSM.get_cost_ticket.set()

    async def process_cost_ticket(self, message: Message, state: FSMContext):
        async with state.proxy() as data:
            data['cost_ticket'] = message.text
        await message.answer("Type the weekend of event")
        await BookingFSM.get_weekday_event.set()
        
    async def process_weekday_event(self, message: Message, state: FSMContext):
        async with state.proxy() as data:
            data['weekday_event'] = message.text
        await message.answer("Type the time of event")
        await BookingFSM.get_time_event.set()
        
    async def process_time_event(self, message: Message, state: FSMContext):
        async with state.proxy() as data:
            data['time_event'] = message.text
        await message.answer("Type the additional info of event")
        await BookingFSM.get_add_info_event.set()
        
    async def process_add_info_event(self, message: Message, state: FSMContext):
        async with state.proxy() as data:
            data['add_info_event'] = message.text
        await message.answer("Type the how many places will be on event")
        await BookingFSM.get_places_event.set()
        
    async def process_places_event(self, message: Message, state: FSMContext):
        async with state.proxy() as data:
            data['places_event'] = message.text
        await message.answer("Type the how many rows will be")
        await BookingFSM.get_rows_event.set()
    

    async def process_rows_event(self, message: Message, state: FSMContext):
        menu = admin_main_menu()
        async with state.proxy() as data:
            data['rows_event'] = message.text
            await db_create_event(data)
        await state.finish()
        await message.answer(f"You have create: {data['name_event']} (cost: {data['cost_ticket']}, weekday: {data['weekday_event']}, time: {data['time_event']}, places:{data['places_event']}, rows: {data['rows_event']})", reply_markup= await menu)



async def start_button_clicked(message: types.Message):
    await message.answer("You started the process of creating event. Type /cancel to cancel the creating")
    await BookingFSM.get_name_event.set()
    fsm = BookingFSM()
    await fsm.start(message=message)



async def get_data(message: types.Message):
    menu = admin_main_menu()
    
    rows = await db_check_all()
    response = "All events:\n"
    if rows is not None:
        for row in rows:
            response += f"{row[0]}, Cost: {row[1]}, Weekend: {row[2]}, Time: {row[3]}, Additional info: {row[4]}, Places: {row[5]}, Rows: {row[6]}\n ---------------------------------------------------------------------------------------- \n"
        await message.answer(response, reply_markup= await menu)
    else:
        await message.answer("No rows found.", reply_markup= await menu)





    
    
class UpdateFSM(StatesGroup):
    name_event = State()
    data_val = State()        
    
    async def cancel_changing(self, message:types.Message, state: FSMContext):
        await message.answer(text='You have canceled changes')
        await state.finish()
    
    
    async def start_changes(self, message: types.Message):
        await message.answer(text='Type the name of event that you want to change')

        
    async def check_name(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['name_event'] = message.text
        names = await db_check_names(message.text)
        if names:
            await message.answer("Type the new value of event")
            await UpdateFSM.data_val.set()
        else:
            await message.answer(text='There are no events with this name')
            await state.finish()
                
                    
    async def change_data_value (self, message:types.Message, state: FSMContext):
        async with state.proxy() as data:   
            data['data_val'] = message.text
        await state.finish()
        await db_update_value(changing_value, data['name_event'], data['data_val'])
        await message.answer(f"{data['name_event']}, {data['data_val']}")

        
    
    
        
async def select_changes(message: types.Message):
    kb_change = kb_change_event()
    await message.answer('Choose what do you want to change', reply_markup= await kb_change)

async def changes_name_event(message:types.Message):
    global changing_value
    changing_value ='name'
    await message.answer('You chose to change a name of event. type /cancel to cancel changing')
    fsm = UpdateFSM()
    await fsm.start_changes(message)
    await fsm.name_event.set()

async def changes_cost_event(message:types.Message):
    global changing_value
    changing_value ='cost_event'
    await message.answer('You chose to change a tickets price of event.')
    fsm = UpdateFSM()
    await fsm.start_changes(message)
    await fsm.name_event.set()
    
async def changes_time_event(message:types.Message):
    global changing_value
    changing_value ='time'
    await message.answer('You chose to change a time of event.')
    fsm = UpdateFSM()
    await fsm.start_changes(message)
    await fsm.name_event.set()
    
async def changes_weekend_event(message:types.Message):
    global changing_value
    changing_value ='weekday'
    await message.answer('You chose to change a weekday of event.')
    fsm = UpdateFSM()
    await fsm.start_changes(message)
    await fsm.name_event.set()
   
async def changes_add_info_event(message:types.Message):
    global changing_value
    changing_value ='additional_info'
    await message.answer('You chose to change a additional info of event.')
    fsm = UpdateFSM()
    await fsm.start_changes(message)
    await fsm.name_event.set()
 
async def changes_places_event(message:types.Message):
    global changing_value
    changing_value ='places'
    await message.answer('You chose to change a places of event.')
    fsm = UpdateFSM()
    await fsm.start_changes(message)
    await fsm.name_event.set()

async def changes_rows_event(message:types.Message):
    global changing_value
    changing_value ='rows'
    await message.answer('You chose to change a rows of event.')
    fsm = UpdateFSM()
    await fsm.start_changes(message)
    await fsm.name_event.set()




class DeleteEventFSM(StatesGroup):
    
    name_del_event = State()
    
    async def cancel_deleting(self, message: types.Message, state: FSMContext):
        await message.answer(text='You have canceled deleting')
        await state.finish()
    
    async def name_deletable_event(self, message: types.Message):
        await message.answer(text='Type the name of the event you want to delete')
        await DeleteEventFSM.name_del_event.set()

    async def delete_event(self, message: types.Message, state: FSMContext):
        kb = admin_main_menu()
        async with state.proxy() as data:   
            data['name_del_event'] = message.text
        await db_delete_event(data['name_del_event'])
        await message.answer(text='Event was deleted', reply_markup=await kb)
        await state.finish()

    
    
async def confidance_del(message:types.Message):
    fsm = DeleteEventFSM()
    await fsm.name_deletable_event(message)

    
