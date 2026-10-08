from email.parser import BytesParser
from email.policy import default
import os
import uuid

from config import UPLOADS_DIR, MAX_FILE_SIZE, ALLOWED_EXTENSIONS
from logger import logger
from responses import send_html, send_error_response
from database import save_image_metadata


def handle_upload(handler):
    content_length = int(
        handler.headers.get("Content-Length", 0)
    )

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
    image_parts = []

    for part in message.iter_parts():

        field_name = part.get_param(
            "name",
            header="Content-Disposition"
        )

        if field_name == "category":
            category = part.get_payload(
                decode=True
            ).decode("utf-8").strip()

        elif field_name == "image":
            image_parts.append(part)

    if not category:
        send_error_response(
            handler,
            "Category not selected."
        )
        return

    if not image_parts:
        send_error_response(
            handler,
            "No file selected."
        )
        return

    uploaded_files = []

    category_dir = os.path.join(
        UPLOADS_DIR,
        category
    )

    os.makedirs(
        category_dir,
        exist_ok=True
    )

    for image_part in image_parts:

        filename = image_part.get_filename()

        if not filename:
            continue

        extension = os.path.splitext(
            filename
        )[1].lower()

        if extension not in ALLOWED_EXTENSIONS:
            send_error_response(
                handler,
                f"Invalid file format: {filename}. "
                "Allowed: JPG, PNG, GIF."
            )
            return

        file_data = image_part.get_payload(
            decode=True
        )

        if len(file_data) > MAX_FILE_SIZE:
            send_error_response(
                handler,
                f"The file {filename} exceeds "
                "the 5 MB limit."
            )
            return

        unique_filename = (
            f"{uuid.uuid4()}{extension}"
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

        uploaded_files.append(
            unique_filename
        )

        logger.info(
            "Успех: изображение %s загружено.",
            unique_filename
        )

        print(
            f"SUCCESS: изображение "
            f"{unique_filename} загружено."
        )

    if not uploaded_files:
        send_error_response(
            handler,
            "No valid files selected."
        )
        return

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
                    ✓ Images uploaded successfully!
                </h1>

                <p class="success-text">
                    {len(uploaded_files)}
                    image(s) uploaded successfully.
                </p>

                <div class="success-buttons">

                    <a
                        href="/upload"
                        class="home-button"
                    >
                        Upload more
                    </a>

                    <a
                        href="/images-list"
                        class="home-button"
                    >
                        Images List
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
                <source
                    src="/static/music.mp3"
                    type="audio/mpeg"
                >
                Your browser does not support
                the audio element.
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