import datetime
import os
import aiohttp
import asyncio
import pandas as pd

import db
import bot

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

WB_SELLER_TOKEN = os.getenv('WB_SELLER_TOKEN')

async def periodic_segment(async_session):
    # prepare query parameters
    half_an_hour_ago = datetime.datetime.now() - datetime.timedelta(minutes=30)
    params = {
        "dateFrom": "T".join(str(half_an_hour_ago).split(" ")),
        "flag": 0
    }
    headers = {
        "Authorization": WB_SELLER_TOKEN
    }

    # load data from WB API and write it to DB
    async def load_and_write_data(session, api_link, obj_type):
        async with session.get(api_link, params=params, headers=headers) as response:
            if response.status != 200:
                return

            res = [obj_type(**obj) for obj in await response.json()]
            await db.insert_objects(async_session, res)

    async with aiohttp.ClientSession(trust_env=True) as session:
        await asyncio.gather(
            load_and_write_data(session, 'https://statistics-api.wildberries.ru/api/v1/supplier/orders', db.Order),
            load_and_write_data(session, 'https://statistics-api.wildberries.ru/api/v1/supplier/sales', db.Sale)
        )
        # await asyncio.wait([
        #     load_and_write_data(session, 'https://statistics-api.wildberries.ru/api/v1/supplier/orders', db.Order),
        #     load_and_write_data(session, 'https://statistics-api.wildberries.ru/api/v1/supplier/sales', db.Sale)
        # ], return_when=asyncio.ALL_COMPLETED)

    # select data from DB
    orders_df = pd.DataFrame( await db.select_objects(async_session, db.Order, half_an_hour_ago) )
    sales_df = pd.DataFrame( await db.select_objects(async_session, db.Sale, half_an_hour_ago) )
    # alternatively, return API result from load_and_write_data, remove await from insert_objects and remove selects

    # save files and send them to telegram bot
    orders_df.to_excel("orders.xlsx")
    sales_df.to_excel("sales.xlsx")

    await bot.send_files(["orders.xlsx", "sales.xlsx"])

async def main():
    # create in-memory DB with tables
    engine = create_async_engine("sqlite+aiosqlite://", echo=True)

    async with engine.begin() as conn:
        await conn.run_sync(db.Base.metadata.create_all)

    async_session = async_sessionmaker(engine, expire_on_commit=False)

    # run task every 30 minutes
    while True:
        await asyncio.gather(
            asyncio.sleep(1800),
            periodic_segment(async_session),
        )

if __name__ == "__main__":
    asyncio.run(main())