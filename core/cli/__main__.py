"""
Uses argparse to load in JSONs and calculate a percentage score 
"""

import argparse
import fnmatch
import sys

from pydantic import ValidationError

from falcon_solver.parser.parse_json import parse_json
from falcon_solver.shared.models import EmpireConfiguration, FalconConfiguration
from falcon_solver.solver.solver import Solver

# def parse_data()

if __name__ == "__main__":
    odds_parser = argparse.ArgumentParser(
        prog="falcon_solver",
        description="Calculate the odds for given millennium falcon data & empire plans in JSON format.",
    )

    odds_parser.add_argument(
        "-m",
        "--millennium-falcon-data",
        dest="millennium_falcon_data",
        type=str,
        default=None,
        help="The millennium falcon data in JSON format.",
    )
    odds_parser.add_argument(
        "-e",
        "--empire-data",
        dest="empire_data",
        type=str,
        default=None,
        help="The empire plans data in JSON format.",
    )

    args, unknown = odds_parser.parse_known_args()

    parser = argparse.ArgumentParser(parents=[odds_parser], add_help=False)

    if args.millennium_falcon_data is None or args.empire_data is None:
        print("Args must contain valid millennium falcon and empire JSON files.")

    falcon_data_fn = args.millennium_falcon_data
    empire_data_fn = args.empire_data

    if fnmatch.fnmatch(falcon_data_fn, "*.json") and fnmatch.fnmatch(
        empire_data_fn, "*.json"
    ):
        try:
            falcon_config = parse_json(falcon_data_fn, FalconConfiguration)
            empire_config = parse_json(empire_data_fn, EmpireConfiguration)
        except FileNotFoundError:
            print(
                "One of the files could not be found, please make sure they exist in the directory this script is ran from."
            )
            sys.exit()
        except ValidationError:
            print(
                "One of the JSON files have invalid values. Please ensure data types are correct and integers are > 0."
            )
            sys.exit()
        # falcon_config = FalconConfiguration(**json.load(open(data_fn)))
        odds = Solver(falcon_config, empire_config).tell_me_the_odds(rounded=True)
        print(f"Your calculated odds: {odds}%!")
    else:
        print(
            f"One of the data files ({falcon_data_fn} or {empire_data_fn}) were not valid JSON."
        )
