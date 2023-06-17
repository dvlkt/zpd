from http.server import HTTPServer

from game_handler.Server import Server
import log
import config

def run() -> None:
    server = HTTPServer(("localhost", config.port), Server)
    log.log(f"API serveris pieejams šeit: http://localhost:{config.port}")

    try:
        while True:
            server.handle_request()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        log.error(e)

    server.server_close()
    log.log("API serveris tika aizvērts.")