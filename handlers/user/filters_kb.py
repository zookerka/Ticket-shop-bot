from aiogram import types
from models.my_sqlltie3 import *
from keyboards.user.ReplyKB import *
from keyboards.user.InlineKB import *
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import datetime
from config import PAYMENT_API_TOKEN
from loader import bot
import uuid

start_parameter = str(uuid.uuid4())
async def Schedule_handler(message: types.Message):
    menu = await user_menu()
    current_day = datetime.datetime.now().strftime("%A")
    rows = await db_weekday_check(current_day)
    if len(rows) > 0:
        await message.answer(text=f'Schedule for {current_day}',  reply_markup=menu)
        for index in range(1, len(rows) + 1):
            await message.answer(text=f'{rows[index - 1]}') 
    else:     
        await message.answer(text='There are no events for today', reply_markup=menu)
        
        
async def main_menu (message: types.Message):
    main_keyboard = await user_menu()
    await message.answer(text='You have returned to main menu', reply_markup=main_keyboard)



class TextState(StatesGroup):
    waiting_for_text = State()

    async def button_handler(self, message: types.Message):
        back_menu = keyboard_main_menu()
        await message.answer("Type the name of event", reply_markup= await back_menu)
        await TextState.waiting_for_text.set()
        
    async def print_name_event(self, message:types.Message, state: FSMContext):
        menu = await user_menu()
        async with state.proxy() as data:
            data['name_event'] = message.text
        event_data = await db_get_data_by_name(data['name_event'])
        await message.answer(text=event_data,reply_markup=menu)
        await state.finish()
        
        
async def start_TextState(message: types.Message):
    fsm = TextState()
    await fsm.button_handler(message)
    await fsm.waiting_for_text.set()


async def Events_handler(message: types.Message):
    menu = user_menu()
    
    rows = await db_check_all()
    response = "All events:\n"
    if rows is not None:
        for row in rows:
            response += f"{row[0]}, Cost: {row[1]}, Weekend: {row[2]}, Time: {row[3]}, Additional info: {row[4]}, Places: {row[5]}, Rows: {row[6]}\n ---------------------------------------------------------------------------------------- \n"
        await message.answer(response, reply_markup= await menu)
    else:
        await message.answer("No rows found.", reply_markup= await menu)



class BuyTicket(StatesGroup):
    event_name = State()
    
    
    async def cancel_buy(self, message: types.Message, state: FSMContext):
        main_menu = await user_menu()
        await message.answer(text='You have canceled buying', reply_markup=main_menu)
        await state.finish()

    async def start_geting(self, message: types.Message):
        back_menu = keyboard_main_menu()
        await message.answer("Type the name of event", reply_markup= await back_menu)
        await BuyTicket.event_name.set()
        
    async def data_name_event(self, message: types.Message, state: FSMContext):
        cancel = await keyboard_cancel()
        async with state.proxy() as data:
            data['name_event'] = message.text
        if len(await db_check_names(data['name_event'])) > 0:
            if PAYMENT_API_TOKEN.split(':')[1] == 'TEST':
                await message.answer(text='Test payment')
            places_data = await db_book_place(data['name_event'])
            if places_data:
                price = await db_get_price(data['name_event'])
                fin_price = price[0] * 100
                prices = [
        types.LabeledPrice(label='Ticket', amount = fin_price),
        
    ] 

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

        
        
        
async def start_BuyTicket(message: types.Message):
    fsm = BuyTicket()
    await fsm.start_geting(message)
    await fsm.event_name.set()
    
    
    
    
    
    
    
    
    
    
    
