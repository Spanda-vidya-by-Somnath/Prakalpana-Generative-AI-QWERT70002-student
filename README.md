# Generative AI: course code

Your course repository. It grows after every class: each session's code, handouts and diagrams are added
here once that session has been taught. Slides and everything else are in your classroom.

## Get it, then keep it up to date

```bash
git clone <this repository's URL>
cd <folder>
git pull            # after every class: the new session appears
```

Work in the files as you like (homework often asks you to change them). Released files don't change later, so
`git pull` won't clash with your edits. If we ever fix a released file, the class announcement will say so.

## Two ways to run a session

**In VS Code on your computer** (setup: `classes/Class1/Handouts/vscode_setup.md`):

```bash
cp sessions/session-01/.env.example .env      # once: one .env at the top folder serves every session; add your key
./run.sh check                                # checks Python, packages, your key and one real call
./run.sh                                      # menu: pick a session, then a script (sets up its .venv the first time)
./run.sh 02 1                                 # or directly: session 2, first script
```

Windows (PowerShell), in a session folder: `py -m venv .venv`, `.venv\Scripts\Activate.ps1`,
`pip install -r requirements.txt`, then `python <script>.py` (the `.env` at the top folder is found from there).

Each session's README says what to run and what to notice. A session with a `data/make_*.py` script creates its
sample images or audio with it: run it once (`.venv/bin/python data/make_samples.py`); `./run.sh` does this for you.

## Layout

- `sessions/session-NN/`: that session's scripts, with its own README.
- `sessions/common/`: the course helper (`llm.py`) and the sample documents every session uses.
- `sessions/capstone/`: the final project, added at the last class.
- `classes/ClassN/Handouts/`: homework, labs and guides (Markdown; the PDFs are in your classroom).
- `classes/ClassN/Assets/`: explainers and diagrams.

Never commit your `.env` or paste API keys into code or chats.
