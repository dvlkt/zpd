from http.server import HTTPServer
import threading, sys, argparse, atexit, os

import api_server
import algorithm
import saving
import data

DEFAULT_ALGORITHM = "random"

state_save_path = None
result_save_path = None

def main():
    global state_save_path, result_save_path

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
        help="Ceļš uz datni, no kura ielādēt algoritma iekšējo stāvokli. Ja netiks norādīts, algoritms sāks mācīties no jauna")
    arg_parser.add_argument(
        "-o", "--state-output",
        help="Ceļš uz datni, kur tiks saglabāts algoritma iekšējais stāvoklis. Ja netiks norādīts, tas netiks saglabāts")
    arg_parser.add_argument(
        "-d", "--result-output",
        help="Ceļš uz datni, kur saglabāt algoritma rezultātus spēlē. Ja netiks norādīts, tie netiks saglabāti.")
    arg_parser.add_argument(
        "-g", "--graph-output",
        help="Ceļš uz direktoriju, kur saglabāt Matplotlib grafikus par rezultātiem spēlē. Ja netiks norādīts, grafiki netiks izveidoti")
    arg_parser.add_argument(
        "-nv", "--no-visualization",
        action="store_true",
        help="Izslēgt vizualizāciju atsevišķā logā")
    args = arg_parser.parse_args()

    if args.graph_output:
        print("⚠️  Grafikus vēl nevar saglabāt!")
    
    # Algorithm selection
    if args.algorithm != None:
        algorithm.set_algorithm(args.algorithm, DEFAULT_ALGORITHM)
    else:
        algorithm.set_algorithm(DEFAULT_ALGORITHM)
        print(f"⚠️  Netika norādīts algoritms; tiks izmantots noklusējums: \"{DEFAULT_ALGORITHM}\"")
    print(f"🤖 Tiek izmantots algoritms: {algorithm.current_name}")
    print()
    
    # State loading
    if args.state_input != None:
        if saving.load_state(args.state_input):
            print(f"💾 Algoritma iekšējais stāvoklis ielādēts no {os.path.join(data.directory, args.state_input)}")
        else:
            print(f"⚠️  Radās kļūda ielādējot algoritma stāvokli. Vai datne \"{os.path.join(data.directory, args.state_input)}\" eksistē?")
            print("💾 Algoritma iekšējais stāvoklis nav ielādēts no nevienas datnes")
    else:
        print("💾 Algoritma iekšējais stāvoklis nav ielādēts no nevienas datnes un algoritms būs sava ceļa gājējs")
    print()
    
    # State saving
    if args.state_output != None:
        state_save_path = args.state_output
        print(f"💾 Algoritma iekšējais stāvoklis tiks saglabāts datnē {os.path.join(data.directory, args.state_output)}")
    else:
        print("💾 Algoritma iekšējais stāvoklis netiks saglabāts")
    print()

    # Result saving
    if args.result_output != None:
        result_save_path = args.result_output
        print(f"💾 Spēles rezultāti tiks saglabāti datnē {os.path.join(data.directory, args.result_output)}")
    else:
        print("💾 Spēles rezultāti netiks saglabāti")
    print()

    # Start the server and control panel in separate threads
    server_thread = threading.Thread(target=run_server_thread)
    server_thread.start()

    if not args.no_visualization:
        vis_thread = threading.Thread(target=run_vis_thread)
        vis_thread.start()
    
    atexit.register(on_exit)


def run_server_thread():
    server = HTTPServer(("localhost", api_server.PORT), api_server.Server)
    print(f"🚀 API serveris pieejams šeit: http://localhost:{api_server.PORT}")

    try:
        while True:
            server.handle_request()
    except KeyboardInterrupt:
        pass

    server.server_close()
    print("🛑 API serveris apturēts")

def run_vis_thread():
    print("🎛️  Vizualizācija pašlaik nestrādā")


def on_exit():
    if state_save_path != None:
        print("💾 Saglabā algoritma iekšējo stāvokli...")
        if saving.save_state(state_save_path):
            print("💾 Algoritma iekšējais stāvoklis saglabāts!")
        else:
            print("⚠️  Nevarēja saglabāt iekšējo stāvokli!")
    print()

    if result_save_path != None:
        print("💾 Saglabā spēles rezultātus...")
        if saving.save_results(result_save_path):
            print("💾 Spēles rezultāti saglabāti!")
        else:
            print("⚠️  Nevarēja saglabāt spēles rezultātus!")
    
    print("حَرَام Programma pārtraukta.")


if __name__ == "__main__":
    main()