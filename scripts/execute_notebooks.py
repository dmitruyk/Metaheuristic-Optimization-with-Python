"""Execute every notebook from a clean kernel. Smoke parameters are already in the notebooks."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache"
os.environ["MPLBACKEND"] = "Agg"
os.environ["MPLCONFIGDIR"] = str(CACHE / "matplotlib")
os.environ["IPYTHONDIR"] = str(CACHE / "ipython")
os.environ["JUPYTER_CONFIG_DIR"] = str(CACHE / "jupyter")
os.environ["XDG_CACHE_HOME"] = str(CACHE)
CACHE.mkdir(exist_ok=True)


def main() -> int:
    failures = 0
    for path in sorted((ROOT / "notebooks").glob("*.ipynb")):
        notebook = nbformat.read(path, as_version=4)
        client = NotebookClient(
            notebook,
            timeout=180,
            kernel_name="python3",
            resources={"metadata": {"path": str(ROOT)}},
        )
        print(f"executing {path.name}")
        try:
            client.execute()
        except Exception as exc:
            failures += 1
            print(f"FAILED {path.name}: {exc}")
            continue
        # Do not write execution output back. Notebooks stay free of hidden state.
    return failures


if __name__ == "__main__":
    sys.exit(main())
