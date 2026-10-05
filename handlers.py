from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import os

from config import IMAGES_DIR, ALLOWED_EXTENSIONS
from pages import home_page, upload_page, gallery_page, images_list_page
from responses import send_html, send_error_response
from upload import handle_upload
from delete import delete_image
from download import get_image_for_download
from rename import rename_image
from database import (
    get_images,
    get_images_count,
    get_image_by_id,
    delete_image_metadata,
    get_image_by_filename,
    delete_image_metadata_by_filename,
    update_image_filename
)


class ImageServer(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/":
            send_html(
                self,
                200,
                home_page()
            )
            return

        if self.path == "/upload":
            send_html(
                self,
               200,
                upload_page()
            )
            return

        if self.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return

        if self.path == "/static/style.css":
            with open("static/style.css", "rb") as file:
                css = file.read()

            self.send_response(200)
            self.send_header(
                "Content-Type",
                "text/css; charset=utf-8"
            )
            self.send_header(
                "Content-Length",
                str(len(css))
            )
            self.end_headers()

            self.wfile.write(css)
            return

        if self.path == "/static/music.mp3":
            with open("static/music.mp3", "rb") as file:
                music = file.read()

            self.send_response(200)
            self.send_header(
                "Content-Type",
                "audio/mpeg"
            )
            self.send_header(
                "Content-Length",
                str(len(music))
            )
            self.end_headers()

            self.wfile.write(music)
            return

        if self.path.startswith("/static/images/"):
            image_name = self.path[len("/static/images/"):]

            file_path = os.path.join(
                "static",
                "images",
                image_name
            )

            if os.path.isfile(file_path):
                with open(file_path, "rb") as file:
                    image = file.read()

                self.send_response(200)
                self.send_header(
                    "Content-Type",
                    "image/jpeg"
                )
                self.send_header(
                    "Content-Length",
                    str(len(image))
                )
                self.end_headers()

                self.wfile.write(image)
                return

            send_error_response(
                self,
                "Image not found."
            )
            return

        if self.path.startswith("/download/"):
            path = self.path[len("/download/"):]

            category, filename = path.split("/", 1)

            filename, data = get_image_for_download(
                os.path.join(category, filename)
            )

            if data is None:
                send_error_response(
                    self,
                    "Ошибка: изображение не найдено."
                )
                return

            self.send_response(200)
            self.send_header(
                "Content-Type",
                "application/octet-stream"
            )
            self.send_header(
                "Content-Disposition",
                f"attachment; filename={filename}"
            )
            self.send_header(
                "Content-Length",
                str(len(data))
            )
            self.end_headers()

            self.wfile.write(data)
            return

        if self.path == "/category/fruits":
            category_dir = os.path.join(
                IMAGES_DIR,
                "fruits"
            )

            files = os.listdir(category_dir)

            image_file = [
                file
                for file in files
                if os.path.splitext(file)[1].lower()
                in ALLOWED_EXTENSIONS
            ]

            send_html(
                self,
                200,
                gallery_page(
                    image_file,
                    "fruits"
                )
            )
            return

        if self.path == "/category/nature":
            category_dir = os.path.join(
                IMAGES_DIR,
                "nature"
            )

            files = os.listdir(category_dir)

            image_file = [
                file
                for file in files
                if os.path.splitext(file)[1].lower()
                in ALLOWED_EXTENSIONS
            ]

            send_html(
                self,
                200,
                gallery_page(
                    image_file,
                    "nature"
                )
            )
            return

        if self.path == "/category/style":
            category_dir = os.path.join(
                IMAGES_DIR,
                "style"
            )

            files = os.listdir(category_dir)

            image_file = [
                file
                for file in files
                if os.path.splitext(file)[1].lower()
                   in ALLOWED_EXTENSIONS
            ]

            send_html(
                self,
                200,
                gallery_page(
                    image_file,
                    "style"
                )
            )
            return

        if self.path == "/category/animals":
            category_dir = os.path.join(
                IMAGES_DIR,
                "animals"
            )

            files = os.listdir(category_dir)

            image_file = [
                file
                for file in files
                if os.path.splitext(file)[1].lower()
                   in ALLOWED_EXTENSIONS
            ]

            send_html(
                self,
                200,
                gallery_page(
                    image_file,
                    "animals"
                )
            )
            return

        if self.path == "/category/city":
            category_dir = os.path.join(
                IMAGES_DIR,
                "city"
            )

            files = os.listdir(category_dir)

            image_file = [
                file
                for file in files
                if os.path.splitext(file)[1].lower()
                   in ALLOWED_EXTENSIONS
            ]

            send_html(
                self,
                200,
                gallery_page(
                    image_file,
                    "city"
                )
            )
            return

        if self.path == "/category/other":
            category_dir = os.path.join(
                IMAGES_DIR,
                "other"
            )

            files = os.listdir(category_dir)

            image_file = [
                file
                for file in files
                if os.path.splitext(file)[1].lower()
                   in ALLOWED_EXTENSIONS
            ]

            send_html(
                self,
                200,
                gallery_page(
                    image_file,
                    "other"
                )
            )
            return

        if self.path == "/images/":
            categories = [
                "fruits",
                "nature",
                "style",
                "animals",
                "city",
                "other"
            ]

            all_images = []

            for category in categories:
                category_dir = os.path.join(
                    IMAGES_DIR,
                    category
                )

                if not os.path.isdir(category_dir):
                    continue

                files = os.listdir(category_dir)

                for filename in files:
                    if os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS:
                        all_images.append(
                            (category, filename)
                        )

            send_html(
                self,
                200,
                gallery_page(
                    all_images
                )
            )
            return

        if self.path.startswith("/images/"):
            image_path = self.path[len("/images/"):]

            file_path = os.path.join(
                IMAGES_DIR,
                image_path
            )

            if os.path.isfile(file_path):
                with open(file_path, "rb") as file:
                    content = file.read()

                self.send_response(200)
                self.send_header(
                    "Content-Type",
                     "image/jpeg"
                )
                self.send_header(
                    "Content-Length",
                    str(len(content))
                )
                self.end_headers()
                self.wfile.write(content)
                return

            send_error_response(
                self,
                "Page not found."
            )
            return

        if self.path.startswith("/images-list"):
            query = urlparse(self.path).query
            params = parse_qs(query)

            page = int(params.get("page", [1])[0])
            deleted = params.get("deleted", [None])[0]

            images = get_images(
                page=page,
                per_page=10
            )

            total_image = get_images_count()

            send_html(
                self,
                200,
                images_list_page(
                    images,
                    page,
                    total_image,
                    deleted
                )
            )
            return

        send_error_response(
            self,
            "Page not found."
        )

    def do_POST(self):

        if self.path.startswith("/delete/") and self.path.count("/") >= 3:
            path = self.path[len("/delete/"):]

            try:
                category, filename = path.split("/", 1)
            except ValueError:
                send_error_response(
                    self,
                    "Error: invalid delete path."
                )
                return

            filename = filename.strip()

            image = get_image_by_filename(filename)


            if image is None:
                send_error_response(
                    self,
                    "Error: image not found."
                )
                return

            success = delete_image(filename)

            if not success:
                send_error_response(
                    self,
                    "Error: image file not found."
                )
                return

            delete_image_metadata_by_filename(filename)

            self.send_response(200)
            self.end_headers()

            return

        if self.path.startswith("/delete/"):
            image_id = self.path[len("/delete/"):]

            try:
                image_id = int(image_id)
            except ValueError:
                send_error_response(
                    self,
                    "Error: invalid image ID."
                )
                return

            image = get_image_by_id(image_id)

            if image is None:
                send_error_response(
                    self,
                    "Error: image not found."
                )
                return

            filename = image[1]

            success = delete_image(filename)

            if not success:
                send_error_response(
                    self,
                    "Error: image file not found."
                )
                return

            delete_image_metadata(image_id)

            self.send_response(303)
            self.send_header(
                "Location",
                "/images-list?deleted=1"
            )
            self.end_headers()

            return

        if self.path.startswith("/rename/"):
            old_filename = self.path[len("/rename/"):]

            content_length = int(
                self.headers.get("Content-Length", 0)
            )

            body = self.rfile.read(content_length)

            from urllib.parse import parse_qs

            form_data = parse_qs(
                body.decode("utf-8")
            )

            new_filename = form_data.get(
                "new_filename",
                [""]
            )[0].strip()

            if not new_filename:
                send_error_response(
                    self,
                    "Новое имя файла не указано."
                )
                return

            success, message = rename_image(
                old_filename,
                new_filename
            )

            if success:
                update_image_filename(
                    os.path.basename(old_filename),
                    message
                )

                print(
                    "DATABASE RENAME:",
                    os.path.basename(old_filename),
                    "->",
                    message,
                    flush=True
                )

                send_html(
                    self,
                    200,
                    f"""
                    <h1>Image renamed successfully!</h1>
                    <p>New filename: {message}</p>
                    <p>
                        <a href="/images/">
                            Back to gallery
                        </a>
                    </p>
                    """
                )
            else:
                send_error_response(
                    self,
                    message
                )

            return

        if self.path != "/upload":
            send_error_response(
                self,
                "Неверный путь."
            )
            return

        handle_upload(self)
