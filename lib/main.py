from http.server import HTTPServer
import threading, sys, argparse, atexit, os

import algorithm
import saving
import config
import logging
import game_handler
import args

save_file_name = None

def main():
    global save_file_name

    args.parse()
    saving.load()
    game_handler.run()
    
    atexit.register(on_exit)

def on_exit():
    saving.save()
    
    logging.log("حَرَام Programma pārtraukta.")

if __name__ == "__main__":
    main()