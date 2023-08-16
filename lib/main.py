import atexit

import saving
import log
import game_handler
import args

def main():
    args.parse()
    saving.load()
    game_handler.run()
    
    atexit.register(on_exit)

def on_exit():
    saving.save()
    
    log.log("Programma pārtraukta.")

if __name__ == "__main__":
    main()