from aiogram.fsm.state import StatesGroup, State

class bot_download_states(StatesGroup):
    all = State()
    name = State()
    file = State()
    question = State()
    file_type = State()
    file_path = State()

class file_action(StatesGroup):
    user_id = State()
    name = State()
    new_name = State()
    action = State()
    path_date = State()
    path_type = State()
    file_path = State()
    search_name = State()
    search_date = State()
    search_type = State()
    list1 = State()
