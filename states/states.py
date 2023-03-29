from aiogram.dispatcher.filters.state import StatesGroup, State


class SelectDifficultTheme(StatesGroup):
    difficult = State()
    theme = State()
    end = State()
