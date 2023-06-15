from http.server import HTTPServer
import threading, sys, argparse

import api_server
import algorithm

DEFAULT_ALGORITHM = "random"

def main():
    # Parse arguments
    arg_parser = argparse.ArgumentParser(
        prog="ZPD",
        description="Hiperparametru ietekme uz Q mācīšanos videospēļu vidē. Zinātniskās pētniecības darbs informātikas/programmēšanas sekcijā.",
        epilog="Darba autori: Dāvis Lektauers un Kazimirs Kārlis Brakovskis. Darba vadītāja: Mg. sr. soc. Agnese Kramēna-Juzova")
    
    arg_parser.add_argument(
        "-a", "--algorithm",
        help="Izmantojamais algoritms (no /lib/algorithms direktorija)")
    arg_parser.add_argument(
        "-i", "--state-input",
        help="Ceļš uz failu, no kura ielādēt algoritma iekšējo stāvokli. Ja netiks norādīts, algoritms sāks mācīties no jauna")
    arg_parser.add_argument(
        "-o", "--state-output",
        help="Ceļš uz failu, kur tiks saglabāts algoritma iekšējais stāvoklis. Ja netiks norādīts, tas netiks saglabāts")
    arg_parser.add_argument(
        "-d", "--result-output",
        help="Ceļš uz failu, kur saglabāt algoritma rezultātus spēlē. Ja netiks norādīts, tie netiks saglabāti.")
    arg_parser.add_argument(
        "-g", "--graph-output",
        help="Ceļš uz direktoriju, kur saglabāt Matplotlib grafikus par rezultātiem spēlē. Ja netiks norādīts, grafiki netiks izveidoti")
    arg_parser.add_argument(
        "-nv", "--no-visualization",
        action="store_true",
        help="Izslēgt vizualizāciju atsevišķā logā")
    args = arg_parser.parse_args()

    if args.state_input:
        print("Stāvokli vēl nevar ielādēt!")
    if args.state_output:
        print("Stāvokli vēl nevar saglabāt!")
    if args.result_output:
        print("Rezultātus vēl nevar saglabāt!")
    if args.graph_output:
        print("Grafikus vēl nevar saglabāt!")
    
    # Algorithm selection
    if args.algorithm != None:
        algorithm.set_algorithm(args.algorithm, DEFAULT_ALGORITHM)
    else:
        algorithm.set_algorithm(DEFAULT_ALGORITHM)
        print(f"⚠️  Tiks izmantots noklusējuma algoritms: \"{DEFAULT_ALGORITHM}\"")

    # Start the server and control panel in separate threads
    server_thread = threading.Thread(target=run_server_thread)
    server_thread.start()

    if not args.no_visualization:
        vis_thread = threading.Thread(target=run_vis_thread)
        vis_thread.start()


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

def run_vis_thread():
    print("🎛️  Vizualizācija pašlaik nestrādā.")


if __name__ == "__main__":
    main()