# Setup guide

About 30 minutes. We work locally in **VS Code**: Python, Git, VS Code and one API key. Then the setup check
turns green and you're ready.

## 1. Get two free API keys

| Provider | Where | Notes |
|---|---|---|
| **NVIDIA** (course default) | [build.nvidia.com](https://build.nvidia.com) → sign in → any model → "Get API Key" | Starts with `nvapi-`. Free tier; enough for the whole course. |
| **Gemini** (second choice) | [aistudio.google.com](https://aistudio.google.com) → "Get API key" | Free tier with your Google account. Also gives you the AI Studio playground for the No-code path. |
| OpenAI / Anthropic (optional) | platform.openai.com · console.anthropic.com | Paid; a few dollars of credit is plenty. Never required. |

**A key is a password that spends money.** Never paste it into code, a chat, a screenshot or GitHub.

## 2. Install Python, Git and VS Code, then get the course

**Install:** Python 3.12+ (3.14 recommended; 3.10 works), Git, and VS Code with the Microsoft **Python** extension.

| | macOS / Linux | Windows (PowerShell) |
|---|---|---|
| Python + Git | `brew install python@3.14 git` · Ubuntu: `sudo apt install python3-venv git` | `py install 3.14` · `winget install Git.Git` |
| Check | `python3 --version` | `py --version` |

**Your key, once:** one `.env` file at the top folder of the repository serves every session.

```bash
git clone <course repo URL> && cd <repo>
cp sessions/session-01/.env.example .env      # paste NVIDIA_API_KEY=nvapi-... (no quotes, no spaces)
./run.sh check                                # first run creates sessions/session-01/.venv (about a minute)
./run.sh                                      # afterwards: a menu of sessions and scripts
```

**Windows** (no `run.sh`): `copy sessions\session-01\.env.example .env`, then in each session folder you use:
`py -3.14 -m venv .venv`, `.venv\Scripts\Activate.ps1`, `pip install -r requirements.txt`, then `python <script>.py`
(for example `python 00_check_setup.py`). "running scripts is disabled"? Run once:
`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`.

## 3. VS Code

Open the course folder in VS Code, install the three recommended extensions, pick the session's `.venv` as the
interpreter, and run a script with **▶ Run Python File** or a single cell with **Run Cell**. Step by step: the [VS Code setup guide](vscode_setup.md).

## 4. The setup check

`00_check_setup.py` (`./run.sh check`) checks Python, the virtual environment, the course packages, your keys (it never
prints them) and one real call, and says how to fix anything wrong. Run it until it says **All set**, and again at the
start of any session where something stops working. A working first call prints a receipt like:

```
nvidia · nvidia/nemotron-3.5-lightning-30b-a3b · 41 in / 490 out · 4.9s · $0.000000
```

## 5. When something goes wrong

| Problem | Fix |
|---|---|
| `No .env file found` / `NoKeyError` | `.env` belongs in the top folder of the repo, with `NVIDIA_API_KEY=nvapi-...` (no quotes, no spaces) |
| `ModuleNotFoundError` | VS Code is using the wrong Python: **Python: Select Interpreter** → the session's `.venv` |
| `401` / `Unauthorized` | Key copied with a space or a missing character, or a key for another provider. Create a new key. |
| `429` / rate limit | Free tiers limit calls per minute. Wait a minute, or switch `PROVIDER`. |
| Empty answer, stopped because `length` | The default NVIDIA model "thinks" first. Keep `max_tokens` large (the course default is 4000). |
| No key at all yet | Put `PROVIDER=fake` in `.env`: everything runs offline with canned replies |
