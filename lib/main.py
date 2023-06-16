import atexit

import saving
import logging
import game_handler
import args

def main():
    args.parse()
    saving.load()
    game_handler.run()
    
    atexit.register(on_exit)

def on_exit():
    saving.save()
    
    logging.log("حَرَام Programma pārtraukta.")

if __name__ == "__main__":
    main()