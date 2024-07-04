async def history_update(user_id, text):
    with open(f'id_{user_id}/logging_history.txt', 'a', encoding='utf-8') as file:
        file.write(str(text) + '\n')

async def delete_history(user_id):
    with open(f'id_{user_id}/logging_history.txt', 'w', encoding='utf-8') as file:
        file.write('')
