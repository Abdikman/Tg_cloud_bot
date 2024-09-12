import logging, os

async def history_update(user_id, text):
    if 'User_logging' not in os.listdir():
        os.mkdir('User_logging')

    py_logger = logging.getLogger(f"User_logging/{str(user_id)}")

    py_handler = logging.FileHandler(f"User_logging/{user_id}.log", mode='a', encoding='utf-8')
    py_formatter = logging.Formatter("%(levelname)s %(asctime)s: %(message)s")

    py_handler.setFormatter(py_formatter)
    py_logger.addHandler(py_handler)

    py_logger.info(text+'\n')

async def delete_history(user_id):
    with open(f'User_logging/{user_id}.log', 'w', encoding='utf-8') as file:
        file.write('')
