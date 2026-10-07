import os

from config import IMAGES_DIR, UPLOADS_DIR
from logger import logger


def delete_image(filename):
    filename = filename.strip("/")

    categories = [
        "fruits",
        "nature",
        "style",
        "animals",
        "city",
        "other"
    ]

    file_path = None

    # Search for the file inside category folders
    for category in categories:
        possible_path = os.path.join(
            IMAGES_DIR,
            category,
            filename
        )

        if os.path.isfile(possible_path):
            file_path = possible_path
            break

    # Search for the file inside uploads category folders
    if file_path is None:
        for category in categories:
            possible_path = os.path.join(
                UPLOADS_DIR,
                category,
                filename
            )

            if os.path.isfile(possible_path):
                file_path = possible_path
                break

    # Also check the root images folder
    if file_path is None:
        possible_path = os.path.join(
            IMAGES_DIR,
            filename
        )

        if os.path.isfile(possible_path):
            file_path = possible_path

    if file_path is None:
        logger.error(
            "Error: file %s not found.",
            filename
        )
        return False

    os.remove(file_path)

    logger.info(
        "Success: image %s deleted.",
        filename
    )

    return True

