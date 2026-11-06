"""Session 1 · Check your setup

Run this first, in class and whenever something stops working. It checks Python, the virtual environment, the
course packages, your keys and one real call, and tells you how to fix whatever is wrong. It never prints a key.
"""
# %%
import importlib
import os
import sys
import time
from pathlib import Path

problems = []


def ok(label, detail=""):
    print(f"  OK    {label}{'  · ' + detail if detail else ''}")


def bad(label, fix):
    print(f"  FIX   {label}\n        → {fix}")
    problems.append(label)


print("Running in folder:", Path.cwd().name, "· Python at", Path(sys.executable).parent.parent.name)

# %% [markdown]
# ## 1 · Python and the virtual environment

# %%
v = sys.version_info
if v >= (3, 10):
    ok("Python version", f"{v.major}.{v.minor}.{v.micro}" + ("" if v >= (3, 12) else " (works; 3.12+ recommended)"))
else:
    bad(f"Python {v.major}.{v.minor} is too old", "install Python 3.12 or newer (setup guide, step 3)")

in_venv = sys.prefix != sys.base_prefix
if in_venv:
    ok("Virtual environment", Path(sys.prefix).name)
else:
    bad("Not inside a virtual environment",
        "use ./run.sh (it creates .venv); VS Code: Python: Select Interpreter -> this session's .venv")

# %% [markdown]
# ## 2 · Course packages

# %%
for name, module in [("openai", "openai"), ("anthropic", "anthropic"), ("python-dotenv", "dotenv"),
                     ("pydantic", "pydantic"), ("ipykernel (VS Code Run Cell)", "ipykernel"),
                     ("course helper llm.py", "llm")]:
    try:
        m = importlib.import_module(module)
        ok(name, getattr(m, "__version__", ""))
    except ImportError:
        bad(f"{name} is not installed", "inside the venv: pip install -r requirements.txt")

# %% [markdown]
# ## 3 · Keys (never printed)

# %%
KEYS = ["NVIDIA_API_KEY", "GEMINI_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY"]
try:
    from dotenv import find_dotenv
    env = find_dotenv(usecwd=True)  # this folder, then its parents: the same search llm.py does
except ImportError:
    env = ""
if env:
    ok(".env file", f"found: {os.path.relpath(env)}")
else:
    bad("No .env file found",
        "copy sessions/session-01/.env.example to .env at the repo root, paste your key")
try:
    import llm  # loads .env on import

    found = [k for k in KEYS if os.getenv(k)]
    for k in found:
        val = os.environ[k].strip()
        looks = not (val.startswith(("'", '"')) or " " in val or len(val) < 20)
        if looks:
            ok(k, f"set · {len(val)} characters")
        else:
            bad(f"{k} looks wrong (quotes, spaces or too short)", "paste the key again: no quotes, no spaces")
    provider = llm.pick()
    ok("Provider in use", provider)
except Exception as e:  # NoKeyError, or llm missing
    provider = None
    bad(f"No usable provider ({type(e).__name__})",
        "add NVIDIA_API_KEY to .env at the repo root, or set PROVIDER=fake to work offline")

# %% [markdown]
# ## 4 · One real call

# %%
if provider == "fake":
    ok("Live call skipped", "PROVIDER=fake: offline mode, canned replies")
elif provider:
    try:
        t = time.time()
        r = llm.ask("Reply with exactly one word: ready", max_tokens=2000)
        ok("Live call", f"{r.provider} · {r.model} · {time.time() - t:.1f}s · said {r.text.strip()[:20]!r}")
    except Exception as e:
        msg = str(e)
        hint = (f"PROVIDER={provider} but {provider.upper()}_API_KEY is missing: add it, or change PROVIDER"
                if type(e).__name__ == "NoKeyError" or "api_key" in msg.lower() else
                "401: the key is wrong or for another provider" if "401" in msg else
                "429: rate limit, wait a minute and run again" if "429" in msg else
                "network: check your internet / proxy, then run again")
        bad(f"Live call failed ({type(e).__name__})", hint)

# %% [markdown]
# ## Result

# %%
print()
if problems:
    print(f"{len(problems)} thing(s) to fix: " + "; ".join(problems))
    print("Fix the first one, then run this check again.")
else:
    print("All set. You're ready for the session.")
