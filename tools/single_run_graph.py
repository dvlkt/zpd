# Specifisku hiperparametru rezultātu grafiku ģenerators

import matplotlib.pyplot as plt
import numpy as np
import json
import argparse

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
        "-a", "--alpha",
        type=float,
        help="Mācīšanās ātruma vērtība"
    )
    arg_parser.add_argument(
        "-g", "--gamma",
        type=float,
        help="Atlaides faktora vērtība"
    )
    arg_parser.add_argument(
        "-n", "--name",
        help="Grafika virsraksts"
    )
    arg_parser.add_argument(
        "-x", "--xlabel",
        help="Horizontālās ass teksts"
    )
    arg_parser.add_argument(
        "-y", "--ylabel",
        help="Vertikālās ass teksts"
    )
    args = arg_parser.parse_args()

    result_file = open(args.input, "r")
    results = json.loads(result_file.read())["game_data"]["results"]

    scores = None
    for r in results:
        if r["hyperparameters"] == [args.alpha, args.gamma]:
            scores = r["scores"]
    if scores == None:
        print("Dotajiem hiperparametriem nav datu!")
        return
    
    fig, ax = plt.subplots()
    ax.plot(np.arange(len(scores)), scores, linewidth=2.5)

    axis_names = ["Epizode", "Rezultāts"]
    if args.xlabel != None:
        ax.set_xlabel(args.xlabel)
    else:
        ax.set_xlabel(axis_names[0])
    if args.ylabel != None:
        ax.set_ylabel(args.ylabel)
    else:
        ax.set_ylabel(axis_names[1])

    plt.title(args.name)

    fig.savefig(args.output)


if __name__ == "__main__":
    main()