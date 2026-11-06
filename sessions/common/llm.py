"""llm.py: one small helper used by every session in this course.

    from llm import ask, chat, stream, embed, ask_json

    reply = ask("Explain tokens in one sentence.")
    print(reply)                 # the text
    print(reply.usage_line())    # provider · model · tokens in/out · seconds · cost

Which provider? Set PROVIDER (nvidia | gemini | openai | anthropic | fake) in .env (one file at the repo root).
If PROVIDER is not set, the first provider with a key wins, in the order of PROVIDERS below.
PROVIDER=fake needs no key and returns canned replies: the offline tests use it.

NVIDIA, Gemini and OpenAI are all called through the OpenAI SDK (Chat Completions); Anthropic through its own SDK.
Read this file once: it is short on purpose, and every line is something a production app also has to do.
"""
from __future__ import annotations

import base64
import hashlib
import json
import math
import mimetypes
import os
import time
from dataclasses import dataclass, field
from pathlib import Path

try:  # keys come from .env: the session folder's, or the one at the repo root
    from dotenv import find_dotenv, load_dotenv
    load_dotenv(find_dotenv(usecwd=True))  # the .env in the folder you run from (or a parent)
except ImportError:
    pass

TIMEOUT = 180  # seconds: NVIDIA's default model reasons before it answers, so allow plenty

# Checked 2026-10-30. Override any model with e.g. NVIDIA_MODEL=... in .env.
PROVIDERS = {
    "nvidia": {
        "key": "NVIDIA_API_KEY",
        "base_url": "https://integrate.api.nvidia.com/v1",
        "model": "nvidia/nemotron-3.5-lightning-30b-a3b",   # reasoning model: needs a generous max_tokens
        "vision": "nvidia/nemotron-3.5-super-vl-120b-a12b",
        "embed": "nvidia/nemotron-3.5-embed-1b",
    },
    "gemini": {
        "key": "GEMINI_API_KEY",
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "model": "gemini-3.5-flash-lite",
        "vision": "gemini-3.5-flash-lite",
        "embed": "gemini-embedding-2",
    },
    "openai": {
        "key": "OPENAI_API_KEY",
        "base_url": None,
        "model": "gpt-6-luna",
        "vision": "gpt-6-luna",
        "embed": "text-embedding-3-small",
    },
    "anthropic": {
        "key": "ANTHROPIC_API_KEY",
        "model": "claude-haiku-5-5",
        "vision": "claude-haiku-5-5",
        "embed": None,  # Anthropic has no embeddings endpoint
    },
}

# US$ per 1M tokens (input, output). Free tiers show as 0. Prices change; the structure doesn't.
PRICES = {
    "claude-haiku-5-5": (0.10, 0.50),
    "gpt-6-luna": (0.10, 0.50),
    "text-embedding-3-small": (0.02, 0.0),
}


class NoKeyError(RuntimeError):
    pass


# ---------------------------------------------------------------- choosing a provider
def available() -> list[str]:
    """Providers that have a key set right now."""
    return [p for p, c in PROVIDERS.items() if os.getenv(c["key"])]


def pick(provider: str | None = None) -> str:
    provider = (provider or os.getenv("PROVIDER") or "").lower().strip()
    if provider == "fake" or provider in PROVIDERS:
        return provider
    if provider:
        raise ValueError(f"Unknown provider {provider!r}. Use one of: {', '.join(PROVIDERS)}, fake")
    keyed = available()
    if not keyed:
        raise NoKeyError(
            "No API key found. Put NVIDIA_API_KEY=... (or GEMINI_API_KEY=...) in .env at the repo root, "
            "or set PROVIDER=fake to run offline. ./run.sh check says what is missing."
        )
    return keyed[0]


def model_for(provider: str, kind: str = "model") -> str:
    if provider == "fake":
        return f"fake-{kind}"
    default = PROVIDERS[provider][kind]
    env = f"{provider.upper()}_{'MODEL' if kind == 'model' else kind.upper() + '_MODEL'}"
    return os.getenv(env, default)


def _client(provider: str):
    cfg = PROVIDERS[provider]
    key = os.getenv(cfg["key"])
    if not key:
        raise NoKeyError(f"{cfg['key']} is not set. Add it to .env, or choose another PROVIDER.")
    if provider == "anthropic":
        from anthropic import Anthropic
        return Anthropic(api_key=key, timeout=TIMEOUT)
    from openai import OpenAI
    return OpenAI(api_key=key, base_url=cfg["base_url"], timeout=TIMEOUT)


