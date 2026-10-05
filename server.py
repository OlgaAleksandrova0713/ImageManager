import os

from http.server import ThreadingHTTPServer
from handlers import ImageServer


port = int(os.environ.get("PORT", 8000))

server = ThreadingHTTPServer(
    ("0.0.0.0", port),
    ImageServer
)

