"""The module contains various decorators used in the project code"""

from asyncio import get_running_loop
from functools import wraps
from typing import Any


def run_in_asyncio_thread(func: Any) -> Any:
    """Decorator that runs a function in a separate asynchronous thread."""

    @wraps(func)
    async def wrapper(*args: Any) -> Any:
        return await get_running_loop().run_in_executor(None, func, *args)

    return wrapper
