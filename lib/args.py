import argparse

import config
import logging
import algo_handler

def parse():
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
        "-v", "--verbose",
        action="store_true",
        help="Rādīt pilnīgi visu izvadi terminālī")
    args = arg_parser.parse_args()

    if not args.no_graphs:
        logging.warn("Grafikus vēl nevar saglabāt!")
    
    # Algorithm selection
    if args.algorithm != None:
        config.algorithm = args.algorithm
        algo_handler.set_current()
    else:
        logging.warn(f"Netika norādīts algoritms; tiks izmantots noklusējums: \"{config.algorithm}\"")
    logging.log(f"Tiek izmantots algoritms: \"{config.algorithm}\"")
    
    # Loading
    if args.input != None:
        config.input_file_name = args.input
    else:
        logging.log("Dati netiks ielādēti un algoritms būs sava ceļa gājējs")
    
    # Saving
    if args.output != None:
        config.output_file_name = args.output
        logging.log(f"Dati tiks saglabāti ar nosaukumu \"{args.output}\"")
    else:
        logging.warn("Dati netiks saglabāti")

    # Episodes per hyperparameter
    if args.episodes_per_hyperparameter != None:
        config.episodes_per_hyperparameter = args.episodes_per_hyperparameter
        logging.log(f"Tiek izmantota EPH vērtība: {args.episodes_per_hyperparameter}")
    else:
        logging.log(f"Tiek izmantota noklusējuma EPH vērtība: {config.episodes_per_hyperparameter}")
    
    # Verbose mode
    if args.verbose:
        config.is_verbose = True