import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

from aiogram import types, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.settings import text as txt
from bot.kb import get_menu, register_user
from bot.states import DataState
from bot.models import User, Coin, Base
from cmc.coinmarket import coins_list


load_dotenv()

router = Router()

engine = create_engine(os.getenv('DB_URL'))
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


@router.message(Command("start"))
async def start_handler(message: Message) -> None:
    """
    Проверяет регистрацию пользователя, если пользователь зарегистрирован, направляет меню(клавиатуру).
    Если нет, то направляет меню для регистрации
    :param message:
    :return: None
    """
    user_id = message.from_user.id
    session = Session()
    user = session.query(User).filter_by(tg_id=user_id).first()
    if user:
        await message.answer(text=txt.menu_text, reply_markup=get_menu())
        session.close()
    else:
        await message.answer(text=txt.user_not_in_base, reply_markup=register_user())
        session.close()


@router.callback_query(F.data == "data")
async def registration_handler(call: types.CallbackQuery, state: FSMContext) -> None:
    """
    Handler для запуска процесса регистрации
    :param call:  call от пользователя
    :param state: объект состояния
    :return: None
    """
    await state.set_state(DataState.name)
    await call.message.answer(text=txt.name)

@router.message(DataState.name)
async def name_handler(message: Message, state: FSMContext) -> None:
    """
    Проверяет корректность ввода возраста и устанавливает DataState.height
    :param message: команда от пользователя
    :param state: объект состояния
    :return: None
    """
    name = message.text
    user_id = message.from_user.id
    if name.isalpha():
        with Session() as session:
            new_user = User(tg_id=user_id, name=name)
            session.add(new_user)
            session.commit()
    # await state.set_state(DataState.coin)
        await message.answer(text=f'Welcome, {name}', reply_markup=get_menu())
    else:
        await state.set_state(DataState.name)
        await message.answer(text=txt.incorrect_name)

@router.callback_query(F.data == "info")
async def choose_coin(call: types.CallbackQuery, state: FSMContext) -> None:
    """
    Handler для выбора валюты
    :param call:  call от пользователя
    :param state: объект состояния
    :return: None
    """
    # необходимо добавить функцию, которая покажет весь списко монет
    await state.set_state(DataState.coin)
    await call.message.answer(text=txt.choose_coin)

@router.message(DataState.coin)
async def border_value(message: Message, state: FSMContext) -> None:
    """
    Добавляет введенные границы в базу данных
    :param message: команда от пользователя
    :param state: объект состояния
    :return: None
    """
    border_value = message.text
    # try:
    #     border_value = float(border_value)
    #     await state.set_state(DataState.border_value)
    #     await message.answer(text=f"Выбрана валюта {border_value} USD")
    # except ValueError:
    #     await state.set_state(DataState.coin)
    #     await message.answer(text=txt.incorrect_border_value)
