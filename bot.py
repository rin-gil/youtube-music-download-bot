import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tgbot import register_commands, register_messages, register_callbacks, load_config


def register_all_handlers(dp):
    register_commands(dp)
    register_messages(dp)
    register_callbacks(dp)


async def main():
    config = load_config()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML', disable_web_page_preview=True)
    dp = Dispatcher(bot, storage=MemoryStorage())
    bot['config'] = config
    register_all_handlers(dp)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())

