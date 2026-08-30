"""Google ADK weather agent backed by a Streamable HTTP MCP server."""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from google.adk import Agent
from google.adk.tools.mcp_tool.mcp_toolset import (
    McpToolset,
    StreamableHTTPConnectionParams,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CLIENT_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(PROJECT_ROOT / ".env")
load_dotenv(CLIENT_DIR / ".env", override=True)

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8085/mcp")
logger.info("Initializing weather agent with MCP server at %s", MCP_SERVER_URL)

connection_params = StreamableHTTPConnectionParams(
    url=MCP_SERVER_URL,
    timeout=30.0,
)
weather_tools = McpToolset(connection_params=connection_params)

root_agent = Agent(
    name="weather_agent",
    model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
    description="An assistant that answers current-weather and forecast questions.",
    instruction=(
        "Use the MCP weather tools for weather questions. "
        "If a tool reports a configuration or network error, explain it clearly."
    ),
    tools=[weather_tools],
)
