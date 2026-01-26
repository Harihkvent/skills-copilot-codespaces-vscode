"""
Tool registry
Manages all available tools and provides access to them
"""
from typing import Dict, Optional
from app.tools.base import BaseTool
from app.tools.mail import MailSendTool
from app.tools.search import WebSearchTool


class ToolRegistry:
    """
    Registry for all available tools
    """
    
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register all default tools"""
        self.register(MailSendTool())
        self.register(WebSearchTool())
    
    def register(self, tool: BaseTool):
        """Register a new tool"""
        self._tools[tool.name] = tool
    
    def get(self, tool_name: str) -> Optional[BaseTool]:
        """Get a tool by name"""
        return self._tools.get(tool_name)
    
    def list_tools(self) -> Dict[str, BaseTool]:
        """Get all registered tools"""
        return self._tools.copy()
    
    def get_schemas(self) -> list:
        """Get schemas for all tools (for LLM function calling)"""
        return [tool.get_schema() for tool in self._tools.values()]


# Global tool registry instance
tool_registry = ToolRegistry()


def get_tool(tool_name: str) -> Optional[BaseTool]:
    """Get a tool from the registry"""
    return tool_registry.get(tool_name)


def list_tools() -> Dict[str, BaseTool]:
    """List all available tools"""
    return tool_registry.list_tools()


def get_tool_schemas() -> list:
    """Get tool schemas for LLM function calling"""
    return tool_registry.get_schemas()
