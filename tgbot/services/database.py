"""Functions for working with the database"""

from datetime import datetime
from sqlite3 import OperationalError
from sys import exit as sys_exit

from aiosqlite import connect

from tgbot.config import DB_FILE
from tgbot.misc.logger import logger
from tgbot.services.statistics import BotStatisticsData


class Database:
    """A class for working with the database"""

    def __init__(self, path: str) -> None:
        """Defines the path to the database file"""
        self._db_path = path

    async def init(self) -> None:
        """Creates a database file and a table in it"""
        try:
            async with connect(database=self._db_path) as db:
                await db.execute(
                    """
                    CREATE TABLE IF NOT EXISTS counters (
                        date VARCHAR(7) PRIMARY KEY,
                        downloads INTEGER NOT NULL DEFAULT 0,
                        searches INTEGER NOT NULL DEFAULT 0
                    );
                    """
                )
        except OperationalError as ex:
            logger.critical("Database connection error: %s", ex)
            sys_exit()

    async def increase_downloads_counter(self) -> None:
        """Increases the value of the YouTube music download counter"""
        async with connect(database=self._db_path) as db:
            await db.execute(
                """
                INSERT INTO counters (date, downloads) VALUES (?, ?)
                ON CONFLICT (date) DO UPDATE SET downloads=downloads+1;
                """,
                (datetime.now().strftime("%Y.%m"), 1),
            )
            await db.commit()

    async def increase_searches_counter(self) -> None:
        """Increases the value of the YouTube search counter"""
        async with connect(database=self._db_path) as db:
            await db.execute(
                """
                INSERT INTO counters (date, searches) VALUES (?, ?)
                ON CONFLICT (date) DO UPDATE SET searches=searches+1;
                """,
                (datetime.now().strftime("%Y.%m"), 1),
            )
            await db.commit()

    async def get_statistics_data(self) -> BotStatisticsData:
        """Returns the number of downloads and searches made by the bot on YouTube in the last 12 months"""
        dates: list = []
        downloads: list = []
        searches: list = []
        async with connect(database=self._db_path) as db:
            async with db.execute(
                    """SELECT date, downloads, searches FROM counters ORDER BY date DESC LIMIT 12;"""
            ) as cursor:
                async for row in cursor:
                    dates.append(row[0])
                    downloads.append(row[1])
                    searches.append(row[2])
        return BotStatisticsData(date=dates, downloads_counter=downloads, searches_counter=searches)


database: Database = Database(path=DB_FILE)
