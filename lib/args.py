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
        "-has", "--hp-adjustment-strategy",
        help="Stratēģija, kā izvēlēties hiperparametrus. Vērtības var būt \"default\", \"random\" vai \"grid\".")
    arg_parser.add_argument(
        "-as", "--autosave-interval",
        type=int,
        help="Epizožu skaits, ik pēc kurām tiek saglabāti dati. Ja netiks norādīts, dati tiks saglabāti tikai procesa apturēšanas mirklī"
    )
    arg_parser.add_argument(
        "-ng", "--no-graphs",
        action="store_true",
        help="Nesaglabāt grafikus")
    arg_parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Rādīt pilnīgi visu izvadi terminālī")
    args = arg_parser.parse_args()
    
    # Port
    if args.port != None:
        config.port = args.port
    else:
        config.port = config.DEFAULT_PORT
        log.warn(f"Netika norādīts ports; tiks izmantots noklusējums: {config.port}")
    log.log(f"Tiek izmantots ports: {config.port}")

    # Algorithm
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
    
    # Hyperparameter adjustment strategy
    if args.hp_adjustment_strategy != None:
        if args.hp_adjustment_strategy in config.VALID_HP_ADJUSTMENT_STRATEGIES:
            config.hp_adjustment_strategy = args.hp_adjustment_strategy
            log.log(f"Tiks izmantota HP izvēles stratēģija: \"{config.hp_adjustment_strategy}\"")
        else:
            config.hp_adjustment_strategy = config.DEFAULT_HP_ADJUSTMENT_STRATEGY
            log.warn(f"Nezināma HP izvēles stratēģija \"{args.hp_adjustment_strategy}\", tiks izmantota noklusējuma vērtība: \"{config.hp_adjustment_strategy}\"")
    else:
        config.hp_adjustment_strategy = config.DEFAULT_HP_ADJUSTMENT_STRATEGY
        log.warn(f"Netika norādīta HP izvēles stratēģija, tiks izmantota noklusējuma vērtība: \"{config.hp_adjustment_strategy}\"")

    # Autosave interval
    if args.autosave_interval != None:
        if args.output == None:
            log.warn(f"Ir norādīts datu saglabāšanas intervāls, bet ne izvadnes ceļš. Nekas netiks saglabāts.")
        else:
            config.autosave_interval = args.autosave_interval
            log.log(f"Dati tiks saglabāti katras {args.autosave_interval} epizodes")
    else:
        if args.output != None:
            log.warn(f"Dati tiks saglabāti tikai procesa apturēšanas mirklī!")
    
    # Graphs
    if args.no_graphs:
        config.create_graphs = False
    
    # Verbose mode
    if args.verbose:
        config.is_verbose = True