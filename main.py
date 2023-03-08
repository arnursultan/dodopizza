from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
import logging
import time
import os

from buttons import loc_button, num_button, inline_button1, inline_button2, inline_button3
from databases import DataBaseCustomers

db = DataBaseCustomers()
connect = db.connect
db.connect_db()

load_dotenv('bot.py')

bot = Bot(os.environ.get('token'))
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer(f'Здравствуйте, {message.from_user.full_name}')
    await message.answer("Я бот, который поможет вам заказать еду. Но для того, чтобы мы могли доставить ваш заказ, необходимо оставить свой адрес и контактный номер. Спасибо!", reply_markup=inline_button1)
    cursor = connect.cursor()
    cursor.execute(f'SELECT user_id FROM customers WHERE user_id = {message.from_user.id};')
    result = cursor.fetchall()
    if result == []:
        cursor.execute(f"INSERT INTO customers VALUES ('{message.from_user.first_name}', '{message.from_user.last_name}', '{message.from_user.username}', '{message.from_user.id}', 'None');")
    connect.commit()

@dp.callback_query_handler(lambda call : call)
async def inline(call):
    if call.data == 'send_number':
        await get_number(call.message)
    elif call.data == 'send_location':
        await get_location(call.message)
    elif call.data == 'take_order':
        await get_order(call.message)

@dp.message_handler(commands='number')
async def get_number(message:types.Message):
    await message.answer('Подтвердите отправку номера.', reply_markup=num_button)

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def add_number(message:types.Message):
    cursor = connect.cursor()
    cursor.execute(f"UPDATE customers SET phone_number = '{message.contact['phone_number']}' WHERE user_id = {message.from_user.id};")
    connect.commit()
    await message.answer("Ваш номер успешно добавлен.",reply_markup=inline_button3)

@dp.message_handler(commands='location')
async def get_location(message:types.Message):
    await message.answer("Подтвердите отправку местоположения.", reply_markup=loc_button)

