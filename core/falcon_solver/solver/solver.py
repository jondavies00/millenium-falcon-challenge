"""
Define the Solver for the backend (C3PO)
"""

import logging
from copy import copy

from falcon_solver.parser.parse_json import process_bounty_hunters
from falcon_solver.parser.parse_universe import parse_universe
from falcon_solver.shared.models import (
    EmpireConfiguration,
    FalconConfiguration,
    PathStep,
)


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
        Compute the odds calculation if there is a successful path.
        """
        k = self._get_least_bounty_hunter_captures()
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

    def _get_least_bounty_hunter_captures(self) -> int | None:
        """
        Implements a kind of priority queue (a dictionary of bounty hunters found, to possible paths)
        This way we iterate to find successful paths with the least bounty hunter captures first.
        """
        steps: dict[int, list[PathStep]] = {0: []}
        steps[0].append(
            PathStep(
                autonomy=self.autonomy,
                day=self.countdown,
                route=[self.start],
                seen_bounty_hunters=0,
            )
        )

        smallest_bh_number = 0
        while steps:
            while steps.get(smallest_bh_number):
                current_step = steps[smallest_bh_number].pop()
                if current_step.day < 0:
                    continue

                if self._is_successful_path(current_step):
                    logging.info(
                        "Found a successful path of length %s with %s bounty hunters.",
                        len(current_step.route),
                        current_step.seen_bounty_hunters,
                    )
                    return current_step.seen_bounty_hunters
                possible_steps = self._calculate_possible_steps(current_step)
                for step in possible_steps:
                    if step.seen_bounty_hunters not in steps:

                        steps[step.seen_bounty_hunters] = []

                    steps[step.seen_bounty_hunters].append(step)
            logging.debug("Nothing more at steps %s", smallest_bh_number)
            del steps[smallest_bh_number]
            smallest_bh_number += 1
        return None

    def _calculate_possible_steps(self, step: PathStep) -> list[PathStep]:
        """
        Calculate the possible steps from the current step (step).
        """
        possible = self._calculate_reachable_planet_steps(step)
        if step.day - 1 > 0:
            possible.append(self._calculate_refuel_step(step))

        return possible

    def _calculate_reachable_planet_steps(
        self, current_step: PathStep
    ) -> list[PathStep]:
        possible_steps = []
        for next_planet, weight in self.routes[current_step.route[-1]].items():
            logging.debug(
                "We're on day %s. checking if there are any bounty hunters on planet %s on day %s",
                current_step.day,
                next_planet,
                (self.countdown - current_step.day) + weight,
            )

            bounty_hunter = False
            if weight <= current_step.autonomy and current_step.day - weight >= 0:
                logging.debug(
                    "Setting day from %s to %s",
                    current_step.day,
                    current_step.day - weight,
                )
                logging.debug(
                    "Checking %s with index %s",
                    self.bounty_hunters,
                    (self.countdown - current_step.day) + weight,
                )
                if next_planet in self.bounty_hunters.get(
                    (self.countdown - current_step.day) + weight, []
                ):
                    logging.debug("Found a bounty hunter whilst moving!")
                    bounty_hunter = True
                updated_route = copy(current_step.route)
                updated_route.append(next_planet)
                possible_steps.append(
                    PathStep(
                        autonomy=current_step.autonomy - weight,
                        day=current_step.day - weight,
                        route=updated_route,
                        seen_bounty_hunters=(
                            current_step.seen_bounty_hunters + 1
                            if bounty_hunter
                            else current_step.seen_bounty_hunters
                        ),
                    )
                )
        return possible_steps

    def _calculate_refuel_step(self, current_step: PathStep) -> PathStep:
        # Refueling is always possible (if we're not on day 0)
        bounty_hunter = False
        if current_step.route[-1] in self.bounty_hunters.get(
            (self.countdown - current_step.day) + 1, []
        ):
            logging.debug("Found a bounty hunter whilst refueling.")
            bounty_hunter = True
        updated_route = copy(current_step.route)
        updated_route.append(current_step.route[-1])
        return PathStep(
            autonomy=self.autonomy,
            day=current_step.day - 1,
            route=updated_route,
            seen_bounty_hunters=(
                current_step.seen_bounty_hunters + 1
                if bounty_hunter
                else current_step.seen_bounty_hunters
            ),
        )

    def _is_successful_path(self, step: PathStep) -> bool:
        return step.route[-1] == self.end
