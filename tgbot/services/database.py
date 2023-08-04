"""Functions for working with the database"""

from datetime import datetime

from asyncpg import create_pool, Pool

from tgbot.config import DbConfig
from tgbot.services.statistics import BotStatisticsData


class Database:
    """A class for working with the database"""

    def __init__(self, db_config: DbConfig) -> None:
        """Defines the path to the database file"""
        self._db_dsn: str = (
            f"postgresql://{db_config.user}:{db_config.password}@{db_config.host}:{db_config.port}/{db_config.database}"
        )
        self._pool: Pool | None = None

    async def _get_pool(self) -> Pool:
        """Creates and returns a pool of database connections"""
        if not self._pool:
            self._pool = await create_pool(dsn=self._db_dsn)
        return self._pool

    async def init(self) -> None:
        """Creates tables in the database"""
        pool: Pool = await self._get_pool()
        await pool.execute("""
            CREATE TABLE IF NOT EXISTS counters (
                date VARCHAR(7) PRIMARY KEY,
                downloads INTEGER NOT NULL DEFAULT 0,
                searches INTEGER NOT NULL DEFAULT 0
            );
            """)

    async def increase_downloads_counter(self) -> None:
        """Increases the value of the YouTube music download counter"""
        pool: Pool = await self._get_pool()
        await pool.execute(
            """
            INSERT INTO counters AS c (date, downloads) VALUES ($1, $2)
            ON CONFLICT (date) DO UPDATE SET downloads=c.downloads+1;
            """,
            datetime.now().strftime("%Y.%m"),
            1,
        )

    async def increase_searches_counter(self) -> None:
        """Increases the value of the YouTube search counter"""
        pool: Pool = await self._get_pool()
        await pool.execute(
            """
            INSERT INTO counters AS c (date, searches) VALUES ($1, $2)
            ON CONFLICT (date) DO UPDATE SET searches=c.searches+1;
            """,
            datetime.now().strftime("%Y.%m"),
            1,
        )

    async def get_statistics_data(self) -> BotStatisticsData:
        """Returns the number of downloads and searches made by the bot on YouTube in the last 12 months"""
        pool: Pool = await self._get_pool()
        dates: list = []
        downloads: list = []
        searches: list = []
        for row in await pool.fetch("""SELECT date, downloads, searches FROM counters ORDER BY date DESC LIMIT 12;"""):
            dates.append(row[0])
            downloads.append(row[1])
            searches.append(row[2])
        return BotStatisticsData(date=dates, downloads_counter=downloads, searches_counter=searches)

    async def close(self) -> None:
        """Closes the database connection pool"""
        if self._pool:
            await self._pool.close()
            self._pool = None
