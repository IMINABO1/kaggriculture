from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
COMMUNITY = DATA / "community"
TOP10 = DATA / "top10"
EPISODE_CACHE = TOP10 / "episodes"
REPLAYS = DATA / "replays"
TRACES = DATA / "traces"
REPORTS = ROOT / "reports" / "top10"
OPPONENTS = ROOT / "opponents"
