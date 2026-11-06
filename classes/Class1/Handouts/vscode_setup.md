# VS Code setup guide

We write and run all course code in **VS Code** on your own computer. About 20 minutes the first time.
Do the [setup guide](setup_guide.md) first: Python, Git, an API key and the `.env` file.

## 1. Install VS Code and three extensions

1. Download VS Code from [code.visualstudio.com](https://code.visualstudio.com) and install it.
   Windows: tick **Add "Open with Code" action** and **Add to PATH** in the installer.
2. Open VS Code → **File → Open Folder…** → choose the course repository folder (the one with `run.sh` in it).
   Answer **Yes, I trust the authors**.
3. A pop-up offers the **recommended extensions** for this folder: click **Install**. If you missed it, open the
   Extensions view (`Ctrl+Shift+X`, Mac `Cmd+Shift+X`) and install:

| Extension | Publisher | What it does for us |
|---|---|---|
| **Python** | Microsoft | Runs `.py` files, picks the virtual environment |
| **Pylance** | Microsoft | Explains code on hover, catches typos as you type |
| **Jupyter** | Microsoft | Runs one `# %%` cell at a time (the **Run Cell** links) |

The course folder already contains `.vscode/settings.json`, so scripts run from their own folder and clutter
(`__pycache__`) stays hidden. You don't need to change any setting.

## 2. Open the terminal and set up a session

**Terminal → New Terminal** (`` Ctrl+` ``) opens a terminal in the course folder.

| | macOS / Linux | Windows (PowerShell) |
|---|---|---|
| Set up and check | `./run.sh check` | `cd sessions\session-01` · `py -m venv .venv` · `.venv\Scripts\Activate.ps1` · `pip install -r requirements.txt` · `python 00_check_setup.py` |
| Each new session | `./run.sh NN` (creates that session's `.venv` the first time) | the same four commands in `sessions\session-NN` |

Every session folder has its own `.venv` (its own packages). Your key lives once, in `.env` at the top folder.

## 3. Pick the session's Python (the interpreter)

VS Code must use the session's `.venv`, or imports fail with `ModuleNotFoundError`.

1. Open any `.py` file of the session, for example `sessions/session-01/01_first_call.py`.
2. `Ctrl+Shift+P` (Mac `Cmd+Shift+P`) → **Python: Select Interpreter** → choose
   `.venv` in `sessions/session-01` (shown as `Python 3.x ('.venv': venv) ./sessions/session-01/.venv/...`).
3. The bottom-right status bar now shows that `.venv`. **Repeat this when you move to a new session.**

## 4. Run code: a whole file, or one cell

| You want to | Do this |
|---|---|
| Run the whole script | **▶ Run Python File** (top right of the editor), or in the terminal `./run.sh 01 01_first_call.py` |
| Run one cell | Click **Run Cell** above a `# %%` line. Results appear in the **Interactive** window on the right |
| Change a value and try again | Edit a line marked `# change me`, save, run again (cells: run that cell again) |
| Run all cells | **Run All** above the first cell |
| Offline, no key | `./run.sh -f 01 01_first_call.py`, or put `PROVIDER=fake` in `.env` |

The first **Run Cell** may ask to install or select a kernel: choose the session's `.venv` (it already contains
`ipykernel`). Cells keep their results in memory, so run them top to bottom the first time.

## 5. The AI assistant

Install an assistant extension (for example **GitHub Copilot Chat**, free tier available, or another of your
choice). Select some code, then ask in its chat: *"Explain this line by line for someone new to Python."*
The assistant writes; **you** run it and check it. **Never** paste your API key into the chat.

## 6. When something goes wrong

| You see | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'llm'` (or `openai`, `fastapi`...) | Wrong interpreter: step 3. Or the session isn't set up yet: `./run.sh NN` |
| `FileNotFoundError: data/...` | The script ran from the wrong folder: use **Run Python File** or `./run.sh` (both run inside the session folder) |
| No **Run Cell** links | Jupyter extension missing (step 1), or the file isn't a `.py` |
| "Select a kernel" keeps appearing | Pick the session's `.venv`; if it isn't listed, run `./run.sh NN` first |
| `NoKeyError` / `401` | `.env` missing at the top folder, or key pasted with quotes or spaces: `./run.sh check` says which |
| PowerShell: "running scripts is disabled" | Once: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |

Shortcuts worth learning: `Ctrl+P` open a file by name · `Ctrl+Shift+P` any command · `` Ctrl+` `` terminal ·
`Ctrl+/` comment a line · `F12` jump to where a function is defined (try it on `ask`).
