import os
import random

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from dotenv import load_dotenv
from sqlalchemy import or_
from sqlalchemy.orm import sessionmaker

from db import engine, TaskCodeForces, Base
from keyboards import inline_buttons_theme, inline_buttons_diff

load_dotenv()
token = os.getenv('TOKEN')

Session = sessionmaker(bind=engine)
session = Session()
bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())
Base.metadata.create_all(engine)

user_data_themes = []


def get_keyboard():
    # Генерация клавиатуры.
    buttons = inline_buttons_theme
    finish_button = types.InlineKeyboardButton(text="Подтвердить", callback_data="data_finish")
    # Благодаря row_width=2, в первом ряду будет две кнопки, а оставшаяся одна
    # уйдёт на следующую строку
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    keyboard.add(finish_button)
    return keyboard


async def update_num_text(message: types.Message, new_value: list):
    # Общая функция для обновления текста с отправкой той же клавиатуры
    await message.edit_text(f"Темы: {new_value}", reply_markup=get_keyboard())


@dp.message_handler(commands="start")
async def start_(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = inline_buttons_diff
    keyboard.add(*buttons)
    await message.answer("Добро пожаловать в <b>CodeForces</b>!" + "\n\n",
                         parse_mode=types.ParseMode.HTML, reply_markup=keyboard)


# @dp.message_handler(
#     Text(equals=get_different_task.data), state=SelectDifficultTheme.difficult)
# async def with_puree(message: types.Message, state: FSMContext):
#     answer_difficult_level = message.text
#     await state.update_data(
#         {
#             "answer": answer_difficult_level
#         }
#     )
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#
#
#     keyboard.add(*buttons)
#     await message.answer("Выберите несколько тем", reply_markup=keyboard)
#     await SelectDifficultTheme.next()

difficult_task = []


@dp.callback_query_handler(Text(startswith="diff_"))
async def cmd_numbers(call: types.CallbackQuery):
    diff = call.data.split("_")[1]
    if diff:
        difficult_task.append(diff)
        await call.message.answer(diff, reply_markup=get_keyboard())
        await call.answer("Выберите темы:")


@dp.callback_query_handler(Text(startswith="data_"))
async def callbacks_num(call: types.CallbackQuery):
    theme = call.data.split("_")[1]
    if theme != "finish":
        user_data_themes.append(theme)
        await update_num_text(call.message, user_data_themes)

    elif theme == "finish":
        await call.message.edit_text(f"Темы: {user_data_themes}" + "\n" + f"Сложность: {difficult_task}")

        filters = [TaskCodeForces.topic_task.like(f'%{t}%') for t in user_data_themes]
        query = session.query(TaskCodeForces).filter(or_(*filters), TaskCodeForces.complexity.in_(difficult_task))
        tasks = random.choices(list(query), k=10)
        for i in tasks:
            print(i.title, i.url, i.topic_task, i.complexity)
            await call.message.answer(
                f"{i.title}" + "\n" + f"{i.url}" + "\n" + f"{i.complexity}"

            )

    await call.answer()


# @dp.message_handler(Text(equals=get_theme_task.data), state=SelectDifficultTheme.theme)
# async def state1(message: types.Message, state: FSMContext):
#     user_answers.append(message.text)
#     print(2)
#     print(user_answers)


# @dp.message_handler()
# async def end_state(message: types.Message, state: FSMContext):
#     await message.answer("<b>Секунду!</b>" + "\n" + "гененирурем уникальную подборку задач для вас",
#                          parse_mode=types.ParseMode.HTML)


# print(result)


if __name__ == "__main__":
    # Запуск бота
    print("Работаем")
    executor.start_polling(dp, skip_updates=True)
