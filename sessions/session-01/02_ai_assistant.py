"""Session 1 · Working with an AI assistant on course code

In this course you are allowed, and encouraged, to use an AI assistant to read and change the code.
In VS Code, use the assistant chat (for example Copilot Chat): select code, then ask about it.
Below is a small working tool. Run it, then use the assistant for the three tasks under it.
"""
# %%
from llm import ask

TEXT = "Open 9 am weekdays, 10 am Saturdays, closed Sundays. Returns within 30 days with a receipt; no gift cards."  # change me
STYLE = "three bullet points"  # change me


def summarise(text: str, style: str) -> str:
    """Ask the model to summarise `text` in the given style and return just the summary."""
    prompt = f"Summarise the text below as {style}. Use only facts from the text.\n\nTEXT:\n{text}"
    return ask(prompt, temperature=0.2).text


print(summarise(TEXT, STYLE))

# %% [markdown]
# ## Your three tasks (use the assistant, then run the cell again)
# 1. **Explain:** ask the assistant "Explain this cell line by line for someone new to Python."
#    Check its answer against what you see when you run it.
# 2. **Change:** ask it to add a new style, "a question a customer might ask", to the `STYLE` list. Run it.
# 3. **Extend:** ask it to make `summarise` also print how many tokens the call used (hint: `ask` returns a reply
#    with `.input_tokens` and `.output_tokens`). Run it, and read the change before you trust it.
#
# Rule of thumb: the assistant writes, **you** run and check. If you can't say what a line does, ask it.
