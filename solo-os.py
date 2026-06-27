#!/usr/bin/env python3
"""
Solo Builder OS - Full 9-Agent Pipeline
Runs all 9 World-Class Agents in sequence with session saving,
so you never lose progress if the API fails mid-workflow.
"""

import os
import sys
import json
import time
import datetime
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("Error: Run `pip install -r core-engine/requirements.txt` first.")
    sys.exit(1)

# ── Configuration ─────────────────────────────────────────────────────────────
API_KEY = os.environ.get("OPENAI_API_KEY")
if not API_KEY:
    print("Error: OPENAI_API_KEY is not set. Copy .env.example to .env and fill it in.")
    sys.exit(1)

client = OpenAI(api_key=API_KEY)
PROJECT_ROOT = Path(__file__).parent
AGENTS_DIR   = PROJECT_ROOT / "agents"
SESSIONS_DIR = PROJECT_ROOT / "sessions"
SESSIONS_DIR.mkdir(exist_ok=True)

# ── The 9-Agent Pipeline ───────────────────────────────────────────────────────
PIPELINE = [
    {"id": "strategy",      "name": "Product Strategist",   "file": "product-strategist.md"},
    {"id": "market",        "name": "Market Researcher",     "file": "market-researcher.md"},
    {"id": "prd",           "name": "PRD Writer",            "file": "prd-writer.md"},
    {"id": "ux",            "name": "UX Planner",            "file": "ux-planner.md"},
    {"id": "code",          "name": "Code Planner",          "file": "code-planner.md"},
    {"id": "growth",        "name": "Growth Marketer",       "file": "growth-marketer.md"},
    {"id": "monetization",  "name": "Monetization Advisor",  "file": "monetization-advisor.md"},
    {"id": "launch",        "name": "Launch Operator",       "file": "launch-operator.md"},
    {"id": "quality",       "name": "Quality Evaluator",     "file": "quality-evaluator.md"},
]

# ── Helpers ────────────────────────────────────────────────────────────────────
def separator(title: str):
    w = 60
    print("\n" + "═" * w)
    print(f"  {title}")
    print("═" * w)

def load_prompt(filename: str) -> str:
    path = AGENTS_DIR / filename
    if not path.exists():
        print(f"Error: Agent file not found: {path}")
        sys.exit(1)
    return path.read_text(encoding="utf-8")

def call_agent(agent_name: str, prompt_file: str, user_message: str) -> str:
    """Single API call for one agent step."""
    system_prompt = load_prompt(prompt_file)
    print(f"\n  🤖 {agent_name} is working...", end="", flush=True)
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message},
        ],
        temperature=0.4,
    )
    print(" Done ✓")
    return response.choices[0].message.content

def save_session(session: dict, session_file: Path):
    session_file.write_text(json.dumps(session, ensure_ascii=False, indent=2), encoding="utf-8")

def load_session(session_file: Path) -> dict:
    return json.loads(session_file.read_text(encoding="utf-8"))

def approval_gate(agent_name: str, output: str) -> bool:
    """Human-in-the-loop approval. Returns True if approved."""
    print(f"\n{'─'*60}")
    print(output)
    print(f"{'─'*60}")
    while True:
        choice = input(f"\n[Feedback Control] Approve {agent_name} output? (y/n/r for retry): ").strip().lower()
        if choice in ("y", "n", "r"):
            return choice
    return "y"

# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    separator("🚀 Solo Builder OS — Full 9-Agent Pipeline")
    print("  Sessions are saved after each step. You can resume if interrupted.")

    # Resume or start fresh
    existing = sorted(SESSIONS_DIR.glob("*.json"), reverse=True)
    session_file = None
    session = {}

    if existing:
        resume = input(f"\n  Found saved session: {existing[0].name}. Resume? (y/n): ").strip().lower()
        if resume == "y":
            session = load_session(existing[0])
            session_file = existing[0]
            print(f"  Resuming from step: {session.get('last_completed', 'beginning')}")

    if not session:
        idea = input("\n  What is your raw product idea?\n  > ").strip()
        if not idea:
            print("Idea cannot be empty.")
            sys.exit(1)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        session_file = SESSIONS_DIR / f"session_{ts}.json"
        session = {"idea": idea, "last_completed": None, "outputs": {}}
        save_session(session, session_file)

    idea = session["idea"]
    outputs = session["outputs"]

    # Build rolling context across agents
    context_parts = [f"## Original Idea\n{idea}"]

    for step in PIPELINE:
        sid = step["id"]
        agent_name = step["name"]

        # Skip already-completed steps
        if sid in outputs:
            print(f"\n  ✓ Skipping {agent_name} (already completed)")
            context_parts.append(f"## {agent_name} Output\n{outputs[sid]}")
            continue

        separator(f"Step: {agent_name}")
        full_context = "\n\n".join(context_parts)
        user_message = (
            f"Here is all context gathered so far:\n\n{full_context}\n\n"
            f"Now perform your role as the {agent_name}. Be thorough, rigorous, and specific."
        )

        while True:
            output = call_agent(agent_name, step["file"], user_message)
            decision = approval_gate(agent_name, output)

            if decision == "y":
                outputs[sid] = output
                session["last_completed"] = sid
                save_session(session, session_file)
                context_parts.append(f"## {agent_name} Output\n{output}")
                break
            elif decision == "n":
                print("  Workflow stopped by user.")
                sys.exit(0)
            elif decision == "r":
                print("  Retrying...\n")
                # Optionally collect feedback before retrying
                feedback = input("  (Optional) Any specific feedback for the retry? > ").strip()
                if feedback:
                    user_message += f"\n\n## Human Feedback (incorporate this)\n{feedback}"
                continue

        time.sleep(0.5)  # Brief pause between agents

    # Export final artifacts
    separator("✅ Pipeline Complete!")
    out_dir = PROJECT_ROOT / "output"
    out_dir.mkdir(exist_ok=True)
    for step in PIPELINE:
        sid = step["id"]
        if sid in outputs:
            out_path = out_dir / f"{sid}.md"
            out_path.write_text(outputs[sid], encoding="utf-8")
    print(f"\n  All 9 agent outputs saved to: {out_dir}/")
    print(f"  Full session saved to: {session_file}\n")

if __name__ == "__main__":
    main()
