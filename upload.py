from email.parser import BytesParser
from email.policy import default
import os
import uuid

from config import IMAGES_DIR, MAX_FILE_SIZE, ALLOWED_EXTENSIONS
from logger import logger
from responses import send_html, send_error_response
from database import save_image_metadata


def handle_upload(handler):
    content_length = int(
        handler.headers.get("Content-Length", 0)
    )

    if content_length > MAX_FILE_SIZE:
        handler.rfile.read(content_length)

        send_error_response(
            handler,
            "Размер файла превышает допустимые 5 MB."
        )
        return

    content_type = handler.headers.get("Content-Type", "")

    if "multipart/form-data" not in content_type:
        send_error_response(
            handler,
            "Неверный формат запроса."
        )
        return

    body = handler.rfile.read(content_length)

    headers = (
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {content_length}\r\n"
        "\r\n"
    )

    message = BytesParser(policy=default).parsebytes(
        headers.encode() + body
    )

    category = None
    image_part = None

    for part in message.iter_parts():

        field_name = part.get_param(
            "name",
            header="Content-Disposition"
        )

        if field_name == "category":
            category = part.get_payload(decode=True).decode("utf-8").strip()

        elif field_name == "image":
            image_part = part

    if not category:
        send_error_response(
            handler,
            "Category not selected."
        )
        return

    if image_part is None:
        send_error_response(
            handler,
            "No file selected."
        )
        return

    filename = image_part.get_filename()

    if not filename:
        send_error_response(
            handler,
            "No file selected."
        )
        return

    extension = os.path.splitext(filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        send_error_response(
            handler,
            "Invalid file format." "Allowed: JPG, PNG, GIF."
        )
        return

    file_data = image_part.get_payload(decode=True)

    if len(file_data) > MAX_FILE_SIZE:
        send_error_response(
            handler,
            "The file size exceeds the 5 MB limit."
        )
        return

    unique_filename = f"{uuid.uuid4()}{extension}"

    category_dir = os.path.join(
        IMAGES_DIR,
        category
    )

    os.makedirs(
        category_dir,
        exist_ok=True
    )

    file_path = os.path.join(
        category_dir,
        unique_filename
    )

    with open(file_path, "wb") as file:
        file.write(file_data)

    save_image_metadata(
        unique_filename,
        filename,
        len(file_data),
        extension
    )

    logger.info(
        "Успех: изображение %s загружено.",
        unique_filename
    )

    print(
        f"SUCCESS: изображение {unique_filename} загружено."
    )

    response = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Upload successful</title>

        <link rel="stylesheet" href="/static/style.css">
        <link rel="stylesheet" href="/static/upload.css">
    </head>

    <body>

        <div class="music-background"></div>

        <div class="upload-page">

            <div class="upload-card">

            <h1 class="success-title">
                ✓ Image uploaded successfully!
            </h1>

            <p class="success-text">
                Your image has been uploaded successfully.
            </p>

            <div class="success-buttons">

                <a
                    href="/images/{category}/{unique_filename}"
                     class="home-button"
                >
                    Open image
                </a>

                <a
                    href="/upload"
                    class="home-button"
                >
                    Upload another
                </a>

                <a
                    href="/"
                    class="home-button"
                >
                    Home
                </a>

            </div>

        </div>

        <audio controls loop>
            <source src="/static/music.mp3" type="audio/mpeg">
                Your browser does not support the audio element.
        </audio>
        
    </div>

</body>
</html>
"""
    send_html(
        handler,
        200,
        response
    )
    return