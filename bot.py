import os
from aiogram.types.input_file import FSInputFile
from aiogram import Bot

TG_TOKEN = str(os.getenv("TG_TOKEN"))
TG_CLIENT_ID = int(os.getenv("TG_CLIENT_ID"))

bot = Bot(token=TG_TOKEN)

async def send_files(files):
    for f in files:
        document = FSInputFile(f)
        await bot.send_document(TG_CLIENT_ID, document)
