from http.server import HTTPServer
import threading, sys, argparse, atexit, os

import api_server
import algorithm
import saving
import data
import logging

DEFAULT_ALGORITHM = "random"
DEFAULT_EPH = 100

save_file_name = None

def main():
    global save_file_name

    # Parse arguments
    arg_parser = argparse.ArgumentParser(
        prog="ZPD",
        description="Hiperparametru ietekme uz Q mācīšanos videospēļu vidē. Zinātniskās pētniecības darbs informātikas/programmēšanas sekcijā.",
        epilog="Darba autori: Dāvis Lektauers un Kazimirs Kārlis Brakovskis. Darba vadītāja: Mg. sr. soc. Agnese Kramēna-Juzova")
    
    arg_parser.add_argument(
        "-a", "--algorithm",
        help="Izmantojamais algoritms (no /lib/algorithms direktorija)")
    arg_parser.add_argument(
        "-i", "--input",
        help="Nosaukums datnēm, no kurām ielādēt datus. Ja netiks norādīts, algoritms sāks mācīties no jauna")
    arg_parser.add_argument(
        "-o", "--output",
        help="Nosaukums datnēm, kurās tiks saglabāti dati. Ja netiks norādīts, tie netiks saglabāti")
    arg_parser.add_argument(
        "-eph", "--episodes-per-hyperparameter",
        type=int,
        help="Epizožu skaits spēlē, ik pa kurai tiek nomainīti hiperparametri (EPH)")
    arg_parser.add_argument(
        "-ng", "--no-graphs",
        action="store_true",
        help="Nesaglabāt grafikus")
    arg_parser.add_argument(
        "-nv", "--no-visualization",
        action="store_true",
        help="Izslēgt vizualizāciju atsevišķā logā")
    args = arg_parser.parse_args()

    if not args.no_graphs:
        logging.warn("Grafikus vēl nevar saglabāt!")
    
    # Algorithm selection
    if args.algorithm != None:
        algorithm.set_algorithm(args.algorithm, DEFAULT_ALGORITHM)
    else:
        algorithm.set_algorithm(DEFAULT_ALGORITHM)
        logging.warn(f"Netika norādīts algoritms; tiks izmantots noklusējums: \"{DEFAULT_ALGORITHM}\"")
    logging.log(f"Tiek izmantots algoritms: {algorithm.current_name}")
    
    # Loading
    if args.input != None:
        if saving.load(args.input):
            logging.log(f"Dati ielādēti no \"/data/{args.input}.state.json\" un \"/data/{args.input}.results.json\"")
        else:
            logging.error(f"Radās kļūda, ielādējot datus. Vai datnes \"/data/{args.input}.state.json\" un \"/data/{args.input}.results.json\" eksistē?")
            logging.log("Dati netiks ielādēti")
    else:
        logging.log("Dati netiks ielādēti un algoritms būs sava ceļa gājējs")
    
    # Saving
    if args.output != None:
        save_file_name = args.output
        logging.log(f"Dati tiks saglabāti \"/data/{args.output}.state.json\" un \"/data/{args.output}.results.json\"")
    else:
        logging.warn("Dati netiks saglabāti")

    # Episodes per hyperparameter
    if args.episodes_per_hyperparameter != None:
        data.episodes_per_hyperparameter = args.episodes_per_hyperparameter
        logging.log(f"Tiek izmantota EPH vērtība: {args.episodes_per_hyperparameter}")
    else:
        data.episodes_per_hyperparameter = DEFAULT_EPH
        logging.log(f"Tiek izmantota noklusējuma EPH vērtība: {DEFAULT_EPH}")

    # Start the server and control panel in separate threads
    server_thread = threading.Thread(target=run_server_thread)
    server_thread.start()

    if not args.no_visualization:
        vis_thread = threading.Thread(target=run_vis_thread)
        vis_thread.start()
    
    atexit.register(on_exit)


def run_server_thread():
    server = HTTPServer(("localhost", api_server.PORT), api_server.Server)
    logging.log(f"API serveris pieejams šeit: http://localhost:{api_server.PORT}")

    try:
        while True:
            server.handle_request()
    except KeyboardInterrupt:
        pass

    server.server_close()
    logging.log("API serveris apturēts")

def run_vis_thread():
    logging.warn("Vizualizācija pašlaik nestrādā")


def on_exit():
    if save_file_name != None:
        logging.log("Saglabā datus...")
        if saving.save(save_file_name):
            logging.log("Dati saglabāti!")
        else:
            logging.error("Nevarēja saglabāt datus!")
    
    logging.log("حَرَام Programma pārtraukta.")


if __name__ == "__main__":
    main()