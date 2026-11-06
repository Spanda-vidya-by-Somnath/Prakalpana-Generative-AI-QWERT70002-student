# Session 1: orientation and setup

Your first call to a language model, and how to use an AI assistant on course code.

| File | What it shows |
|---|---|
| `00_check_setup.py` | Checks Python, the venv, packages, your keys (never printed) and one live call, with a fix for anything wrong. Run it first. |
| `01_first_call.py` | One question, one answer, and the receipt: provider, model, tokens in/out, seconds, cost. Change `SYSTEM` and `QUESTION`. |
| `02_ai_assistant.py` | A small summariser to explain, change and extend with an AI assistant. |
| `../common/llm.py` | The course helper used in every session (`ask`, `chat`, `stream`, `ask_json`, `embed`). It is installed into every session's `.venv`. |

## Run

**Local:** from the repo root, with your key in `.env` at the repo root (setup guide):

```bash
./run.sh 01               # menu; sets up .venv the first time
./run.sh 01 01_first_call.py
./run.sh 01 test          # offline, no key
```

Windows (PowerShell, in this folder): `py -m venv .venv`, `.venv\Scripts\Activate.ps1`,
`pip install -r requirements.txt`, then `python <script>.py`.

`sample_outputs/` has real runs on NVIDIA from 2026-10-30.

## Questions to ask

- Why are there more tokens out than in for a three-sentence answer?
- What changed when you swapped the system prompt, and what stayed the same?
- In task 3, how did you check the assistant's change was right?
