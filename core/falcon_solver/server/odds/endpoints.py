from pathlib import Path
from fastapi import APIRouter

from falcon_solver.parser.parse_json import parse_json
from falcon_solver.shared.models import EmpireConfiguration, FalconConfiguration
from falcon_solver.solver.solver import Solver

router = APIRouter(tags=["Odds Calculations"], prefix="/odds")


@router.post("", response_model=float)
async def odds(
    empire_config: EmpireConfiguration, falcon_config: FalconConfiguration | None = None
):
    """
    Calculate the odds for an empire plan configuration. Use the default millennium falcon
    config if not supplied.
    """
    if not falcon_config:
        falcon_config = parse_json(
            str(Path.cwd()) + "/falcon_solver/shared/resources/millennium-falcon.json",
            FalconConfiguration,
        )
    solver = Solver(falcon_config=falcon_config, empire_config=empire_config)
    odds = solver.tell_me_the_odds(rounded=True)
    return odds
