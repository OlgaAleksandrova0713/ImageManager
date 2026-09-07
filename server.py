from http.server import ThreadingHTTPServer
from handlers import ImageServer


server = ThreadingHTTPServer(("0.0.0.0", 8000), ImageServer)



