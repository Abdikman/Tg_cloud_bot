from aiogram.fsm.state import StatesGroup, State

class bot_download_states(StatesGroup):
    all = State()
    name = State()
    file = State()
    media_id = State()
    input_name = State()
    input_description = State()
    file_type = State()
    file_path = State()

class file_action(StatesGroup):
    user_id = State()
    name = State()
    new_name = State()
    question = State()
    new_description = State()
    action = State()
    path_date = State()
    path_type = State()
    file_path = State()
    search_date = State()
    list1 = State()
