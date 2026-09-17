import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
COMMUNITY = DATA / "community"
# KAGG_WORKSPACE points the study tables (snapshot, teams, history, sample, daily index) at
# another directory, e.g. data/gold for the gold-zone replay pull; replays, traces and the
# episode-listing cache stay shared so nothing is downloaded twice
TOP10 = Path(os.environ.get("KAGG_WORKSPACE", DATA / "top10"))
EPISODE_CACHE = DATA / "top10" / "episodes"
REPLAYS = DATA / "replays"
TRACES = DATA / "traces"
REPORTS = ROOT / "reports" / "top10"
OPPONENTS = ROOT / "opponents"
