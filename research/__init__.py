"""Research tooling for the Kaggriculture project.

Importing this package switches stdout/stderr to UTF-8. Team names on the leaderboard include
mathematical-bold and CJK characters, and the default cp1252 console on this Windows machine
raises UnicodeEncodeError on them, which has killed two background runs.
"""

import sys

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")
