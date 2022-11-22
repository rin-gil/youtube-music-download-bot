"""Describes the state for the FSM (Final State Machine)"""

from aiogram.dispatcher.filters.state import StatesGroup, State


class UserInput(StatesGroup):
    """Controls whether the bot reacts to the user's messages"""

    Block = State()
