"""
Given a start planet, end planet, autonomy, and time, calculate all possible paths, and return the one with the highest success odds
"""
import logging
from copy import copy
from queue import PriorityQueue

from falcon_solver.parser.parse_json import process_bounty_hunters
from falcon_solver.parser.parse_universe import parse_universe
from falcon_solver.shared.models import (EmpireConfiguration,
                                         FalconConfiguration, PathStep)


class Solver:

    """
    The solver will calculate possible paths, and find a successful path with the best odds.
    """

    def __init__(
        self, falcon_config: FalconConfiguration, empire_config: EmpireConfiguration
    ) -> None:
        self.routes: dict = parse_universe(falcon_config.routes_db)
        self.autonomy = falcon_config.autonomy
        self.start = falcon_config.departure
        self.end = falcon_config.arrival
        self.countdown = empire_config.countdown
        self.bounty_hunters = process_bounty_hunters(empire_config.bounty_hunters)

    def tell_me_the_odds(self, rounded: bool = False) -> float:
        """
        Ask C3PO to tell you the odds, as a percentage
        """
        k = self.get_least_bounty_hunter_captures()
        if k is None:
            return 0
        odds = 1 - Solver.compute_capture_times_formula(k) or 1
        return round(odds, 2) * 100 if rounded else odds * 100


    @staticmethod
    def compute_capture_times_formula(k: int) -> float:
        sum_ = 0
        for i in range(k):
            sum_ += (9**i) / (10 ** (i + 1))
        return sum_
    
    def get_least_bounty_hunter_captures(self) -> int | None:
        """
        Implements a kind of priority queue (a dictionary of bounty hunters found, to possible paths)
        This way we iterate to find successful paths with the least bounty hunter captures first.
        """
        steps: dict[int, list[PathStep]] = {0: []}
        steps[0].append(PathStep(
                autonomy=self.autonomy,
                day=self.countdown,
                route=[self.start],
                seen_bounty_hunters=0
            ))

        smallest_bh_number = 0
        while steps:
            while steps.get(smallest_bh_number):
                current_step = steps[smallest_bh_number].pop()
                if current_step.day < 0:
                    continue
        
                if self.is_successful_path(current_step):
                    logging.info("Found a successful path with %s bounty hunters: %s", current_step.seen_bounty_hunters, current_step.route)
                    return current_step.seen_bounty_hunters
                possible_steps = self.calculate_possible_steps(current_step)
                for step in possible_steps:
                    if step.seen_bounty_hunters not in steps:

                        steps[step.seen_bounty_hunters] = []

                    steps[step.seen_bounty_hunters].append(step)
            logging.debug("Nothing more at steps %s", smallest_bh_number)
            del steps[smallest_bh_number]
            smallest_bh_number += 1
        return None
        

    def calculate_possible_steps(self, step: PathStep) -> list[PathStep]:
        possible = []

        for next_planet, weight in self.routes[step.route[-1]].items():
            logging.debug("We're on day %s. checking if there are any bounty hunters on planet %s on day %s", step.day, next_planet, (self.countdown - step.day) + weight)

            bh = False
            if weight <= step.autonomy and step.day - weight >= 0:
                logging.debug("Setting day from %s to %s", step.day, step.day - weight)
                if next_planet in self.bounty_hunters.get((self.countdown - step.day) + weight, []):
                    logging.debug("Found a bh whilst moving.")
                    bh = True
                updated_route = copy(step.route)
                updated_route.append(next_planet)
                possible.append(
                    PathStep(
                        autonomy=step.autonomy - weight,
                        day=step.day - weight,
                        route=updated_route,
                        seen_bounty_hunters=step.seen_bounty_hunters + 1 if bh else step.seen_bounty_hunters
                    )
                )
        bh = False
        # It's always possible to refuel and go nowhere
        if step.day - 1 > 0:
            if step.route[-1] in self.bounty_hunters.get((self.countdown - step.day) + 1, []):
                logging.debug("Found a bh whilst refueling.")
                bh = True
            updated_route = copy(step.route)
            updated_route.append(step.route[-1])
            possible.append(
                PathStep(
                    autonomy=self.autonomy,
                    day=step.day - 1,
                    route=updated_route,
                    seen_bounty_hunters=step.seen_bounty_hunters + 1 if bh else step.seen_bounty_hunters
                )
            )
        return possible

    def is_successful_path(self, step: PathStep) -> bool:
        return step.route[-1] == self.end
