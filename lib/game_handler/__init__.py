from http.server import HTTPServer

from game_handler.Server import Server
import logging
import config

def run() -> None:
    server = HTTPServer(("localhost", config.port), Server)
    logging.log(f"API serveris pieejams šeit: http://localhost:{config.port}")

    try:
        while True:
            server.handle_request()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logging.error(e)

    server.server_close()
    logging.log("API serveris tika aizvērts.")