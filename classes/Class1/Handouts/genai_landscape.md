# The GenAI landscape (November 2026)

A map of the tools you'll hear about, so you can place any new one. Tools change every month; the four layers
and the course ideas (tokens, prompts, embeddings, RAG, tool calls, evals) don't. **In course** = where we use it.

| Layer | What it is | Examples |
|---|---|---|
| 1 · Models | The labs that train them | Anthropic (Claude), OpenAI (GPT), Google (Gemini), Meta (Llama), Mistral, DeepSeek, Qwen, xAI (Grok) |
| 2 · Access | Ways to call the models | Lab APIs, NVIDIA, OpenRouter, LiteLLM, AWS Bedrock, Azure AI Foundry, Vertex AI |
| 3 · Building blocks | What apps are made of | Vector DBs, LangChain / LlamaIndex, evals, MCP, FastAPI, Next.js |
| 4 · Apps | What people use | ChatGPT, Claude, Gemini, Copilot, Cursor, Midjourney, ElevenLabs |

## Access: one key, many models

| Kind | Examples | In course |
|---|---|---|
| Lab APIs | [Anthropic](https://console.anthropic.com), [OpenAI](https://platform.openai.com), [Gemini / AI Studio](https://aistudio.google.com) | Sessions 1–24 |
| Open-model hosts | [NVIDIA build](https://build.nvidia.com) (our default), Groq, Together, Fireworks, Hugging Face | Sessions 1–24 |
| Aggregators | [OpenRouter](https://openrouter.ai) (API), [Poe](https://poe.com) (chat app) | |
| Gateways | [LiteLLM](https://github.com/BerriAI/litellm), Portkey, Vercel AI Gateway, Cloudflare AI Gateway | Session 22 builds the idea |
| Cloud platforms | AWS Bedrock, Azure AI Foundry, Google Vertex AI | |

## Assistants and research

ChatGPT · Claude · Gemini · Microsoft Copilot · Perplexity (web answers with sources) ·
[NotebookLM](https://notebooklm.google.com) (answers only from your sources; a Project 1 option) ·
[Google AI Studio](https://aistudio.google.com) (free Gemini playground; Session 1).
Never paste company data into a personal plan of any of these.

## Coding with AI

| Level | Tools |
|---|---|
| Autocomplete | GitHub Copilot, Cursor Tab |
| Chat in the editor | Copilot Chat, Cursor, Claude Code in VS Code / JetBrains |
| Agent on your machine | Claude Code, OpenAI Codex CLI, Gemini CLI, Google Antigravity, Cursor agent |
| Agent in the cloud (issue in, pull request out) | Copilot coding agent, Codex cloud, Claude Code on the web, Jules, Devin |
| App builders (prototype from a description) | Lovable, Bolt, v0, Replit Agent, AI Studio Build |

Whatever you use, you must be able to explain every line you submit.

## One vendor, many surfaces

| Surface | Anthropic | OpenAI | Google |
|---|---|---|---|
| Chat app | Claude | ChatGPT | Gemini |
| Coding in the terminal | Claude Code | Codex CLI | Gemini CLI |
| Coding in an editor | Claude Code for VS Code, JetBrains | Codex IDE extension | Antigravity |
| Coding in the cloud | Claude Code on the web | Codex cloud | Jules |
| Agent for desk work | Cowork, Claude in Chrome | ChatGPT agent, Atlas browser | Gemini in Chrome |
| Your documents | Projects | Projects | NotebookLM, Gems |
| Add-ons | Skills, plugins, MCP connectors | GPTs, apps in ChatGPT | Gems, extensions |
| For developers | Claude API, Agent SDK | OpenAI API, Agents SDK | Gemini API, ADK |

**MCP** (Model Context Protocol) is the common plug between assistants and tools or data; Session 15 (tool calling)
is the idea underneath it.

## Images, video, voice, music

| Media | Tools | In course |
|---|---|---|
| Images | Nano Banana and Imagen (Google), GPT Image (OpenAI), Midjourney, FLUX, Ideogram, Adobe Firefly, Canva | Session 17 (FLUX, Gemini, OpenAI) |
| Video | Veo and Flow (Google), Kling, Runway, Seedance, Luma | |
| Avatars | HeyGen, Synthesia | |
| Speech to text | Whisper, NVIDIA Parakeet, Deepgram, AssemblyAI | Session 18 |
| Text to speech | ElevenLabs, NVIDIA Magpie, OpenAI and Gemini voices | Session 18 |
| Live voice | OpenAI Realtime, Gemini Live | |
| Music | Suno, Udio | |

Check the rights to what you generate, and get consent before cloning anyone's voice.

## The builder's stack (this course)

| Need | We use | Also on the market |
|---|---|---|
| Vector databases | Chroma, pgvector, Pinecone (Sessions 10–12) | Qdrant, Weaviate, Milvus |
| Frameworks | LangChain, LlamaIndex (Session 20) | LangGraph, CrewAI, the labs' agent SDKs |
| Evaluation | Our own test sets (Sessions 7, 13) | Ragas, LangSmith, Langfuse, Braintrust |
| Tools and actions | Function calling (Session 15) | MCP servers |
| Guardrails | Input/output checks (Session 19) | Moderation APIs, NeMo Guardrails |
| App and deploy | FastAPI, Next.js (Sessions 3, 21–23) | Vercel, Render, Cloud Run |

## Entering GenAI now: where to look

1. **Agents and tools:** models that act (tool calling, MCP, computer use), kept safe.
2. **RAG and evals:** answers grounded in your data, and proof they stay right.
3. **AI-assisted coding:** directing coding agents and reviewing their work.
4. **Multimodal:** documents, screenshots and voice as everyday inputs.
5. **Cost and speed:** small and open models, caching, routing between models.
6. **Trust:** privacy, prompt injection, India's DPDP Act, the EU AI Act.

To keep up: pick one assistant, one coding tool and one API; test new models on your own 10 questions;
compare on [LMArena](https://lmarena.ai) and [Artificial Analysis](https://artificialanalysis.ai).
