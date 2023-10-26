# Grafiku formatētājs (tikai 2 hiperparametru grafikiem)

import matplotlib.pyplot as plt
import numpy as np
import json
import os
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
        "-t", "--type",
        help="Grafika veids. \'avg\', \'best\', \'last\' vai \'diff\'"
    )
    arg_parser.add_argument(
        "-n", "--name",
        help="Grafika virsraksts"
    )
    arg_parser.add_argument(
        "-x", "--x-label",
        help="Horizontālās ass teksts"
    )
    arg_parser.add_argument(
        "-y", "--y-label",
        help="Vertikālās ass teksts"
    )
    arg_parser.add_argument(
        "-l", "--levels",
        type=int,
        help="Līmeņu skaits"
    )
    arg_parser.add_argument(
        "-f", "--fill",
        action="store_true",
        help="Aizpildīt visu grafiku, nevis zīmēt kontūrlīnijas"
    )
    arg_parser.add_argument(
        "-p", "--points",
        action="store_true",
        help="Parādīt datu punktus grafikā"
    )
    arg_parser.add_argument(
        "-h", "--hypothesis",
        action="store_true",
        help="Parādīt hipotēzē veikto paredzējumu kā sarkanu punktu"
    )
    args = arg_parser.parse_args()

    hp1_values = []
    hp2_values = []
    scores = []

    result_file = open(args.input, "r")
    results = json.loads(result_file.read())

    for r in results:
        curr_hp = list(r["hyperparameters"].values())
        hp1_values.append(curr_hp[0])
        hp2_values.append(curr_hp[1])

        if args.type == "avg":
            scores.append(r["avg_score"])
        elif args.type == "best":
            scores.append(np.max(r["scores"]))
        elif args.type == "last":
            scores.append(r["scores"][-1])
        elif args.type == "diff":
            scores.append(r["scores"][-1] - r["scores"][0])

    fig, ax = plt.subplots()

    if args.points:
        ax.plot(hp1_values, hp2_values, "x", markersize=1, color="grey")

    if args.hypothesis:
        ax.plot(0.2, 1, "ro")
        
    levels = np.linspace(np.min(scores), np.max(scores), args.levels)

    if not args.fill:
        ax.tricontour(hp1_values, hp2_values, scores, levels=levels)
    else:
        ax.tricontourf(hp1_values, hp2_values, scores, levels=levels)

    hp_names = list(r["hyperparameters"].keys())
    if args.x-label != None:
        ax.set_xlabel(args.x-label)
    else:
        ax.set_xlabel(hp_names[0])
    if args.y-label != None:
        ax.set_ylabel(args.y-label)
    else:
        ax.set_ylabel(hp_names[1])

    plt.title(args.name)

    fig.savefig(args.output)


if __name__ == "__main__":
    main()