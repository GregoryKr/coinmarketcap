from aiogram.fsm.state import StatesGroup, State


class DataState(StatesGroup):
    name = State()
    coin = State()
    # height = State()


# class RunState(StatesGroup):
#     actions = State()
#     duration = State()
#
#
# class WalkingState(StatesGroup):
#     actions = State()
#     duration = State()
#
#
#
# class SwimmingState(StatesGroup):
#     actions = State()
#     duration = State()
#     length_pool = State()
#     count_pool = State()