# ---------------------------------------------------------------- the reply
@dataclass
class Reply:
    text: str
    provider: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    stop: str = ""          # why it stopped: "stop"/"end_turn" = finished, "length"/"max_tokens" = cut off
    seconds: float = 0.0
    reasoning: str = ""     # the model's thinking, when the provider returns it separately
    raw: object = field(default=None, repr=False)

    def __str__(self) -> str:
        return self.text

    @property
    def cost(self) -> float:
        p_in, p_out = PRICES.get(self.model, (0.0, 0.0))
        return (self.input_tokens * p_in + self.output_tokens * p_out) / 1_000_000

    @property
    def cut_off(self) -> bool:
        return self.stop in ("length", "max_tokens")

    def usage_line(self) -> str:
        return (f"{self.provider} · {self.model} · {self.input_tokens:,} in / {self.output_tokens:,} out · "
                f"{self.seconds:.1f}s · ${self.cost:.6f}" + (" · CUT OFF" if self.cut_off else ""))


# ---------------------------------------------------------------- images (vision)
def image_part(src: str | bytes | Path) -> dict:
    """A path, URL or raw bytes -> {'mime', 'data' (base64) | 'url'}."""
    if isinstance(src, (bytes, bytearray)):
        return {"mime": "image/png", "data": base64.b64encode(src).decode()}
    s = str(src)
    if s.startswith(("http://", "https://")):
        return {"url": s}
    mime = mimetypes.guess_type(s)[0] or "image/png"
    return {"mime": mime, "data": base64.b64encode(Path(s).read_bytes()).decode()}


def _content(text: str, images, provider: str):
    if not images:
        return text
    parts = []
    for img in map(image_part, images):
        if provider == "anthropic":
            source = ({"type": "url", "url": img["url"]} if "url" in img
                      else {"type": "base64", "media_type": img["mime"], "data": img["data"]})
            parts.append({"type": "image", "source": source})
        else:
            url = img.get("url") or f"data:{img['mime']};base64,{img['data']}"
            parts.append({"type": "image_url", "image_url": {"url": url}})
    parts.append({"type": "text", "text": text})
    return parts


# ---------------------------------------------------------------- calling the model
def chat(messages: list[dict], *, system: str | None = None, provider: str | None = None, model: str | None = None,
         temperature: float | None = None, max_tokens: int = 4000, json_mode: bool = False,
         thinking: bool | None = None, **extra) -> Reply:
    """Send a whole conversation: messages = [{"role": "user"|"assistant", "content": ...}, ...].

    thinking=False switches off the reasoning step of NVIDIA's default model: short answers in ~1 s instead of ~5 s.
    (None = the model's default; other providers ignore it.)"""
    provider = pick(provider)
    if provider == "fake":
        return _fake_reply(messages, json_mode)
    model = model or model_for(provider)
    client = _client(provider)
    t0 = time.time()
    if provider == "anthropic":
        kw = {"system": system} if system else {}
        if temperature is not None:
            kw["temperature"] = temperature
        r = client.messages.create(model=model, max_tokens=max_tokens, messages=messages, **kw, **extra)
        text = "".join(b.text for b in r.content if b.type == "text")
        return Reply(text, provider, model, r.usage.input_tokens, r.usage.output_tokens, r.stop_reason,
                     time.time() - t0, raw=r)
    msgs = ([{"role": "system", "content": system}] if system else []) + messages
    kw = {"temperature": temperature} if temperature is not None else {}
    if json_mode:
        kw["response_format"] = {"type": "json_object"}
    if thinking is not None and provider == "nvidia":
        extra.setdefault("extra_body", {}).setdefault("chat_template_kwargs", {})["enable_thinking"] = thinking
    r = client.chat.completions.create(model=model, messages=msgs, max_tokens=max_tokens, **kw, **extra)
    choice = r.choices[0]
    u = r.usage
    return Reply(choice.message.content or "", provider, model,
                 getattr(u, "prompt_tokens", 0) or 0, getattr(u, "completion_tokens", 0) or 0,
                 choice.finish_reason or "", time.time() - t0,
                 reasoning=getattr(choice.message, "reasoning_content", None) or "", raw=r)


def ask(prompt: str, *, system: str | None = None, images=None, provider: str | None = None, **kw) -> Reply:
    """One question, one answer. images = list of paths/URLs/bytes for vision models."""
    provider = pick(provider)
    if images and "model" not in kw and provider != "fake":
        kw["model"] = model_for(provider, "vision")
    return chat([{"role": "user", "content": _content(prompt, images, provider)}],
                system=system, provider=provider, **kw)


