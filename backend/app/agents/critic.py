"""
Critic Agent
Validates plans for safety and permissions
"""
from typing import Dict, Any, List


class CriticAgent:
    """
    Critic Agent validates execution plans for safety
    """
    
    def __init__(self):
        self.dangerous_actions = ["system.exec", "file.delete"]
        self.always_confirm = ["mail.send", "system.exec"]
    
    async def validate_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a plan for safety and permissions
        
        Args:
            plan: Plan from PlannerAgent
            
        Returns:
            Validation result with approved flag and warnings
        """
        warnings = []
        approved = True
        reasoning = []
        
        # Check if plan requires confirmation
        requires_confirmation = plan.get("requires_confirmation", False)
        
        # Check each tool call
        tool_calls = plan.get("tool_calls", [])
        for tool_call in tool_calls:
            tool_name = tool_call.get("tool", "")
            
            # Check for dangerous actions
            if tool_name in self.dangerous_actions:
                warnings.append(f"Tool '{tool_name}' is potentially dangerous")
                requires_confirmation = True
            
            # Check for actions that always need confirmation
            if tool_name in self.always_confirm:
                requires_confirmation = True
                reasoning.append(f"Tool '{tool_name}' requires explicit user confirmation")
        
        # Build response
        result = {
            "approved": approved,
            "requires_confirmation": requires_confirmation,
            "warnings": warnings,
            "reasoning": " | ".join(reasoning) if reasoning else "Plan appears safe to execute"
        }
        
        return result
