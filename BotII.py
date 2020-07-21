import conf
import apiai, json

from aiogram.utils import executor
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram import types

bot = Bot(token=conf.token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Привет хочешь поговорить?")

@dp.message_handler()
async def message(message: types.Message):
    request = apiai.ApiAI(conf.tokenAPI).text_request()
    request.lang = 'ru'
    request.session_id=conf.token
    request.query = message.text
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech']
    if response:
       await bot.send_message(message.from_user.id, response)
    else:
       await bot.send_message(message.from_user.id, "Я вас не понял!")

if __name__ == '__main__':
    executor.start_polling(dp)