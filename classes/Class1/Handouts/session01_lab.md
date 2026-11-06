# Session 1 Lab: orientation and setup

Code: `sessions/session-01/` (`00_check_setup`, `01_first_call.py`, `02_ai_assistant.py`). Time: about 60 minutes.

## In class

**No-code path (everyone)**

1. Follow the setup guide and the VS Code setup guide: a key in `.env`, the session's `.venv` as interpreter, run `01_first_call.py`.
2. Change `QUESTION` to something from your work. Run it again. Then change `SYSTEM` to "You are a strict lawyer.
   Answer in one sentence." Same question: what changed?
3. In Google AI Studio, paste the same system prompt and question. Compare the two answers.

**Build path (Python)**

1. Run `02_ai_assistant.py` and do its three assistant tasks (explain, change, extend).
2. Read `sessions/common/llm.py` (F12 on `ask` jumps there). Find where the provider is chosen and where the receipt is built.

## Homework

1. **Keys (10 min).** Get both keys working. Run `01_first_call.py` once with `PROVIDER` = `nvidia` and once with
   `gemini`. Save both receipt lines.
2. **Local setup (20 min).** Install Python, Git and VS Code, clone the repo, add your key to
   `.env` at the top folder of the repo and run `./run.sh check` until it says "All set" (setup guide, part 5).
   Sessions 2–3 (Python for GenAI) work best on your laptop. From another language? Skim *Python for programmers* too.
3. **Explore (20 min).** Ask five prompts in AI Studio that you would really use (email, summary, explain a concept,
   plan, code). For each, note one thing that surprised you: good or bad.
4. **Interview question.** Answer in five sentences or fewer:
   *"What's the difference between a model, an API and an app like ChatGPT?"*

Bring your two receipt lines and your five surprises to Session 2.
