"""
Executor Agent
Executes validated tool calls
"""
from typing import Dict, Any, List
from app.tools.registry import get_tool
from app.tools.base import ToolResult


class ExecutorAgent:
    """
    Executor Agent runs validated tool calls
    """
    
    async def execute_plan(
        self,
        plan: Dict[str, Any],
        user_context: Dict[str, Any],
        confirmed: bool = False
    ) -> List[ToolResult]:
        """
        Execute a validated plan
        
        Args:
            plan: Validated plan from PlannerAgent
            user_context: User context information
            confirmed: Whether user has confirmed the action
            
        Returns:
            List of ToolResult objects
        """
        results = []
        tool_calls = plan.get("tool_calls", [])
        
        for tool_call in tool_calls:
            tool_name = tool_call.get("tool")
            args = tool_call.get("args", {})
            
            # Get tool from registry
            tool = get_tool(tool_name)
            if not tool:
                results.append(ToolResult(
                    status="failed",
                    error=f"Tool '{tool_name}' not found"
                ))
                continue
            
            # Validate arguments
            is_valid, error_msg = tool.validate(args)
            if not is_valid:
                results.append(ToolResult(
                    status="failed",
                    error=f"Invalid arguments: {error_msg}"
                ))
                continue
            
            # Check if confirmation is required
            if tool.requires_confirmation and not confirmed:
                results.append(ToolResult(
                    status="requires_confirmation",
                    result={
                        "tool": tool_name,
                        "args": args,
                        "message": "This action requires user confirmation"
                    }
                ))
                continue
            
            # Execute tool
            try:
                result = await tool.run(args, user_context)
                results.append(result)
            except Exception as e:
                results.append(ToolResult(
                    status="failed",
                    error=f"Execution error: {str(e)}"
                ))
        
        return results
