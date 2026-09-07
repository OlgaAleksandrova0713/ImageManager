import os

from config import IMAGES_DIR
from logger import logger

def delete_image(filename):
    filename = os.path.basename(filename)

    file_path = os.path.join(IMAGES_DIR, filename)

    if not os.path.isfile(file_path):
        logger.error(
            "Ошибка: файл %s не найден.",
            filename
        )
        return False

    os.remove(file_path)

    logger.info(
        "Успех: изображение %s удалено.",
        filename
    )
    return True



