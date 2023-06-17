import argparse

import config
import log
import algo_handler

def parse():
    arg_parser = argparse.ArgumentParser(
        prog="ZPD",
        description="Hiperparametru ietekme uz Q mācīšanos videospēļu vidē. Zinātniskās pētniecības darbs informātikas/programmēšanas sekcijā.",
        epilog="Darba autori: Dāvis Lektauers un Kazimirs Kārlis Brakovskis. Darba vadītāja: Mg. sr. soc. Agnese Kramēna-Juzova")
    
    arg_parser.add_argument(
        "-p", "--port",
        type=int,
        help="Ports, ko izmantot (atkarīgs no spēles)")
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
        help="Epizožu skaits spēlē, ik pa kurai tiek nomainīti hiperparametri un restartēts algoritms (EPH)")
    arg_parser.add_argument(
        "-ng", "--no-graphs",
        action="store_true",
        help="Nesaglabāt grafikus")
    arg_parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Rādīt pilnīgi visu izvadi terminālī")
    args = arg_parser.parse_args()
    
    # Port selection
    if args.port != None:
        config.port = args.port
    else:
        config.port = config.DEFAULT_PORT
        log.warn(f"Netika norādīts ports; tiks izmantots noklusējums: {config.port}")
    log.log(f"Tiek izmantots ports: {config.port}")

    # Algorithm selection
    if args.algorithm != None:
        config.algorithm = args.algorithm
    else:
        config.algorithm = config.DEFAULT_ALGORITHM
        log.warn(f"Netika norādīts algoritms; tiks izmantots noklusējums: \"{config.algorithm}\"")
    algo_handler.set_current()
    log.log(f"Tiek izmantots algoritms: \"{config.algorithm}\"")
    
    # Loading
    if args.input != None:
        config.input_file_name = args.input
    else:
        log.log("Dati netiks ielādēti un algoritms būs sava ceļa gājējs")
    
    # Saving
    if args.output != None:
        config.output_file_name = args.output
        log.log(f"Dati tiks saglabāti ar nosaukumu \"{args.output}\"")
    else:
        log.warn("Dati netiks saglabāti")

    # Episodes per hyperparameter
    if args.episodes_per_hyperparameter != None:
        config.episodes_per_hyperparameter = args.episodes_per_hyperparameter
        log.log(f"Tiek izmantota EPH vērtība: {args.episodes_per_hyperparameter}")
    else:
        log.log(f"Tiek izmantota noklusējuma EPH vērtība: {config.episodes_per_hyperparameter}")
    
    # Graphs
    if args.no_graphs:
        config.create_graphs = False
    
    # Verbose mode
    if args.verbose:
        config.is_verbose = True