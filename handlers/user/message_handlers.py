from aiogram import types
from models.my_sqlltie3 import *
from keyboards.user.ReplyKB import *
from keyboards.user.InlineKB import *
from aiogram.dispatcher import FSMContext
from fsm.user.text_state import GetEventState
import datetime
from config import PAYMENT_API_TOKEN
from loader import bot, dp
from aiogram.dispatcher.filters import Text
import uuid
from fsm.user.but_ticket_state import BuyTicket




   # Main menu backkk 
@dp.message_handler(Text('Back to main menu'))     
async def main_menu (message: types.Message):
    main_keyboard = await user_menu()
    await message.answer(text='You have returned to main menu', reply_markup=main_keyboard)


    # Events for today
@dp.message_handler(Text('Schedule for today'))
async def Schedule_handler(message: types.Message):
    menu = await user_menu()
    current_day = datetime.datetime.now().strftime("%A") #get current dau with datetime
    data = await db_weekday_check(current_day)  #get data by current day
    if len(data) > 0:  
        await message.answer(text=f'Schedule for {current_day}',  reply_markup=menu)
        for index in range(1, len(data) + 1):
            await message.answer(text=f'{data[index - 1]}') 
    else:     
        await message.answer(text='There are no events for today', reply_markup=menu)


    # Get event name to FSM from user
@dp.message_handler(Text('Info about event'))
async def button_handler(message: types.Message):
    back_menu = keyboard_main_menu()
    await message.answer("Type the name of event", reply_markup= await back_menu)
    await GetEventState.waiting_for_text.set()

    # Get event data from db by name from FSM
@dp.message_handler(state=GetEventState.waiting_for_text)    
async def print_name_event(message:types.Message, state: FSMContext):
    menu = await user_menu()
    async with state.proxy() as data: 
        data['name_event'] = message.text  #record text in fsm state, to use it.
    event_data = await db_get_data_by_name(data['name_event'])  #use our recorded data in database fucntion 
    await message.answer(text=event_data,reply_markup=menu) 
    await state.finish() 
        


# return for user all events info
@dp.message_handler(Text('Events'))
async def Events_handler(message: types.Message):
    menu = user_menu()
    
    # loop for get all data from db
    rows = await db_check_all()
    response = "All events:\n"
    if rows is not None:
        for row in rows:
            # response text
            response += f"{row[0]}, Cost: {row[1]}, Weekend: {row[2]}, Time: {row[3]}, Additional info: {row[4]}, Places: {row[5]}, Rows: {row[6]}\n ---------------------------------------------------------------------------------------- \n"
        await message.answer(response, reply_markup= await menu)
    else:
        await message.answer("No rows found.", reply_markup= await menu)









    # Buy ticket FSM

@dp.message_handler(commands=['cancel'], state='*')
async def cancel_buy(message: types.Message, state: FSMContext):
    main_menu = await user_menu()
    await message.answer(text='You have canceled buying', reply_markup=main_menu)
    await state.finish()


    # set buying fsm
@dp.message_handler(Text('Buy a ticket'))
async def start_geting(message: types.Message):
    back_menu = keyboard_main_menu()
    await message.answer("Type the name of event", reply_markup= await back_menu)
    await BuyTicket.event_name.set()

    # buy process 
@dp.message_handler(state=BuyTicket.event_name)
async def data_name_event(message: types.Message, state: FSMContext):
    start_parameter = str(uuid.uuid4())
    cancel = await keyboard_cancel() #cancel button
    async with state.proxy() as data:
        data['name_event'] = message.text
    if len(await db_check_names(data['name_event'])) > 0:    #check name
        if PAYMENT_API_TOKEN.split(':')[1] == 'TEST':  # check api token
            await message.answer(text='Test payment')  
        places = await db_book_place(data['name_event']) #get places
        if places: 
            price = await db_get_price(data['name_event']) #get price
            fin_price = price[0] * 100 #  *100 to get not cents
            prices = [
    types.LabeledPrice(label='Ticket', amount = fin_price),
    
] 
            # send offer
            await bot.send_invoice(message.chat.id,
                                start_parameter=start_parameter,
                                title='Buy Ticket',
                                provider_token=PAYMENT_API_TOKEN,
                                currency="rub",
                                is_flexible=False,
                                prices=prices,
                                description='description',
                                payload='test-payload')
            await state.finish()
        else:
            await message.answer(text='We are out of seats', reply_markup=cancel)
            await state.finish()
    else:
        await message.answer(text='There are no events with this name')

    

    
    
    
    
    
    
    
    
    
    
