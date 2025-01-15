import os
import asyncio
import logging
import multiprocessing

from aiogram import Bot, Dispatcher

from dotenv import load_dotenv

from bot.handlers import router

from cmc.coinmarket import update_coin_table, url, coin_rate


load_dotenv()


async def main():
    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    process = multiprocessing.Process(target=update_coin_table)
    process.start()
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
    process.join()

