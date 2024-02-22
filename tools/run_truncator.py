# Skripts, kas datos atstāj tikai pirmās N epizodes katram hiperparametram.

import argparse
import json
import numpy

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
        "-n", "--number",
        type=int,
        help="Skaits, cik epizodes atstāt"
    )
    args = arg_parser.parse_args()

    original_file = open(args.input, "r")
    data = json.loads(original_file.read())

    for i in data["game_data"]["results"]:
        if len(i["scores"]) > args.number:
            i["scores"] = i["scores"][:args.number]
            i["avg_score"] = numpy.average(i["scores"])
    
    new_file = open(args.output, "w")
    new_file.write(json.dumps(data))
    new_file.close()

if __name__ == "__main__":
    main()