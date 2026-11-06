# Generative AI & Prompt Engineering: Course Roadmap

8 weeks · 24 live sessions (3 a week) · 90 minutes each · all times IST

## How the course works

- **Run and modify, not write from scratch.** Every lab is a ready-made Python script that you open in VS Code.
  You run it, change the values marked `# change me`, and with an AI assistant's help, change the code.
- **Two paths every session.** The **No-code path** (everyone) uses browser tools and runs the scripts as given. The
  **Build path** (if you know some Python) changes the code. Projects have a level for each path.
- **AI assistants are allowed and taught** from Session 1: the assistant writes, you run and check.
- **Hosted models only.** Everything runs on provider APIs (NVIDIA and Gemini have free tiers), so any laptop works.

**Each session:** concept → live build → "what breaks" in production → homework and one interview question.

## Modules

| Module | Weeks | Sessions | You learn |
|---|---|---|---|
| 1 · LLM & Prompt Foundations | 1–3 | 1–8 | Setup, Python for GenAI (functions, classes, calling and building REST APIs, databases), how LLMs work, tokens and cost, context windows, prompt engineering, structured output |
| 2 · Embeddings, Vector DBs & RAG | 3–5 | 9–14 | Embeddings, Chroma / pgvector / Pinecone, RAG pipelines, chunking and retrieval, evaluation · **Project 1** |
| 3 · Tool Calling & Multimodal | 5–7 | 15–19 | Tool calling, vision, image generation, speech and audio, safety and guardrails |
| 4 · Production GenAI | 7–8 | 20–24 | LangChain and LlamaIndex, FastAPI + Next.js, caching and cost control, deployment · **Capstone** |

## Session by session

| # | Week | Topic | The question |
|---|---|---|---|
| 1 | 1 | Orientation and setup | What can GenAI do, and how will we work? |
| 2 | 1 | **Python for GenAI I**: values, collections, functions, classes, files and JSON, errors | Can I read and change every line in our scripts? |
| 3 | 1 | **Python for GenAI II**: calling REST APIs, building one with FastAPI, databases (SQLite) | How do programs talk to services and remember things? |
| 4 | 2 | How LLMs work | Why does the model say *that*? |
| 5 | 2 | Tokens, context windows, cost | Why did that cost so much, and why did it cut off? |
| 6 | 2 | Prompt engineering I: anatomy | What does a good prompt contain? |
| 7 | 3 | Prompt engineering II: patterns and testing | How do I know my prompt got better? |
| 8 | 3 | Structured output | How do I get data, not prose, every time? |
| 9 | 3 | Embeddings | How does a computer know two sentences mean the same? |
| 10 | 4 | Vector databases · **Project 1 brief** | Where do a million vectors live? |
| 11 | 4 | RAG pipelines | How does a model answer from documents it never saw? |
| 12 | 4 | Chunking and retrieval quality | The answer was in the docs: why didn't we find it? |
| 13 | 5 | Evaluating RAG | How would we know if it got worse? |
| 14 | 5 | **Project 1 demo** | |
| 15 | 5 | Function and tool calling | How does a model *do* things? |
| 16 | 6 | Vision and documents | Can the model read a screenshot, a chart, a PDF? |
| 17 | 6 | Image generation | How do we generate images, and control them? |
| 18 | 6 | Speech and audio · **Capstone brief** | How do we build voice in and voice out? |
| 19 | 7 | Safety and guardrails | How do we stop it saying what it shouldn't? |
| 20 | 7 | LangChain and LlamaIndex | When does a framework help? |
| 21 | 7 | FastAPI + Next.js · **Capstone kickoff** | How does a script become an app? |
| 22 | 8 | Caching and cost control | How do we make it 10x cheaper? |
| 23 | 8 | Deployment and interview prep | What does it take to run this for real users? |
| 24 | 8 | **Capstone demo** | |

## Projects

| | No-code level | Build level |
|---|---|---|
| **Project 1 · Ask-My-Docs** (brief S10, demo S14) | Your own documents in the run-only RAG script or NotebookLM; a 15-question evaluation sheet; three failures and how you fixed them | A RAG notebook over your documents with citations, one vector store, one retrieval fix, and before/after evaluation scores |
| **Capstone · a deployed GenAI app** (brief S18, demo S24) | The starter app configured through one config file and deployed; a red-team report; a cost estimate | A FastAPI + Next.js app with RAG, one tool and one multimodal feature, guardrails, caching and an eval set, deployed with a public URL |

## Before Session 1

- A laptop with Python, Git and **VS Code** installed, and a free **NVIDIA** key: see the setup guide and the VS Code setup guide.

**Prerequisites:** none beyond using a computer. Sessions 2–3 teach the Python the course needs; if you already know
Python, skim them and help a neighbour. From another language? The *Python for programmers* bridge handout helps. If you don't program, take the No-code path; you will still ship both projects.

**After this course:** Agentic AI (agents, tools, multi-agent systems), then AI Engineering / MLOps.
