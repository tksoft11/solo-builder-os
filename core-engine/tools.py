import os
import subprocess

def read_file(filepath: str) -> str:
    """Reads the content of a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def write_file(filepath: str, content: str) -> str:
    """Writes content to a file, creating directories if needed."""
    try:
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

def execute_command(command: str, cwd: str = ".") -> str:
    """Executes a terminal command and returns the output."""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        output = result.stdout
        if result.stderr:
            output += f"\nSTDERR: {result.stderr}"
        return output if output else "Command executed successfully with no output."
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds."
    except Exception as e:
        return f"Error executing command: {str(e)}"

# The schema mapping for OpenAI Function Calling
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads the content of a file from the local filesystem.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "Path to the file."}
                },
                "required": ["filepath"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Writes text content to a file on the local filesystem.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "Path to the file to write."},
                    "content": {"type": "string", "description": "The content to write into the file."}
                },
                "required": ["filepath", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "execute_command",
            "description": "Executes a bash/terminal command on the host machine.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The command to run (e.g., 'npm install', 'git status')."},
                    "cwd": {"type": "string", "description": "Current working directory. Default is '.'"}
                },
                "required": ["command"],
            },
        },
    }
]

# Dispatcher
def execute_tool_call(name: str, arguments: dict) -> str:
    if name == "read_file":
        return read_file(arguments["filepath"])
    elif name == "write_file":
        return write_file(arguments["filepath"], arguments["content"])
    elif name == "execute_command":
        return execute_command(arguments["command"], arguments.get("cwd", "."))
    else:
        return f"Unknown tool: {name}"
