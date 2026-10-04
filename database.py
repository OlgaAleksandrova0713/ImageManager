import psycopg2

def get_connection():
    connection = psycopg2.connect(
        host="db",
        port=5432,
        dbname="images_db",
        user="postgres",
        password="password"
    )

    return connection

def save_image_metadata(filename, original_name, size, file_type):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO images
                (filename, original_name, size, file_type)
            VALUES (%s, %s, %s, %s)
            """,
            (filename, original_name, size, file_type)
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()

def get_images(page=1, per_page=10):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        offset = (page - 1) * per_page

        cursor.execute(
            """
            Select
                id,
                filename,
                original_name,
                size,
                upload_time,
                file_type
            From images
            Order By upload_time DESC
            Limit %s Offset %s
            """,
            (per_page, offset)
        )

        images = cursor.fetchall()

        return images

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    connection = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="images_db",
        user="postgres",
        password="password"
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            filename,
            original_name,
            size,
            upload_time,
            file_type
        FROM images
        ORDER BY upload_time DESC
        """
    )

    images = cursor.fetchall()

    for image in images:
        print(image)

    cursor.close()
    connection.close()

if __name__ == "__main__":
    connection = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="images_db",
        user="postgres",
        password="password"
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            filename,
            original_name,
            size,
            upload_time,
            file_type
        FROM images
        ORDER BY upload_time DESC
        """
    )

    images = cursor.fetchall()

    BLUE_BOLD = "\033[1;36m"
    RESET = "\033[0m"

    for image in images:
        print(f"{BLUE_BOLD}id{RESET} = {image[0]}")
        print(f"{BLUE_BOLD}filename{RESET} = {image[1]}")
        print(f"{BLUE_BOLD}original_name{RESET} = {image[2]}")
        print(f"{BLUE_BOLD}size{RESET} = {image[3]}")
        print(f"{BLUE_BOLD}upload_time{RESET} = {image[4]}")
        print(f"{BLUE_BOLD}file_type{RESET} = {image[5]}")
        print("-" * 50)

    cursor.close()
    connection.close()

def get_images_count():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM images
            """
        )

        count = cursor.fetchone()[0]

        return count

    finally:
        cursor.close()
        connection.close()

def get_image_by_id(image_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                filename,
                original_name,
                size,
                upload_time,
                file_type
            FROM images
            WHERE id = %s
            """,
            (image_id,)
        )

        image = cursor.fetchone()

        return image

    finally:
        cursor.close()
        connection.close()

def delete_image_metadata(image_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM images
            WHERE id = %s
            """,
            (image_id,)
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()