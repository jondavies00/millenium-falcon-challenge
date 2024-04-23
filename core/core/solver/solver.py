"""
Given a start planet, end planet, autonomy, and time, calculate all possible paths, and return the one with the highest success odds
"""

from copy import copy
import logging
from core.parser.parse_json import process_bounty_hunters
from core.parser.parse_universe import parse_universe
from core.shared.models import (
    EmpireConfiguration,
    FalconConfiguration,
    PathStep,
)


class Solver:

    def __init__(
        self, falcon_config: FalconConfiguration, empire_config: EmpireConfiguration
    ) -> None:
        self.routes: dict = parse_universe(falcon_config.routes_db)
        logging.info("From tat: %s", self.routes["Tatooine"])
        self.autonomy = falcon_config.autonomy
        self.start = falcon_config.departure
        self.end = falcon_config.arrival
        self.countdown = empire_config.countdown
        self.bounty_hunters = process_bounty_hunters(empire_config.bounty_hunters)

    def tell_me_the_odds(self) -> int:
        """
        Ask C3PO to tell you the odds
        """
        return round(self.calculate_odds(self.get_successful_paths()), 2) * 100

    def calculate_odds(self, successful_paths: list[PathStep]) -> float:
        if not successful_paths:
            return 0
        logging.info("There are %s successful paths", len(successful_paths))
        # logging.info(successful_paths)

        smallest_k = None

        for successful_path in successful_paths:
            route = successful_path.route
            day = 0

            k = 0

            if self.start in self.bounty_hunters.get(day, []):
                k += 1
            prev_planet = self.start
            for planet in route[1:]:
                if planet not in self.routes[prev_planet]:
                    day += 1
                    if (
                        hunters_on_planets := self.bounty_hunters.get(day)
                    ) and planet in hunters_on_planets:
                        k += 1
                    continue
                day += self.routes[prev_planet][planet]
                if (
                    hunters_on_planets := self.bounty_hunters.get(day)
                ) and planet in hunters_on_planets:
                    k += 1
                prev_planet = planet
            logging.debug(
                "k was %s for path %s",
                k,
                successful_path,
            )
            if k == 0:
                return 1
            if smallest_k is None:
                smallest_k = k
            else:
                smallest_k = min(k, smallest_k)

        return 1 - Solver.compute_capture_times_formula(smallest_k) or 1

    @staticmethod
    def compute_capture_times_formula(k: int) -> float:
        sum_ = 0
        for i in range(k):
            sum_ += (9**i) / (10 ** (i + 1))
        return sum_

    def get_successful_paths(self):
        steps = [
            PathStep(
                autonomy=self.autonomy,
                day=self.countdown,
                route=[self.start],
            )
        ]
        successful_paths = []
        i = 0
        while steps:
            i += 1
            current_step = steps.pop(0)
            if current_step.day < 0:
                continue
            if self.is_successful_path(current_step):
                successful_paths.append(current_step)
                continue

            possible_steps = self.calculate_possible_steps(current_step)
            steps.extend(possible_steps)
        logging.info("Total steps: %s", i)
        return successful_paths

    def calculate_possible_steps(self, step: PathStep) -> list[PathStep]:
        possible = []
        for next_planet, weight in self.routes[step.route[-1]].items():
            if weight <= step.autonomy:
                updated_route = copy(step.route)
                updated_route.append(next_planet)
                possible.append(
                    PathStep(
                        autonomy=step.autonomy - weight,
                        day=step.day - weight,
                        route=updated_route,
                    )
                )

        # It's always possible to refuel and go nowhere
        if step.day - 1 > 0:
            updated_route = copy(step.route)
            updated_route.append(step.route[-1])
            possible.append(
                PathStep(
                    autonomy=self.autonomy,
                    day=step.day - 1,
                    route=updated_route,
                )
            )
        return possible

    def is_successful_path(self, step: PathStep) -> bool:
        return step.route[-1] == self.end
