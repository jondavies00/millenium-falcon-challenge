"""
Given a start planet, end planet, autonomy, and time, calculate all possible paths, and return the one with the highest success odds
"""

from copy import copy
import logging
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
        self.bounty_hunters = empire_config.bounty_hunters

    def tell_me_the_odds(self):
        """
        Ask C3PO to tell you the odds
        """
        self.calculate_odds(self.get_successful_paths())

    def calculate_odds(self, successful_paths: list[PathStep]):
        for successful_path in successful_paths:
            route = successful_path.route
            # For each route we can check the current day, and if there are bounty hunters
            # Alternatively, we could store our solutions as a different data structure? Linked list

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
            if self.successful_path(current_step):
                successful_paths.append(current_step)
                continue

            possible_steps = self.calculate_possible_steps(current_step)
            steps.extend(possible_steps)
        logging.info("total steps: %s", i)
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

    def successful_path(self, step: PathStep) -> bool:
        return step.route[-1] == self.end
