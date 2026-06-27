"""
Solo Builder OS — Tool Registry
Gives the autonomous agent real "hands" to interact with the filesystem and terminal.
Each tool is registered in TOOLS_SCHEMA for OpenAI Function Calling.
"""

import os
import re
import subprocess
from pathlib import Path

# ── Safety Guardrails ──────────────────────────────────────────────────────────
BLOCKED_COMMANDS = ["rm -rf /", "format", "del /f /s /q", "mkfs", "dd if="]

def _is_safe_command(command: str) -> bool:
    cmd_lower = command.lower()
    return not any(blocked in cmd_lower for blocked in BLOCKED_COMMANDS)

# ── Tool Implementations ───────────────────────────────────────────────────────

def read_file(filepath: str) -> str:
    """Reads the content of a file."""
    try:
        content = Path(filepath).read_text(encoding="utf-8")
        return content if content else "(empty file)"
    except FileNotFoundError:
        return f"Error: File not found at '{filepath}'."
    except Exception as e:
        return f"Error reading file: {e}"

def write_file(filepath: str, content: str) -> str:
    """Writes content to a file, creating parent directories as needed."""
    try:
        p = Path(filepath)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"Success: Wrote {len(content)} characters to '{filepath}'."
    except Exception as e:
        return f"Error writing file: {e}"

def list_directory(dirpath: str = ".") -> str:
    """Lists all files and directories at the given path, recursively (max depth 3)."""
    try:
        root = Path(dirpath)
        if not root.exists():
            return f"Error: Directory '{dirpath}' does not exist."
        lines = []
        for item in sorted(root.rglob("*")):
            # Limit depth
            depth = len(item.relative_to(root).parts)
            if depth > 3:
                continue
            # Skip hidden / git dirs
            if any(part.startswith(".") for part in item.parts):
                continue
            indent = "  " * (depth - 1)
            icon = "📁" if item.is_dir() else "📄"
            lines.append(f"{indent}{icon} {item.name}")
        return "\n".join(lines) if lines else "(empty directory)"
    except Exception as e:
        return f"Error listing directory: {e}"

def search_files(pattern: str, dirpath: str = ".", file_glob: str = "**/*") -> str:
    """Searches for a regex pattern across files. Returns matching lines with filenames."""
    try:
        root = Path(dirpath)
        regex = re.compile(pattern, re.IGNORECASE)
        results = []
        for filepath in root.glob(file_glob):
            if not filepath.is_file():
                continue
            if any(p.startswith(".") for p in filepath.parts):
                continue
            try:
                for i, line in enumerate(filepath.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                    if regex.search(line):
                        results.append(f"{filepath}:{i}: {line.strip()}")
            except Exception:
                continue
        if not results:
            return f"No matches found for pattern '{pattern}'."
        return "\n".join(results[:50])  # cap at 50 results
    except re.error as e:
        return f"Invalid regex pattern: {e}"
    except Exception as e:
        return f"Error during search: {e}"

def execute_command(command: str, cwd: str = ".") -> str:
    """Executes a shell command and returns stdout + stderr. Blocks dangerous commands."""
    if not _is_safe_command(command):
        return f"Error: Command '{command}' is blocked for safety."
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60,
        )
        output = ""
        if result.stdout:
            output += result.stdout
        if result.stderr:
            output += f"\nSTDERR:\n{result.stderr}"
        return output.strip() if output.strip() else "Command ran with no output (exit code 0)."
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 60 seconds."
    except Exception as e:
        return f"Error executing command: {e}"

def ask_human(question: str) -> str:
    """Pauses execution and asks the human a clarifying question. Returns their answer."""
    print(f"\n  🤔 Agent needs clarification:\n  {question}")
    answer = input("  Your answer: ").strip()
    return answer if answer else "(no answer provided)"

# ── OpenAI Function Calling Schema ─────────────────────────────────────────────
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the full text content of a file from the local filesystem.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "Absolute or relative path to the file."}
                },
                "required": ["filepath"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write or overwrite text content to a file. Creates parent directories automatically.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "Path to the file to write."},
                    "content":  {"type": "string", "description": "Full content to write into the file."},
                },
                "required": ["filepath", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_directory",
            "description": "List all files and subdirectories in a directory (max 3 levels deep). Use this first to understand the project structure before doing anything.",
            "parameters": {
                "type": "object",
                "properties": {
                    "dirpath": {"type": "string", "description": "Path to the directory to list. Default is current directory."}
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_files",
            "description": "Search for a regex pattern across all files in a directory. Returns matching lines with file paths and line numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern":   {"type": "string", "description": "Regex pattern to search for."},
                    "dirpath":   {"type": "string", "description": "Root directory to search in. Default is current directory."},
                    "file_glob": {"type": "string", "description": "Glob pattern to filter files, e.g. '**/*.py'. Default is all files."},
                },
                "required": ["pattern"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "execute_command",
            "description": "Execute a shell/terminal command and return the output. Use for running scripts, installing packages, running tests, git operations, etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The command to execute."},
                    "cwd":     {"type": "string", "description": "Working directory for the command. Default is current directory."},
                },
                "required": ["command"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "ask_human",
            "description": "Ask the human operator a clarifying question when you are uncertain. Use sparingly — only when you truly cannot proceed without the answer.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "The precise question to ask the human."}
                },
                "required": ["question"],
            },
        },
    },
]

# ── Dispatcher ─────────────────────────────────────────────────────────────────
TOOL_MAP = {
    "read_file":       lambda a: read_file(a["filepath"]),
    "write_file":      lambda a: write_file(a["filepath"], a["content"]),
    "list_directory":  lambda a: list_directory(a.get("dirpath", ".")),
    "search_files":    lambda a: search_files(a["pattern"], a.get("dirpath", "."), a.get("file_glob", "**/*")),
    "execute_command": lambda a: execute_command(a["command"], a.get("cwd", ".")),
    "ask_human":       lambda a: ask_human(a["question"]),
}

def execute_tool_call(name: str, arguments: dict) -> str:
    handler = TOOL_MAP.get(name)
    if not handler:
        return f"Error: Unknown tool '{name}'."
    return handler(arguments)
