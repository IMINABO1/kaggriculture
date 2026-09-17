"""Build and verify submission.tar.gz.

    uv run python scripts/package.py

Bundles main.py and the agent/ package, then verifies the archive the way Kaggle will use
it: extract to a temp dir, load main.py through kaggle-environments' file loader, check that
the selected callable is really ``agent``, and run a short self-play game from that dir.
"""

from __future__ import annotations

import tarfile
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "submission.tar.gz"
SIZE_LIMIT = 100 * 1024 * 1024


def members() -> list[Path]:
    files = [ROOT / "main.py"]
    files += sorted(p for p in (ROOT / "agent").rglob("*.py") if "__pycache__" not in p.parts)
    files += sorted((ROOT / "agent").glob("*.npz"))  # the clone's weights, when a clone is shipped
    return files


def build() -> None:
    with tarfile.open(ARCHIVE, "w:gz") as tar:
        for path in members():
            tar.add(path, arcname=str(path.relative_to(ROOT)).replace("\\", "/"))
    size = ARCHIVE.stat().st_size
    print(f"built {ARCHIVE.name}: {size / 1024:.1f} KiB, {len(members())} files")
    if size > SIZE_LIMIT:
        raise SystemExit("archive exceeds Kaggle's 100 MiB limit")


def verify() -> None:
    from kenv import import_ke

    make = import_ke().make
    from kaggle_environments.agent import get_last_callable

    with tempfile.TemporaryDirectory() as tmp:
        with tarfile.open(ARCHIVE) as tar:
            tar.extractall(tmp, filter="data")
        main_py = Path(tmp) / "main.py"
        fn = get_last_callable(main_py.read_text(), path=str(main_py))
        if getattr(fn, "__name__", None) != "agent":
            raise SystemExit(
                f"loader would pick {fn!r}, not agent(); fix the binding order in main.py"
            )
        env = make("kaggriculture", configuration={"episodeSteps": 48, "seed": 0}, debug=True)
        env.run([str(main_py), str(main_py)])
        statuses = [str(s.status) for s in env.steps[-1]]
        if statuses != ["DONE", "DONE"]:
            raise SystemExit(f"self-play validation failed: {statuses}")
    print("verified: loader picks agent(), self-play validation DONE/DONE")


if __name__ == "__main__":
    build()
    verify()
