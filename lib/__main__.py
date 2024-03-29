import atexit
import argparse

import saving
import log
import server
import config

def main():
    arg_parser = argparse.ArgumentParser(
        prog="ZPD",
        description="Hiperparametru ietekme uz Q mācīšanos videospēļu vidē. Zinātniskās pētniecības darbs informātikas/programmēšanas sekcijā.",
        epilog="Darba autori: Dāvis Lektauers un Kazimirs Kārlis Brakovskis. Darba vadītāja: Mg.sr.soc. Agnese Kramēna-Juzova")
    
    arg_parser.add_argument(
        "-p", "--port",
        type=int,
        help="Ports, ko izmantot (atkarīgs no spēles)")
    
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
        "-as", "--autosave-interval",
        type=int,
        help="Epizožu skaits, ik pēc kurām tiek saglabāti dati. Ja netiks norādīts, dati tiks saglabāti tikai procesa apturēšanas mirklī")
    
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
        log.log(f"Tiek izmantots ports: {config.port}")
    else:
        log.error(f"Netika norādīts ports!")
        return
    
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
    
    saving.load()
    server.run()
    
    atexit.register(on_exit)

def on_exit():
    saving.save()
    
    log.log("Programma pārtraukta.")

if __name__ == "__main__":
    main()