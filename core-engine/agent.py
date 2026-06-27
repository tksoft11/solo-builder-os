#!/usr/bin/env python3
"""
Solo Builder OS — Autonomous ReAct Agent
Uses the ReAct (Reasoning + Acting) loop to complete complex,
multi-step coding tasks autonomously using real filesystem and terminal tools.
"""

import os
import sys
import json
import time
from pathlib import Path
from colorama import init, Fore, Style
from openai import OpenAI
from tools import TOOLS_SCHEMA, execute_tool_call

init(autoreset=True)

# ── Configuration ──────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent
AGENTS_DIR   = PROJECT_ROOT / "agents"
MODEL        = "gpt-4o"
MAX_TOKENS_WARN = 100_000   # warn when context approaches limit

# ── Agent ──────────────────────────────────────────────────────────────────────
class AutonomousAgent:
    def __init__(self, role_name: str, role_file: str, max_iterations: int = 20, workdir: str = "."):
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print(Fore.RED + "Error: OPENAI_API_KEY is not set.")
            sys.exit(1)

        self.client = OpenAI(api_key=api_key)
        self.role_name = role_name
        self.max_iterations = max_iterations
        self.workdir = str(Path(workdir).resolve())
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0

        # Load role prompt from agents directory
        role_path = AGENTS_DIR / role_file
        if not role_path.exists():
            print(Fore.RED + f"Error: Agent file not found: {role_path}")
            sys.exit(1)
        role_prompt = role_path.read_text(encoding="utf-8")

        self.messages = [
            {
                "role": "system",
                "content": (
                    f"{role_prompt}\n\n"
                    "You are operating as an autonomous agent with access to filesystem and terminal tools.\n"
                    f"The working directory for this task is: {self.workdir}\n\n"
                    "## Operating Rules\n"
                    "1. ALWAYS start by calling `list_directory` to understand the project structure.\n"
                    "2. Think step-by-step before every action. State your reasoning.\n"
                    "3. After running a command or writing a file, VERIFY the result with `read_file` or `execute_command`.\n"
                    "4. If you encounter an error, analyse it and self-correct — do not give up on the first failure.\n"
                    "5. Use `ask_human` only when you are genuinely blocked and cannot proceed without input.\n"
                    "6. When the task is fully complete, state 'TASK COMPLETE' clearly in your final message."
                ),
            }
        ]

    # ── Token Tracking ─────────────────────────────────────────────────────────
    def _track_tokens(self, response):
        usage = response.usage
        self.total_prompt_tokens     += usage.prompt_tokens
        self.total_completion_tokens += usage.completion_tokens
        total = self.total_prompt_tokens + self.total_completion_tokens
        if total > MAX_TOKENS_WARN:
            print(Fore.YELLOW + f"  ⚠  Context size warning: {total:,} tokens used. Consider summarising earlier context.")

    def _print_cost_estimate(self):
        # GPT-4o pricing (approximate, as of 2025): $5/1M input, $15/1M output
        cost = (self.total_prompt_tokens / 1_000_000 * 5.0) + (self.total_completion_tokens / 1_000_000 * 15.0)
        print(Fore.YELLOW + f"\n  💰 Estimated cost: ${cost:.4f} USD  "
              f"({self.total_prompt_tokens:,} prompt + {self.total_completion_tokens:,} completion tokens)")

    # ── Core Loop ──────────────────────────────────────────────────────────────
    def run(self, task: str) -> str:
        print(Fore.CYAN + Style.BRIGHT + f"\n{'═'*60}")
        print(Fore.CYAN + Style.BRIGHT + f"  🚀 {self.role_name} — Task Started")
        print(Fore.CYAN + Style.BRIGHT + f"{'═'*60}")
        print(Fore.WHITE + f"  Task: {task}\n")

        self.messages.append({"role": "user", "content": task})

        for iteration in range(1, self.max_iterations + 1):
            print(Fore.YELLOW + f"\n  ─── Iteration {iteration}/{self.max_iterations} ───")

            # ── LLM Call ──────────────────────────────────────────────────────
            response = self.client.chat.completions.create(
                model=MODEL,
                messages=self.messages,
                tools=TOOLS_SCHEMA,
                tool_choice="auto",
                temperature=0.2,
            )
            self._track_tokens(response)

            message  = response.choices[0].message
            finish   = response.choices[0].finish_reason

            # Print thought
            if message.content:
                print(Fore.MAGENTA + f"\n  🧠 Thought:\n{message.content}")

            self.messages.append(message)

            # ── Tool Execution (Act) ───────────────────────────────────────────
            if message.tool_calls:
                for tc in message.tool_calls:
                    name = tc.function.name
                    args = json.loads(tc.function.arguments)
                    print(Fore.BLUE + f"\n  🛠  Action: {name}({json.dumps(args, ensure_ascii=False)[:200]})")

                    result = execute_tool_call(name, args)

                    # Truncate large outputs in the display (not in the message)
                    display = result if len(result) <= 800 else result[:800] + "\n  ...(truncated for display)"
                    print(Fore.GREEN + f"  👁  Observation:\n{display}")

                    self.messages.append({
                        "role":        "tool",
                        "tool_call_id": tc.id,
                        "name":        name,
                        "content":     result,
                    })

            # ── Task Complete ──────────────────────────────────────────────────
            elif finish == "stop":
                print(Fore.CYAN + Style.BRIGHT + "\n  ✅ Task Complete!")
                self._print_cost_estimate()
                return message.content or ""

            # Slight pause to avoid hammering the API
            time.sleep(0.5)

        # Iteration limit reached
        print(Fore.RED + f"\n  ❌ Reached {self.max_iterations} iterations without completing the task.")
        self._print_cost_estimate()
        return "Did not complete within iteration limit."


# ── Entry Point ────────────────────────────────────────────────────────────────
def main():
    print(Fore.CYAN + Style.BRIGHT + "\n╔══════════════════════════════════════════╗")
    print(Fore.CYAN + Style.BRIGHT +   "║   Solo Builder OS: Autonomous Engine     ║")
    print(Fore.CYAN + Style.BRIGHT +   "╚══════════════════════════════════════════╝\n")

    print("Available agents:")
    for i, f in enumerate(sorted(AGENTS_DIR.glob("*.md")), 1):
        print(f"  {i}. {f.stem}")

    agent_name = input("\nWhich agent role? (e.g., 'code-planner'): ").strip()
    role_file  = f"{agent_name}.md"

    workdir = input("Working directory for the task? (press Enter for current dir): ").strip() or "."
    task    = input("Describe the task in detail:\n> ").strip()
    if not task:
        print("Task cannot be empty.")
        sys.exit(1)

    agent = AutonomousAgent(
        role_name=agent_name.replace("-", " ").title(),
        role_file=role_file,
        workdir=workdir,
    )
    result = agent.run(task)

    # Optionally save the final output
    save = input("\nSave final output to file? (y/n): ").strip().lower()
    if save == "y":
        out = Path(f"{agent_name}-output.md")
        out.write_text(result, encoding="utf-8")
        print(f"Saved to {out}")


if __name__ == "__main__":
    main()
