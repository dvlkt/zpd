# Skripts, kas noņem liekos datu punktus no mācīšanās datiem

import argparse
import json

def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "-i", "--input",
        help="Ceļš uz ievaddatiem"
    )
    arg_parser.add_argument(
        "-o", "--output",
        help="Ceļš uz izvadi"
    )
    arg_parser.add_argument(
        "-m", "--maxpoints",
        type=int,
        help="Maksimālais punktu skaits uz katras ass"
    )
    args = arg_parser.parse_args()

    original_file = open(args.input, "r")
    data = json.loads(original_file.read())

    if len(data["game_data"]["results"]) > args.maxpoints ** 2:
        data["game_data"]["results"] = data["game_data"]["results"][0:args.maxpoints**2]
    
    played_episodes = 0
    for i in data["game_data"]["results"]:
        played_episodes += len(i["scores"])
    data["game_data"]["played_episodes"] = played_episodes
    
    new_file = open(args.output, "w")
    new_file.write(json.dumps(data))
    new_file.close()


if __name__ == "__main__":
    main()