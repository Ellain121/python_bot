import my_token_unsecure
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, KeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup
from aiogram.filters import Command
import asyncio
import time
import logging
import my_user_id
from datetime import datetime

logging.basicConfig(level=logging.INFO)
bot = Bot(token=my_token_unsecure.Token)
dp = Dispatcher()
router = Router()

##################
bStart = False
bPhoto = False


def get_time():
    return int(datetime.now().strftime("%H"))


@router.message(Command("start"))
async def start_cmd(message: Message):
    global bStart
    await bot.send_message(my_user_id.user_id, "Good, Now fill in sticker and send it to me. I'll wait patiently.", reply_markup=ReplyKeyboardRemove())
    bStart = True


@router.message(F.photo)
async def photo_cmd(message: Message):
    global bPhoto
    await bot.download(
        message.photo[-1],
        destination=f"./data/{message.photo[-1].file_id}.jpg"
    )
    bPhoto = True
    await bot.send_message(my_user_id.user_id, "Thanks m8, have a good day!")
    exit()


async def start_day():
    global bStart
    success = False
    kb_start = [
        [KeyboardButton(text="/start")]
    ]
    keyboard_start = ReplyKeyboardMarkup(keyboard=kb_start)

    while not success:
        print(bStart, success)
        await bot.send_message(my_user_id.user_id, "Let's start your day!", reply_markup=keyboard_start, )
        await asyncio.sleep(60 * 1)  # 30 mins
        success = bStart


async def maui_routine():
    print("I've been there!")
    await start_day()


async def task_starter():
    while True:
        # await bot.send_message(my_user_id.user_id, "Hello")
        time = get_time()
        if time >= 8:
            await maui_routine()
            break
        await asyncio.sleep(60)


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


loop = asyncio.get_event_loop()
sub_task = loop.create_task(task_starter())
main_task = loop.create_task(main())
loop.run_until_complete(main_task)

pending = asyncio.all_tasks(loop=loop)

for task in pending:
    task.cancel()

group = asyncio.gather(*pending, return_exceptions=True)
loop.run_until_complete(group)
loop.close()
