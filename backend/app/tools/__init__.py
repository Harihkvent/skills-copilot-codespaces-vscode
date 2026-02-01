"""Tools module initialization"""
from app.tools.base import BaseTool, ToolResult
from app.tools.registry import tool_registry, get_tool, list_tools, get_tool_schemas
from app.tools.mail import MailSendTool
from app.tools.search import WebSearchTool

__all__ = [
    "BaseTool",
    "ToolResult",
    "tool_registry",
    "get_tool",
    "list_tools",
    "get_tool_schemas",
    "MailSendTool",
    "WebSearchTool",
]
