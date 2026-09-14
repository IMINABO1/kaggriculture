"""Import kaggle_environments without the OpenSpiel registry errors it writes to stderr.

On this Windows build the package's open_spiel env loaders fail to register two poker games and
print the entire game list twice (~330 lines) on every import. The messages come from native
code, so the redirect has to happen at the file-descriptor level, not via sys.stderr.
"""

from __future__ import annotations

import os
import sys


def import_ke():
    if "kaggle_environments" not in sys.modules:
        sys.stderr.flush()
        saved_fd = os.dup(2)
        try:
            with open(os.devnull, "w") as devnull:
                os.dup2(devnull.fileno(), 2)
                import kaggle_environments
        finally:
            os.dup2(saved_fd, 2)
            os.close(saved_fd)
    import kaggle_environments

    return kaggle_environments
