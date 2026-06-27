# Contributing to Solo Builder OS

Thank you for your interest in contributing! Here is how to get started.

## Ground Rules
- Every Agent file must follow the structure in `agents/product-strategist.md` (Role, Goals, Scope, Inputs, Outputs, Constraints, Handoff).
- Code contributions must pass a manual test before submitting a PR.
- No sycophancy. If you see an agent prompt that praises ideas instead of stress-testing them, fix it.

## How to Add a New Agent
1. Create a new file in `agents/` following the existing format.
2. Add the agent to the `PIPELINE` list in `solo-os.py` in the correct sequential position.
3. Update `agents.md` with the new entry.
4. Add a test case showing a sample input and expected output in `examples/`.

## How to Improve the Core Engine
The engine lives in `core-engine/`. Key files:
- `tools.py` — Add new tool functions here. Register them in `TOOLS_SCHEMA` and `TOOL_MAP`.
- `agent.py` — The ReAct loop. Keep it model-agnostic.

## Submitting a Pull Request
1. Fork the repository.
2. Create a branch: `git checkout -b feat/your-feature-name`
3. Commit with a clear message: `feat: add web_search tool`
4. Open a PR and describe what problem it solves.

## Reporting Bugs
Open a GitHub Issue with:
- The exact command you ran
- The full error output
- Your Python version and OS
