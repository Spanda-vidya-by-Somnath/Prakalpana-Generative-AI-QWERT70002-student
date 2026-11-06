"""Session 1 · Your first call to a language model

One question in, one answer out, and the receipt: which model answered, how many tokens it read and wrote,
how long it took and what it cost. Change the question and the system prompt in the form, then run the cell again.
"""
# %%
from llm import ask, available, pick

print("Keys found for:", available() or "none")
print("Using provider:", pick())

# %% [markdown]
# ## Ask something
# The **system prompt** sets who the model is and how it should answer. The **question** is what you ask.
# Try: a question about your own work, then the same question with a different system prompt.

# %%
SYSTEM = "You are a friendly teacher. Answer in at most three short sentences."  # change me
QUESTION = "What is a large language model, in plain words?"  # change me

reply = ask(QUESTION, system=SYSTEM)
print(reply.text)

# %% [markdown]
# ## Read the receipt
# Every call reports tokens in (what the model read) and tokens out (what it wrote). You pay for both.
# NVIDIA's and Gemini's free tiers show $0, but the tokens are still counted.

# %%
print(reply.usage_line())
print("Stopped because:", reply.stop)
if reply.reasoning:
    print(f"The model also 'thought' before answering ({len(reply.reasoning)} characters of reasoning, not shown).")
