"""
Agent Orchestrator Service
Coordinates the multi-agent workflow
"""
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.agents import PlannerAgent, CriticAgent, ExecutorAgent
from app.models import Message, ActionLog
from app.schemas import MessageCreate, ActionLogCreate


class AgentOrchestrator:
    """
    Orchestrates the multi-agent workflow:
    1. Perception - normalize input
    2. Memory - retrieve context
    3. Planner - create execution plan
    4. Critic - validate plan
    5. Executor - execute approved actions
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.planner = PlannerAgent()
        self.critic = CriticAgent()
        self.executor = ExecutorAgent()
    
    async def process_command(
        self,
        user_id: str,
        transcript: str,
        context_id: Optional[str] = None,
        task_id: Optional[str] = None,
        confirmed: bool = False
    ) -> Dict[str, Any]:
        """
        Process a user command through the multi-agent pipeline
        
        Args:
            user_id: User identifier
            transcript: User's transcribed text
            context_id: Optional conversation context ID
            task_id: Optional task identifier
            confirmed: Whether user has confirmed the action
            
        Returns:
            Result dictionary with status and actions taken
        """
        try:
            # Step 1: Save user message
            await self._save_message(
                user_id=user_id,
                role="user",
                text=transcript,
                context_id=context_id
            )
            
            # Step 2: Retrieve recent context/memory
            context = await self._get_context(user_id, context_id)
            
            # Step 3: Generate plan using Planner
            plan = await self.planner.create_plan(
                user_text=transcript,
                context=context
            )
            
            # Step 4: Validate plan using Critic
            validation = await self.critic.validate_plan(plan)
            
            # Step 5: Execute if approved
            if validation["approved"]:
                # Check if confirmation is required
                if validation.get("requires_confirmation") and not confirmed:
                    response = {
                        "status": "requires_confirmation",
                        "plan": plan,
                        "validation": validation,
                        "message": "This action requires your confirmation. Please confirm to proceed.",
                        "estimated_ops": [tc.get("tool") for tc in plan.get("tool_calls", [])]
                    }
                else:
                    # Execute the plan
                    user_context = {"user_id": user_id}
                    results = await self.executor.execute_plan(
                        plan=plan,
                        user_context=user_context,
                        confirmed=confirmed
                    )
                    
                    # Log actions
                    await self._log_actions(user_id, plan, results)
                    
                    # Generate response message
                    response_text = self._generate_response(plan, results)
                    
                    # Save assistant message
                    await self._save_message(
                        user_id=user_id,
                        role="assistant",
                        text=response_text,
                        context_id=context_id
                    )
                    
                    response = {
                        "status": "success",
                        "plan": plan,
                        "results": [r.dict() for r in results],
                        "message": response_text,
                        "estimated_ops": [tc.get("tool") for tc in plan.get("tool_calls", [])]
                    }
            else:
                # Plan rejected by critic
                response = {
                    "status": "rejected",
                    "plan": plan,
                    "validation": validation,
                    "message": "Action was rejected for safety reasons.",
                    "estimated_ops": []
                }
            
            return response
            
        except Exception as e:
            # Log error and return failure response
            error_msg = f"Failed to process command: {str(e)}"
            await self._save_message(
                user_id=user_id,
                role="system",
                text=error_msg,
                context_id=context_id
            )
            
            return {
                "status": "error",
                "message": error_msg,
                "estimated_ops": []
            }
    
    async def _save_message(
        self,
        user_id: str,
        role: str,
        text: str,
        context_id: Optional[str] = None
    ):
        """Save a message to the database"""
        from uuid import UUID
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            # If not a valid UUID, use a default or skip saving
            return
        
        message = Message(
            user_id=user_uuid,
            role=role,
            text=text,
            context_id=context_id
        )
        self.db.add(message)
        await self.db.commit()
    
    async def _get_context(
        self,
        user_id: str,
        context_id: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """
        Retrieve recent conversation context
        TODO: Implement vector similarity search for relevant memories
        
        For now, returns basic recent message history.
        Future: Use pgvector for semantic search of memories.
        """
        from sqlalchemy import select
        from uuid import UUID
        
        try:
            user_uuid = UUID(user_id)
            # Get last 5 messages for basic context
            stmt = (
                select(Message)
                .where(Message.user_id == user_uuid)
                .order_by(Message.created_at.desc())
                .limit(5)
            )
            result = await self.db.execute(stmt)
            messages = result.scalars().all()
            
            # Format as context
            context = [
                {"role": msg.role, "content": msg.text}
                for msg in reversed(messages)
            ]
            return context
        except Exception:
            # Return empty on error
            return []
    
    async def _log_actions(
        self,
        user_id: str,
        plan: Dict[str, Any],
        results: List[Any]
    ):
        """Log executed actions to audit trail"""
        from uuid import UUID
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            return
        
        for i, tool_call in enumerate(plan.get("tool_calls", [])):
            result = results[i] if i < len(results) else None
            
            action_log = ActionLog(
                user_id=user_uuid,
                action_type=tool_call.get("tool", "unknown"),
                payload=tool_call.get("args", {}),
                result=result.dict() if result else {},
                confirmed_by_user=True,
                status=result.status if result else "unknown"
            )
            self.db.add(action_log)
        
        await self.db.commit()
    
    def _generate_response(
        self,
        plan: Dict[str, Any],
        results: List[Any]
    ) -> str:
        """Generate a natural language response from plan and results"""
        intent = plan.get("intent", "unknown")
        
        # Check if all results succeeded
        all_success = all(r.status == "success" for r in results)
        
        if all_success:
            if intent == "send_email":
                return "I've sent the email successfully."
            elif intent == "web_search":
                return "I've completed the search. Here are the results."
            else:
                return "I've completed your request successfully."
        else:
            failed = [r for r in results if r.status != "success"]
            errors = ", ".join([r.error for r in failed if r.error])
            return f"I encountered some issues: {errors}"
