import os
import asyncio
import logging
import multiprocessing

from aiogram import Bot, Dispatcher

from dotenv import load_dotenv

from bot.handlers import router
from bot.comparison import compare

from cmc.coinmarket import update_coin_table, url, coin_rate

# logging.getLogger('sqlalchemy.engine').setLevel(logging.CRITICAL)
load_dotenv()


async def main():
    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher()
    dp.include_router(router)
    loop = asyncio.get_event_loop()
    loop.create_task(compare())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

    # await compare()
    # try:
    #     task = asyncio.create_task(compare())
    #     await task
    # except asyncio.CancelledError:
    #     print("Фоновая задача остановлена.")


if __name__ == "__main__":
    # process = multiprocessing.Process(target=update_coin_table)
    # process.start()
    logging.basicConfig(level=logging.INFO)
    # logging.getLogger('sqlalchemy.engine.Engine').setLevel(logging.WARNING)
    asyncio.run(main())
    # asyncio.run(compare())
    # process.join()


