<div align="center">

# Solo Builder OS 🚀

**An open-source framework of 9 AI Agents that turns a raw idea into a world-class product plan.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-green.svg)](https://openai.com/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

</div>

---

## What it actually does (no hype)

Most AI tools help you build the wrong thing faster. Solo Builder OS forces the AI to **behave like a rigorous product team** — one that pushes back, cuts scope, and demands evidence before moving forward.

It runs a sequential 9-agent pipeline, where **every agent's output is reviewed by you before the next agent begins** (the Feedback Control Loop). The result is a complete, validated product plan saved to your disk.

```
Your Idea
    │
    ▼
1. Product Strategist   → Core Truth, JTBD, brutal MVP scope
    │ (you approve)
    ▼
2. Market Researcher    → Blue Ocean gap, competitor teardown, Moat
    │ (you approve)
    ▼
3. PRD Writer           → Amazon PR/FAQ, MECE user stories, edge cases
    │ (you approve)
    ▼
4. UX Planner           → Fogg Behavior Model, frictionless flow, IA
    │ (you approve)
    ▼
5. Code Planner         → SOLID architecture, zero-ops stack, issue-ready tasks
    │ (you approve)
    ▼
6. Growth Marketer      → AIDA copy, viral loop, launch assets
    │ (you approve)
    ▼
7. Monetization Advisor → Value-based pricing, tier anchoring
    │ (you approve)
    ▼
8. Launch Operator      → Distribution matrix, T-minus calendar, KPIs
    │ (you approve)
    ▼
9. Quality Evaluator    → Red-team audit. Rejects weak outputs automatically.
    │
    ▼
output/*.md  ← your complete product plan on disk
```

---

## Quick Start (60 seconds)

```bash
# 1. Clone
git clone https://github.com/tksoft11/solo-builder-os.git
cd solo-builder-os

# 2. Install dependencies
pip install -r core-engine/requirements.txt

# 3. Set your API key
cp .env.example .env
# Edit .env and paste your OPENAI_API_KEY

export OPENAI_API_KEY="sk-your-key-here"

# 4. Run the full pipeline
python solo-os.py
```

The tool will guide you through each step interactively. After each agent produces output, you can **approve (y)**, **stop (n)**, or **retry with feedback (r)**.
Sessions are saved to `sessions/` — if your API call fails halfway, you can resume exactly where you stopped.

---

## What's inside

| Path | What it does |
| :--- | :--- |
| `agents/` | 9 agent definitions with embedded frameworks (JTBD, Blue Ocean, SOLID, etc.) |
| `solo-os.py` | CLI that runs the full 9-agent pipeline with session saving and human approval gates |
| `core-engine/agent.py` | Autonomous ReAct loop with token tracking and cost estimation |
| `core-engine/tools.py` | 6 tools: `read_file`, `write_file`, `list_directory`, `search_files`, `execute_command`, `ask_human` |
| `ide-rules/cursorrules.md` | Drop-in rules for Cursor / Windsurf to enforce MVP scope in your editor |
| `examples/` | End-to-end examples: Thai Calendar PWA, NicheTrend Radar |
| `workflows/` | Step-by-step workflow documentation |

---

## The 9 Agents

| # | Agent | Core Framework |
| :- | :--- | :--- |
| 1 | Product Strategist | First Principles · Jobs-to-be-Done |
| 2 | Market Researcher | Blue Ocean Strategy · Moat Analysis |
| 3 | PRD Writer | Amazon PR/FAQ · MECE |
| 4 | UX Planner | Fogg Behavior Model · Cognitive Load |
| 5 | Code Planner | SOLID · Zero-Ops (Jamstack/Serverless) |
| 6 | Growth Marketer | AIDA · PAS · Viral Loop Design |
| 7 | Monetization Advisor | Value-Based Pricing · Anchoring |
| 8 | Launch Operator | Distribution Matrix · Traction KPIs |
| 9 | Quality Evaluator | Red-Team · Self-Correction |

---

## Autonomous Agent (for developers)

The `core-engine/` contains a standalone autonomous agent that can read, write, and execute code:

```bash
cd solo-builder-os
python core-engine/agent.py
# Choose an agent role, point it at a working directory, describe the task
# It will think, act, observe, and self-correct until done
```

**What it can do:**
- Read any file in your project
- Write and create files
- List directory structure before touching anything
- Search across files with regex
- Run terminal commands (with safety guardrails)
- Ask you for clarification when genuinely stuck
- Track token usage and estimate API cost

---

## Examples

See [examples/](examples/) for complete end-to-end runs:
- **[Thai Calendar PWA](examples/thai-calendar-pwa/)** — From "I want to show Thai holidays" to full SOLID architecture + Affiliate monetization plan.
- **[NicheTrend Radar](examples/trend-curator/)** — From "track affiliate trends" to B2B SaaS pricing + Programmatic SEO launch plan.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). PRs that add new agents, new tools, or real-world example runs are especially welcome.

---

*MIT License · Built for solo founders who are serious about shipping.*
