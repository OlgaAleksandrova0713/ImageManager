def send_html(handler, status_code, html, close=False):
    response_bytes = html.encode("utf-8")

    handler.send_response(status_code)
    handler.send_header(
        "Content-Type",
        "text/html; charset=utf-8"
    )
    handler.send_header(
        "Content-Length",
        str(len(response_bytes))
    )

    if close:
        handler.send_header("Connection", "close")

    handler.end_headers()

    handler.wfile.write(response_bytes)


def send_error_response(handler, message):
    from logger import logger

    logger.error(message)
    print(f"ERROR: {message}")

    response = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Error</title>
    </head>
    <body>
        <h1>Error 400</h1>
        <p>{message}</p>
        <p><a href="/">Try again</a></p>
    </body>
    </html>
    """

    send_html(
        handler,
        400,
        response,
        close=True
    )