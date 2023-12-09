# Skripts, kas pārvērš mācīšanās datus no vecā formāta uz pašreizējo

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
    args = arg_parser.parse_args()

    original_file = open(args.input, "r")
    data = json.loads(original_file.read())

    played_episodes = 0
    for i in data:
        i["hyperparameters"] = list(i["hyperparameters"].values()) # Replace the hyperparameter object with an array
        played_episodes += len(i["scores"])
    
    new_data = {
        "q_table": {},
        "hyperparameters": {
            "learning_rate": 0,
            "discount_factor": 0,
            "grid": {
                "step": 0,
                "pos": [0, 0],
                "used": []
            }
        },
        "game_data": {
            "played_episodes": played_episodes,
            "results": data
        }
    }

    new_file = open(args.output, "w")
    new_file.write(json.dumps(new_data))
    new_file.close()


if __name__ == "__main__":
    main()