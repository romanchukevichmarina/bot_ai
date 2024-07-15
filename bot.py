from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.filters.command import Command
import os
from openai import OpenAI
import asyncio
from dotenv import load_dotenv
import datetime

import database

load_dotenv()
database.create_tables()
print("db created")
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'), base_url="https://api.proxyapi.ru/openai/v1",)

dp = Dispatcher()
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
  await message.answer("""Привет! Это телеграм-бот для ответа на учебные вопросы :)
                       Чтобы вывести список команд, напиши /help""")
  database.insert_messages(message_id = message.message_id, user_id=message.chat.id, text=message.text, datetime=datetime.datetime.now())

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
  await message.answer("""Список команд:
                       /start -- приветсвие :)
                       /newquestion -- задать вопрос боту (максимум 3 вопроса в день!)
                       /limit -- посмотреть сколько вопросов осталось
                       /help -- вывести список команд""")
  database.insert_messages(message_id = message.message_id, user_id=message.chat.id, text=message.text, datetime=datetime.datetime.now())

@dp.message(Command("newquestion"))
async def cmd_new_question(message: types.Message):
  await message.answer("Введите условие задачи")
  database.insert_messages(message_id = message.message_id, user_id=message.chat.id, text=message.text, datetime=datetime.datetime.now())

@dp.message()
async def ask_gpt(message: types.Message):
  database.insert_messages(message_id = message.message_id, user_id=message.chat.id, text=message.text, datetime=datetime.datetime.now())
  msg_list = database.get_last_commands(message.chat.id)
  msg_list.reverse()
  print(msg_list)
  cmnd = "/newquestion"
  if msg_list[1][0] == cmnd:
    if msg_list[0][0] == cmnd or msg_list[2][0] == cmnd:
      await message.answer("Чтобы задать вопрос, надо ввести условие задачи после /newquestion")
    else:
      await message.answer("Введите свое решение")
  elif msg_list[0][0] == cmnd:
    if msg_list[2][0] == cmnd:
      await message.answer("Чтобы задать вопрос, надо ввести условие задачи после /newquestion")
    else:
      print(msg_list[2][0])
      response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
          {
            "role": "system",
            "content": f"Найди ошибки в решении задачи.\nУсловие: {msg_list[1][0]}\nРешение:\n'''{msg_list[2][0]}'''"
          }
        ],
      )
      await message.reply(response.choices[0].message.content)
  else:
    await message.answer("Простите, я отвечаю только на учебные вопросы :( Чтобы задать вопрос, введите /newquestion")

async def main():
  BOT_TOKEN = os.getenv("TELEGRAM_BOT_KEY")
  bot = Bot(BOT_TOKEN)
  
  await dp.start_polling(bot)
  
if __name__ == '__main__':
  asyncio.run(main())