# Hiperparametru grafiku ģenerators

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
        "-t", "--type",
        help="Grafika veids. \'avg\', \'best\', \'last\' vai \'diff\'"
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
        "-hyp", "--hypothesis",
        action="store_true",
        help="Parādīt hipotēzē veikto paredzējumu kā sarkanu punktu"
    )
    arg_parser.add_argument(
        "-val", "--values",
        action="store_true",
        help="Parādīt blakus punktu vērtības"
    )
    args = arg_parser.parse_args()

    hp1_values = []
    hp2_values = []
    scores = []

    result_file = open(args.input, "r")
    results = json.loads(result_file.read())["game_data"]["results"]

    for r in results:
        hp1_values.append(r["hyperparameters"][0])
        hp2_values.append(r["hyperparameters"][1])

        if args.type == "avg":
            scores.append(r["avg_score"])
        elif args.type == "best":
            scores.append(np.max(r["scores"]))
        elif args.type == "last":
            scores.append(r["scores"][-1])
        elif args.type == "diff":
            scores.append(r["scores"][-1] - r["scores"][0])

    fig, axs = plt.subplots(1, 2 if args.values else 1, figsize=(10, 5))

    cax = axs
    if args.values:
        cax = axs[0]
        vax = axs[1]

    cax.set_aspect("equal", "box")
    if args.values:
        vax.set_aspect("equal", "box")
        vax.set_xlim(-0.05, 1.05)
        vax.set_ylim(-0.05, 1.05)

    if args.points:
        cax.plot(hp1_values, hp2_values, "x", markersize=1, color="grey")

    if args.hypothesis:
        cax.plot(0.3, 1, "ro")
    
    levels = np.linspace(np.min(scores), np.max(scores), args.levels)

    if not args.fill:
        cax.tricontour(hp1_values, hp2_values, scores, levels=levels)
    else:
        cax.tricontourf(hp1_values, hp2_values, scores, levels=levels)
    
    if args.values:
        for i in range(len(scores)):
            vax.annotate(str(round(scores[i], 1)), xy=(hp1_values[i], hp2_values[i]), fontsize=8, xytext=(hp1_values[i]-0.03, hp2_values[i]-0.02))

    hp_names = ["Mācīšanās ātrums", "Atlaides faktors"]
    if args.xlabel != None:
        cax.set_xlabel(args.xlabel)
        if args.values:
            vax.set_xlabel(args.xlabel)
    else:
        cax.set_xlabel(hp_names[0])
        if args.values:
            vax.set_xlabel(hp_names[0])
    if args.ylabel != None:
        cax.set_ylabel(args.ylabel)
        if args.values:
            vax.set_ylabel(args.ylabel)
    else:
        cax.set_ylabel(hp_names[1])
        if args.values:
            vax.set_ylabel(hp_names[1])

    plt.subplots_adjust(wspace=0.3)
    
    plt.title(args.name)

    fig.savefig(args.output)


if __name__ == "__main__":
    main()