import os
import subprocess

from langchain_core.tools import tool
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("demo")


@tool
def run_python(code: str) -> str:
    """Execute Python code and return the result."""
    # ruleid: dangerous-sink-in-tool
    return str(eval(code))


@tool("shell", return_direct=True)
def run_shell(command: str) -> str:
    """Run a shell command."""
    # ruleid: dangerous-sink-in-tool
    return subprocess.check_output(command, shell=True).decode()


@mcp.tool()
def system_command(cmd: str) -> int:
    """Run a system command."""
    # ruleid: dangerous-sink-in-tool
    return os.system(cmd)


@mcp.tool(description="execute a snippet")
def exec_snippet(snippet: str) -> None:
    # ruleid: dangerous-sink-in-tool
    exec(snippet)


# CrewAI exports the same @tool decorator shape (from crewai.tools import tool):
@tool("CrewAI shell tool")
def crewai_shell(command: str) -> str:
    """Run a command for the crew."""
    # ruleid: dangerous-sink-in-tool
    return subprocess.run(command, shell=True, capture_output=True).stdout.decode()


@tool
def word_count(text: str) -> int:
    """Count words in text."""
    # ok: dangerous-sink-in-tool
    return len(text.split())


@tool
def list_directory(path: str) -> str:
    """List a directory using a fixed command with an args list."""
    # ok: dangerous-sink-in-tool
    return subprocess.check_output(["ls", "-la"]).decode()


def not_a_tool(cmd: str) -> int:
    # ok: dangerous-sink-in-tool
    return os.system(cmd)
