# Skripts, kas nosauc hiperparametrus ar labākajiem vidējiem rezultātiem

import argparse
import json

def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "-i", "--input",
        help="Ceļš uz ievaddatiem"
    )
    arg_parser.add_argument(
        "-t", "--top",
        type=int,
        help="Skaits, cik vienumus nosaukt"
    )
    args = arg_parser.parse_args()

    result_file = open(args.input, "r")
    results = json.loads(result_file.read())["game_data"]["results"]

    avg_results = {}
    for r in results:
        avg_results[str(r["hyperparameters"])] = r["avg_score"]
    sorted_results = dict(sorted(avg_results.items(), key=lambda i: i[1], reverse=True)) # Taken from https://realpython.com/sort-python-dictionary/

    for i in enumerate(sorted_results):
        if i[0] < args.top:
            hp = json.loads(i[1])
            print(f"{i[0]+1}. vieta: α = {hp[0]}; γ = {hp[1]}; vidējais rezultāts ir {sorted_results[i[1]]}")


if __name__ == "__main__":
    main()