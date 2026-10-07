import os

from config import IMAGES_DIR, UPLOADS_DIR, ALLOWED_EXTENSIONS
from logger import logger

def rename_image(old_filename, new_filename):
    old_filename = old_filename.strip("/")
    new_filename = os.path.basename(new_filename)

    old_extension = os.path.splitext(old_filename)[1].lower()
    new_extension = os.path.splitext(new_filename)[1].lower()

    if old_extension not in ALLOWED_EXTENSIONS:
        logger.error(
            "Error: invalid format of source file %s.",
            old_filename
        )
        return False, "Invalid source file format."

    if not new_extension:
        new_filename = f"{new_filename}{old_extension}"
        new_extension = old_extension

    if new_extension not in ALLOWED_EXTENSIONS:
        logger.error(
            "Error: invalid format for new file %s.",
            new_filename
        )
        return False, "Only JPG, PNG, and GIF are allowed."

    old_path = os.path.join(
        IMAGES_DIR,
        old_filename
    )

    base_dir = IMAGES_DIR

    if not os.path.isfile(old_path):
        old_path = os.path.join(
            UPLOADS_DIR,
            old_filename
        )
        base_dir = UPLOADS_DIR

    category = os.path.dirname(old_filename)

    new_path = os.path.join(
        base_dir,
        category,
        new_filename
    )

    if not os.path.isfile(old_path):
        logger.error(
            "Error: file %s not found.",
            old_filename
        )
        return False, "Image not found."

    if os.path.exists(new_path):
        logger.error(
            "Error: file %s already exists.",
            new_filename
        )
        return False, "A file with that name already exists."

    os.rename(old_path, new_path)

    logger.info(
        "Success: Image %s renamed to %s.",
        old_filename,
        new_filename
    )

    return True, new_filename


