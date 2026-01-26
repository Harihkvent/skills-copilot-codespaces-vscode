"""
Planner Agent
Analyzes user requests and creates execution plans
"""
from typing import Dict, Any, List
from app.agents.llm_adapter import LLMAdapter
from app.tools.registry import get_tool_schemas


class PlannerAgent:
    """
    Planner Agent creates execution plans from user requests
    """
    
    def __init__(self):
        self.llm = LLMAdapter()
    
    async def create_plan(
        self,
        user_text: str,
        context: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Create an execution plan from user text
        
        Args:
            user_text: User's transcribed text
            context: Recent conversation context
            
        Returns:
            Plan dictionary with intent, tool_calls, etc.
        """
        # Get available tool schemas
        tools = get_tool_schemas()
        
        # Generate plan using LLM
        plan = await self.llm.generate_plan(
            prompt=user_text,
            context=context,
            tools=tools
        )
        
        return plan
