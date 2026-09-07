from email.parser import BytesParser
from email.policy import default
import os
import uuid

from config import IMAGES_DIR, MAX_FILE_SIZE, ALLOWED_EXTENSIONS
from logger import logger
from responses import send_html, send_error_response


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

    for part in message.iter_parts():

        if part.get_param(
            "name",
            header="Content-Disposition"
        ) != "image":
            continue

        filename = part.get_filename()

        if not filename:
            send_error_response(
                handler,
                "Файл не выбран."
            )
            return

        extension = os.path.splitext(filename)[1].lower()

        if extension not in ALLOWED_EXTENSIONS:
            send_error_response(
                handler,
                "Недопустимый формат файла. "
                "Разрешены: JPG, PNG, GIF."
            )
            return

        file_data = part.get_payload(decode=True)

        if len(file_data) > MAX_FILE_SIZE:
            send_error_response(
                handler,
                "Размер файла превышает допустимые 5 MB."
            )
            return

        unique_filename = f"{uuid.uuid4()}{extension}"

        os.makedirs(IMAGES_DIR, exist_ok=True)

        file_path = os.path.join(
            IMAGES_DIR,
            unique_filename
        )

        with open(file_path, "wb") as file:
            file.write(file_data)

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
        </head>
        <body>
            <h1>Upload successful!</h1>

            <p>Файл успешно загружен.</p>

            <p>
                <a href="/images/{unique_filename}">
                    Открыть изображение
                </a>
            </p>

            <p>
                <a href="/upload">
                    Загрузить ещё
                </a>
            </p>

            <p>
                <a href="/">
                    На главную
                </a>
            </p>
        </body>
        </html>
        """

        send_html(handler, 200, response)
        return

    send_error_response(
        handler,
        "Файл изображения не найден."
    )