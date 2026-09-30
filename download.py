import os

from config import IMAGES_DIR


def get_image_for_download(filename):
    file_path = os.path.join(
        IMAGES_DIR,
        filename
    )

    if not os.path.isfile(file_path):
        return None, None

    with open(file_path, "rb") as file:
        data = file.read()

    return os.path.basename(filename), data

