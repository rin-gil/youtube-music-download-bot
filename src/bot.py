"""Launches the bot"""

from functools import partial

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.utils.executor import start_polling, start_webhook
from aiohttp import ClientSession

from tgbot.config import Config, load_config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin

from tgbot.handlers.callbacks import register_callbacks
from tgbot.handlers.commands import register_commands
from tgbot.handlers.errors import register_errors
from tgbot.handlers.messages import register_messages
from tgbot.middlewares.localization import i18n
from tgbot.misc.commands import set_default_commands
from tgbot.misc.logger import logger
from tgbot.services.database import Database


def register_all_middlewares(dp: Dispatcher) -> None:
    """Registers middlewares"""
    dp.middleware.setup(i18n)


def register_all_filters(dp: Dispatcher) -> None:
    """Registers filters"""
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp: Dispatcher) -> None:
    """Registers handlers"""
    register_admin(dp=dp)
    register_commands(dp=dp)
    register_messages(dp=dp)
    register_callbacks(dp=dp)
    register_errors(dp=dp)


async def on_startup(dp: Dispatcher, database: Database, config: Config) -> None:
    """The functions that runs when the bot starts"""
    await database.init()
    await set_default_commands(dp)
    if config.webhook:
        await dp.bot.set_webhook(
            url=f"{config.webhook.wh_host}/{config.webhook.wh_path}",
            drop_pending_updates=False,
            secret_token=config.webhook.wh_token,
        )


async def on_shutdown(dp: Dispatcher, database: Database, config: Config) -> None:
    """The functions that runs when the bot is stopped"""
    await dp.storage.close()
    await dp.storage.wait_closed()
    await database.close()
    if config.webhook:
        await dp.bot.delete_webhook()
        session: ClientSession = await dp.bot.get_session()
        await session.close()


def start_bot() -> None:
    """Starts the bot"""
    config: Config = load_config()
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    storage: MemoryStorage | RedisStorage2 = (
        RedisStorage2(
            host=config.redis.host,
            port=config.redis.port,
            db=config.redis.database_index,
            password=config.redis.password,
            prefix="ymdb_fsm",
        )
        if config.redis
        else MemoryStorage()
    )
    dp: Dispatcher = Dispatcher(bot=bot, storage=storage)
    database: Database = Database(db_config=config.db)
    bot["config"] = config
    bot["db"] = database

    register_all_middlewares(dp=dp)
    register_all_filters(dp=dp)
    register_all_handlers(dp=dp)

    if config.webhook:
        start_webhook(
            dispatcher=dp,
            webhook_path=f"/{config.webhook.wh_path}",
            on_startup=partial(on_startup, database=database, config=config),
            on_shutdown=partial(on_shutdown, database=database, config=config),
            host=config.webhook.app_host,
            port=config.webhook.app_port,
        )
    else:
        start_polling(
            dispatcher=dp,
            on_startup=partial(on_startup, database=database, config=config),
            on_shutdown=partial(on_shutdown, database=database, config=config),
        )


if __name__ == "__main__":
    logger.info("Starting bot")
    try:
        start_bot()
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception as ex:
        logger.critical("Unknown error: %s", repr(ex))
    logger.info("Bot stopped!")
