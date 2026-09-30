import os

from config import IMAGES_DIR, ALLOWED_EXTENSIONS
from logger import logger

def rename_image(old_filename, new_filename):
    old_filename = old_filename.strip("/")
    new_filename = os.path.basename(new_filename)

    old_extension = os.path.splitext(old_filename)[1].lower()
    new_extension = os.path.splitext(new_filename)[1].lower()

    if old_extension not in ALLOWED_EXTENSIONS:
        logger.error(
            "Ошибка: недопустимый формат исходного файла %s.",
            old_filename
        )
        return False, "Недопустимый формат исходного файла."

    if not new_extension:
        new_filename = f"{new_filename}{old_extension}"
        new_extension = old_extension

    if new_extension not in ALLOWED_EXTENSIONS:
        logger.error(
            "Ошибка: недопустимый формат нового файла %s.",
            new_filename
        )
        return False, "Разрешены только JPG, PNG, GIF."

    old_path = os.path.join(
        IMAGES_DIR,
        old_filename
    )

    category = os.path.dirname(old_filename)

    new_path = os.path.join(
        IMAGES_DIR,
        category,
        new_filename
    )

    if not os.path.isfile(old_path):
        logger.error(
            "Ошибка: файл %s не найден.",
            old_filename
        )
        return False, "Изображение не найдено."

    if os.path.exists(new_path):
        logger.error(
            "Ошибка: файл %s уже существует.",
            new_filename
        )
        return False, "Файл с таким именем уже существует."

    os.rename(old_path, new_path)

    logger.info(
        "Успех: изображение %s переименовано в %s.",
        old_filename,
        new_filename
    )

    return True, "Изображение успешно переименовано."


