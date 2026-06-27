# Solo Builder OS: Core Autonomous Engine

Welcome to the **"Hermes/Claude-Level"** engine. This directory transforms the Solo Builder OS from a passive prompt library into an **active, autonomous entity**.

## Why does this exist?
Standard LLM scripts just return text. Real autonomous agents (like Devin or Claude Engineer) operate on a **ReAct (Reasoning + Acting)** loop. They can look around your file system, write code, run terminal commands, debug their own errors, and iterate until the job is done.

## The Architecture
1. **`tools.py`**: Defines the "Hands" of the agent. It gives the AI the ability to read files, write files, and execute Bash/Terminal commands (via OpenAI Function Calling).
2. **`agent.py`**: Defines the "Brain" of the agent. It runs a `while` loop that forces the AI to:
   - **Think** about the task.
   - **Act** by selecting a tool (e.g., `execute_command("npm init -y")`).
   - **Observe** the output (e.g., reading the terminal error).
   - **Self-Correct** based on the observation.

## How to Run the Autonomous Agent

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set your API Key:**
   ```bash
   export OPENAI_API_KEY="sk-your-key-here"
   ```

3. **Launch the Engine:**
   ```bash
   python agent.py
   ```

4. **Give it a complex task:**
   - *Example 1:* "Read the `prd.md` file in the root directory, create a new folder called `frontend`, and initialize a React project inside it."
   - *Example 2:* "Run tests on my Python file. If they fail, fix the code until they pass."

---
**Warning:** This agent has access to your terminal via `execute_command`. Use it with caution and do not give it destructive commands.