def stream(prompt: str, *, system: str | None = None, provider: str | None = None, model: str | None = None,
           max_tokens: int = 4000, temperature: float | None = None):
    """Yield the answer in small pieces as it is generated (what chat apps do)."""
    provider = pick(provider)
    if provider == "fake":
        yield from _fake_reply([{"role": "user", "content": prompt}]).text.split(" ")
        return
    model = model or model_for(provider)
    client = _client(provider)
    kw = {"temperature": temperature} if temperature is not None else {}
    if provider == "anthropic":
        with client.messages.stream(model=model, max_tokens=max_tokens, system=system or "",
                                    messages=[{"role": "user", "content": prompt}], **kw) as s:
            yield from s.text_stream
        return
    msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}]
    for ev in client.chat.completions.create(model=model, messages=msgs, max_tokens=max_tokens, stream=True, **kw):
        if ev.choices and ev.choices[0].delta.content:
            yield ev.choices[0].delta.content


def ask_json(prompt: str, schema, *, system: str | None = None, retries: int = 2, **kw):
    """Ask for JSON matching a Pydantic model; validate it; on failure, show the model its error and retry."""
    from pydantic import ValidationError
    shape = json.dumps(schema.model_json_schema())
    sys_msg = (system + "\n\n" if system else "") + f"Reply with only a JSON object matching this JSON Schema:\n{shape}"
    messages = [{"role": "user", "content": prompt}]
    # JSON mode makes NVIDIA's reasoning model think until max_tokens and return nothing, so it is off there by default.
    json_mode = kw.pop("json_mode", pick(kw.get("provider")) != "nvidia")
    for attempt in range(retries + 1):
        r = chat(messages, system=sys_msg, json_mode=json_mode, **kw)
        text = r.text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        try:
            return schema.model_validate_json(text)
        except ValidationError as e:
            if attempt == retries:
                raise
            messages += [{"role": "assistant", "content": r.text},
                         {"role": "user", "content": f"That JSON was invalid:\n{e}\nReply with corrected JSON only."}]


# ---------------------------------------------------------------- embeddings
def embed(texts: list[str] | str, *, provider: str | None = None, kind: str = "passage",
          model: str | None = None, batch: int = 64) -> list[list[float]]:
    """Text -> vectors. kind = "query" for search questions, "passage" for documents (NVIDIA uses the difference)."""
    if isinstance(texts, str):
        texts = [texts]
    provider = pick(provider)
    if provider == "fake":
        return [_hash_vector(t) for t in texts]
    if provider == "anthropic":
        keyed = [p for p in available() if PROVIDERS[p]["embed"]]
        if not keyed:
            raise NoKeyError("Anthropic has no embeddings API: add an NVIDIA, Gemini or OpenAI key for embeddings.")
        provider = keyed[0]
    model = model or model_for(provider, "embed")
    client = _client(provider)
    extra = {"extra_body": {"input_type": kind, "truncate": "END"}} if provider == "nvidia" else {}
    out = []
    for i in range(0, len(texts), batch):
        r = client.embeddings.create(model=model, input=texts[i:i + batch], **extra)
        out += [d.embedding for d in sorted(r.data, key=lambda d: d.index)]
    return out


def cosine(a: list[float], b: list[float]) -> float:
    """1.0 = same direction (same meaning), about 0 = unrelated."""
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)) or 1.0)


# ---------------------------------------------------------------- offline stand-ins (PROVIDER=fake)
def _fake_reply(messages: list[dict], json_mode: bool = False) -> Reply:
    last = messages[-1]["content"]
    if isinstance(last, list):
        last = " ".join(p.get("text", "[image]") for p in last if isinstance(p, dict))
    text = "{}" if json_mode else f"[fake reply] You asked: {str(last)[:80]}"
    return Reply(text, "fake", "fake-model", max(1, len(str(messages)) // 4), max(1, len(text) // 4), "stop", 0.0)


def _hash_vector(text: str, dims: int = 256) -> list[float]:
    """Bag-of-words hashing: shared words -> similar vectors. Good enough to test code offline, not meaning."""
    v = [0.0] * dims
    for w in text.lower().split():
        v[int(hashlib.md5(w.strip(".,!?").encode()).hexdigest(), 16) % dims] += 1.0
    return v
