from http.server import HTTPServer
import threading, sys

import api_server
import control_panel

def main():
	# Start the server and control panel in separate threads
	server_thread = threading.Thread(target=run_server_thread)
	server_thread.start()

	if not "--nogui" in sys.argv:
		panel_thread = threading.Thread(target=run_panel_thread)
		panel_thread.start()


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

	try:
		while True:
			control_panel.process()
	except KeyboardInterrupt:
		pass

	print("🛑 Kontroles panelis apturēts.")


if __name__ == "__main__":
	main()