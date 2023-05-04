from http.server import HTTPServer
import threading, sys

import api_server, control_panel
import algorithm

def main():
    # Start the server and control panel in separate threads
    #server_thread = threading.Thread(target=run_server_thread)
    #server_thread.start()

    if not "--nogui" in sys.argv:
        panel_thread = threading.Thread(target=run_panel_thread)
        panel_thread.start()
    
    # Parse CLI arguments
    for i in sys.argv:
        if "--algorithm=" in i:
            algorithm.set_algorithm(i[12:])


def run_server_thread():
    server = HTTPServer(("localhost", api_server.PORT), api_server.Server)
    print(f"🚀 API serveris pieejams šeit: http://localhost:{api_server.PORT}")

    try:
        while True:
            server.handle_request()
    except KeyboardInterrupt:
        pass

    server.server_close()
    print("🛑 API serveris apturēts.")

def run_panel_thread():
    print("🎛️  Kontroles panelis veiksmīgi atvērts!")

    control_panel.init()

    try:
        while True:
            control_panel.process()
    except KeyboardInterrupt:
        pass

    print("🛑 Kontroles panelis apturēts.")


if __name__ == "__main__":
    main()