@dp.message_handler(content_types=types.ContentType.LOCATION)
async def add_location(message:types.Message):
    address = f"{message.location.longitude}, {message.location.latitude}"
    cursor = connect.cursor()
    cursor.execute(f"INSERT INTO address VALUES ('{message.from_user.id}', '{message.location.longitude}', '{message.location.latitude}');")
    cursor.execute(f"UPDATE orders SET address_destination ='{address}';")
    connect.commit()
    await message.answer("Ваш адрес успешно записан", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(commands='order')
async def get_order(message:types.Message):
    await message.reply("Mеню: ")

    with open('1.webp', 'rb') as photo1:
        await message.answer_photo(photo1, caption='1. Пицца-сказка\n\n25 см, традиционное тесто, 360 г\n\nМоцарелла, смесь сыров чеддер и пармезан, цыпленок, пепперони, соус альфредо\n\nЦена: 399 рублей')

    with open('2.webp', 'rb')as photo2:
        await message.answer_photo(photo2, caption='2. Ветчина и сыр\n\n35 см, традиционное тесто, 670 г\n\nВетчина, моцарелла, фирменный соус альфредо\n\nЦена:729 рублей')

    with open('3.webp', 'rb')as photo3:
        await message.answer_photo(photo3, caption='3. Сырная\n\n35 см, традиционное тесто, 670 г\n\nМоцарелла, сыры чеддер и пармезан, фирменный соус альфредо\n\nЦена:639 рублей')

    with open('4.webp', 'rb')as photo4:
        await message.answer_photo(photo4, caption='4. Двойной цыпленок\n\n35 см, традиционное тесто, 730 г\n\nЦыпленок, моцарелла, соус альфредо\n\nЦена:729 рублей')

    with open('5.webp', 'rb')as photo5:
        await message.answer_photo(photo5, caption='5. Пепперони фреш\n\n35 см, традиционное тесто, 820 г\n\nПикантная пепперони, увеличенная порция моцареллы, томаты, фирменный томатный соус\n\nЦена:639 рублей')

    with open('6.webp', 'rb') as photo6:
        await message.answer_photo(photo6, caption='6. Чоризо фреш\n\n35 см, традиционное тесто, 650 г\n\nФирменный томатный соус, моцарелла, острая чоризо, сладкий перец\n\nЦена:639 рублей')

    with open('7.webp', 'rb') as photo7:
        await message.answer_photo(photo7, caption='7. Додо Микс\n\n35 см, традиционное тесто, 820 г\n\nБекон, цыпленок, ветчина, сыры чеддер и пармезан, соус песто, кубики брынзы, томаты, красный лук, моцарелла, фирменный соус альфредо, чеснок, итальянские травы\n\nЦена:889 рублей')

    with open('8.webp', 'rb') as photo8:
        await message.answer_photo(photo8, caption='8. Сырный цыпленок\n\n35 см, традиционное тесто, 870 г\n\nЦыпленок, моцарелла, сыры чеддер и пармезан, сырный соус, томаты, фирменный соус альфредо, чеснок\n\nЦена:889 рублей')

    with open('9.webp', 'rb') as photo9:
        await message.answer_photo(photo9, caption='9. Карбонара\n\n35 см, традиционное тесто, 880 г\n\nБекон, сыры чеддер и пармезан, моцарелла, томаты, красный лук, чеснок, фирменный соус альфредо, итальянские травы\n\nЦена:889 рублей')

    with open('10.webp', 'rb') as photo10:
        await message.answer_photo(photo10, caption='10. Мясная\n\n35 см, традиционное тесто, 820 г\n\nЦыпленок, ветчина, пикантная пепперони, острая чоризо, моцарелла, фирменный томатный соус\n\nЦена:988 рублей')

    await message.answer("Введите номер из меню и ваш заказ будет записан.")

@dp.message_handler(text=[1, 2 ,3 ,4 , 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
async def add_order(message:types.Message):
    cursor = connect.cursor()
    if message.text == '1':
        cursor.execute(f"INSERT INTO orders VALUES('{message.from_user.id}', ' Пицца-сказка с игрушкой на коробке', '' , '{time.ctime()}');")
    elif message.text == '2':
        cursor.execute(f"INSERT INTO orders VALUES('{message.from_user.id}', ' Ветчина и сыр', '', '{time.ctime()}');")
    elif message.text == '3':
        cursor.execute(f"INSERT INTO orders VALUES('{message.from_user.id}', ' Сырная', '', '{time.ctime()}');")
    elif message.text == '4':
        cursor.execute(f"INSERT INTO orders VALUES('{message.from_user.id}', ' Двойной цыпленок', '', '{time.ctime()}');")
    elif message.text == '5':
        cursor.execute(f"INSERT INTO orders VALUES('{message.from_user.id}', ' Пепперони фреш', '', '{time.ctime()}');")
    elif message.text == '6':
        cursor.execute(f"INSERT INTO orders VALUES('{message.from_user.id}', ' Чоризо фреш', '', '{time.ctime()}');")
    elif message.text == '7':
        cursor.execute(f"INSERT INTO orders VALUES('{message.from_user.id}', ' Додо Микс', '', '{time.ctime()}');")
    elif message.text == '8':
        cursor.execute(f"INSERT INTO orders VALUES('{message.from_user.id}', ' Сырный цыпленок', '', '{time.ctime()}');")
    elif message.text == '9':
        cursor.execute(f"INSERT INTO orders VALUES('{message.from_user.id}', ' Карбонара', '', '{time.ctime()}');")
    elif message.text == '10':   
        cursor.execute(f"INSERT INTO orders VALUES('{message.from_user.id}', ' Мясная', '', '{time.ctime()}');")
    
    connect.commit()
    await message.reply("Ваш заказ записан. Укажите адрес",reply_markup=inline_button2)

executor.start_polling(dp)