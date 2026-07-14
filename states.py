from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):

    phone = State()

    manual_phone = State()

    front_id = State()

    back_id = State()

    selfie_id = State()