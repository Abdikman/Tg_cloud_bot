async def document_path(message, bot):
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    return file_path

async def photo_path(message, bot):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    return file_path

async def video_path(message, bot):
    file_id = message.video.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    return file_path

async def audio_path(message, bot):
    file_id = message.audio.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    return file_path
