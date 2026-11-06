"""coursetest.py: the offline smoke test every session reuses.

    # sessions/session-NN/tests/test_smoke.py
    from coursetest import run_all_scripts
    def test_scripts_run_offline(): run_all_scripts(__file__)

Runs every numbered script (01_*.py, 02_*.py, ...) with PROVIDER=fake, so no key and no network are needed.
"""
import os
import runpy
import sys
from pathlib import Path


def session_dir(test_file: str) -> Path:
    return Path(test_file).resolve().parents[1]


def run_all_scripts(test_file: str, skip: tuple[str, ...] = ()) -> list[str]:
    here = session_dir(test_file)
    scripts = sorted(p for p in here.glob("[0-9][0-9]_*.py") if p.name not in skip)
    assert scripts, f"no numbered scripts in {here}"
    old_cwd, old_env = os.getcwd(), os.environ.get("PROVIDER")
    os.environ["PROVIDER"] = "fake"
    sys.path.insert(0, str(here))
    try:
        os.chdir(here)
        for s in scripts:
            runpy.run_path(str(s), run_name="__main__")
    finally:
        os.chdir(old_cwd)
        sys.path.remove(str(here))
        if old_env is None:
            os.environ.pop("PROVIDER", None)
        else:
            os.environ["PROVIDER"] = old_env
    return [s.name for s in scripts]
