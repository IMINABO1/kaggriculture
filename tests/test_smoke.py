from pathlib import Path

from kaggle_environments import make
from kaggle_environments.agent import get_last_callable

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "main.py"


def run(a, b, steps, seed=0):
    env = make("kaggriculture", configuration={"episodeSteps": steps, "seed": seed}, debug=True)
    env.run([a, b])
    return env.steps[-1]


def test_loader_picks_agent_as_last_callable():
    fn = get_last_callable(MAIN.read_text(), path=str(MAIN))
    assert fn.__name__ == "agent"


def test_selfplay_validation_finishes():
    final = run(str(MAIN), str(MAIN), steps=72)
    assert [str(s.status) for s in final] == ["DONE", "DONE"]


def test_full_season_vs_pass_makes_money():
    final = run(str(MAIN), "pass", steps=720)
    assert str(final[0].status) == "DONE"
    assert final[0].reward > 3000
