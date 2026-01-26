"""
Base tool interface
All tools must inherit from this base class
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple
from pydantic import BaseModel


class ToolResult(BaseModel):
    """Standard tool result format"""
    status: str  # success, failed, requires_confirmation
    result: Dict[str, Any] = {}
    error: str = None
    metadata: Dict[str, Any] = {}


class BaseTool(ABC):
    """
    Base class for all tools
    Each tool must implement validate() and run() methods
    """
    
    def __init__(self):
        self.name: str = self.__class__.__name__
        self.requires_confirmation: bool = False
        self.description: str = ""
        self.parameters: Dict[str, Any] = {}
    
    @abstractmethod
    def validate(self, args: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate tool arguments
        
        Args:
            args: Dictionary of arguments
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        pass
    
    @abstractmethod
    async def run(self, args: Dict[str, Any], user_context: Dict[str, Any]) -> ToolResult:
        """
        Execute the tool
        
        Args:
            args: Validated arguments
            user_context: User context information
            
        Returns:
            ToolResult with status and result data
        """
        pass
    
    def get_schema(self) -> Dict[str, Any]:
        """
        Get tool schema for LLM function calling
        
        Returns:
            Dictionary with tool name, description, and parameters
        """
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
            "requires_confirmation": self.requires_confirmation
        }
