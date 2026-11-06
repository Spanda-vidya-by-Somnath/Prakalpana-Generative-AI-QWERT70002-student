# Versions and models

Checked **2026-10-30** (live API calls on NVIDIA; other providers from docs). Python used for testing: 3.14.6 (course minimum 3.10).

## Shared packages (`sessions/common/pyproject.toml`)

| Package | Version |
|---|---|
| `openai` | 3.41.0 (also used for NVIDIA and Gemini, OpenAI-compatible endpoints) |
| `anthropic` | 2.3.0 |
| `python-dotenv` | 1.2.4 |
| `pydantic` | 2.14.1 |
| `pytest` (tests only) | 9.0.1 |

Session-specific packages are pinned in each `sessions/session-NN/requirements.txt` and listed in that session's README.

## Default models (`sessions/common/llm.py`)

| Provider | Text | Vision | Embeddings | Tested live |
|---|---|---|---|---|
| **NVIDIA** (default) | `nvidia/nemotron-3.5-lightning-30b-a3b` (reasoning: keep `max_tokens` ≥ 2000, timeout ≥ 120 s) | `nvidia/nemotron-3.5-super-vl-120b-a12b` | `nvidia/nemotron-3.5-embed-1b` (2048 dims, `input_type` query/passage) | Yes, 2026-10-30 |
| Gemini | `gemini-3.5-flash-lite` | same | `gemini-embedding-2` | **Not yet** (no key on the build machine) |
| OpenAI | `gpt-6-luna` | same | `text-embedding-3-small` | No (paid, optional) |
| Anthropic | `claude-haiku-5-5` | same | none | No (paid, optional) |

Other NVIDIA endpoints used: image generation `black-forest-labs/flux.1-dev` at `https://ai.api.nvidia.com/v1/genai/` (steps ≥ 5; ~4 s per image, tested 2026-10-30);
safety models `nvidia/nemotron-3.5-content-safety`, `meta/llama-guard-4-12b`.

Override any default with `NVIDIA_MODEL`, `GEMINI_MODEL`, `NVIDIA_VISION_MODEL`, `NVIDIA_EMBED_MODEL`, etc.

## Notes from the build (2026-10-30, all live on NVIDIA unless stated)

- **Reasoning off:** `llm.chat(..., thinking=False)` (sends `chat_template_kwargs={"enable_thinking": False}`) makes short answers ~0.7 s
  instead of ~5 s. Used for batch runs (S7, S8) and as the "cheap tier" in S22 routing.
- **JSON mode + reasoning = empty reply** on NVIDIA's default model (it thinks until `max_tokens`). `llm.ask_json` therefore
  skips JSON mode on NVIDIA and relies on the schema prompt and the repair loop.
- **Logprobs:** returned (`logprobs`, `top_logprobs`). With reasoning on, the first tokens belong to the thinking (S4 skips to `</think>`).
- **Model list caveats:** `nvidia/nemotron-3.5-bolt-e4b` is listed but timed out twice; `google/gemma-3-*`, `mistral-7b`, `mistral-nemo-12b` returned 404.
- **Safety models (S19):** `nvidia/nemotron-3.5-content-safety` replies in plain text (`User Safety: safe`, `Response Safety: unsafe`);
  `meta/llama-guard-4-12b` replies `unsafe\nS1`.
- **Speech (S18), NVIDIA Riva cloud over gRPC** (`nvidia-riva-client`, `grpc.nvcf.nvidia.com:443`, function ids in `sessions/session-18/speech.py`):
  ASR Parakeet 1.1b and Whisper large-v3 work; TTS Magpie multilingual works; Parakeet 0.6b refuses file transcription.
  `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` also transcribes `audio_url` input (~20 s).
- **Images (S17):** FLUX.1-dev 4–10 s quiet, 70–150 s when the shared tier is busy; same seed = identical image.
  The FLUX Kontext edit endpoint returned 422 (preset examples only), so image editing is No-code only.
- **Frameworks (S20):** langchain-core 1.7.3, langchain-nvidia-ai-endpoints 1.5.0, llama-index-core 0.14.25, llama-index-embeddings-nvidia 0.6.0.
  `llama-index-llms-nvidia` conflicts with `openai==3.41.0` (needs `openai<3`); S20 uses a 20-line adapter over `llm.ask` instead.
- **Vector stores (S10):** chromadb 1.5.9 (always pass our own vectors; it still installs `onnxruntime` but we never call it),
  pgvector tested against a local Docker `pgvector/pgvector:pg17` (2048-dim vectors need `halfvec` for HNSW); Pinecone SDK 10.2.0 untested live.
- **Capstone:** Next 16.4.3 / React 19.3.1; `backend/llm.py` is a copy of `common/llm.py` (`make -C sessions/capstone sync-llm`; a test fails on drift).
- **Untested live:** every Gemini, OpenAI and Anthropic branch; Pinecone; Supabase/Neon; Render/Vercel/Codespaces deploys.
