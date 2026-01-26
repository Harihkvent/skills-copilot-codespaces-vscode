"""
LLM Adapter for interacting with different LLM providers
"""
from typing import Dict, Any, List, Optional
import json
import httpx

from app.core.config import settings
from app.tools.registry import get_tool_schemas


class LLMAdapter:
    """
    Adapter for LLM providers (Krutrim, local LLM, etc.)
    """
    
    def __init__(self, provider: str = None):
        self.provider = provider or settings.LLM_PROVIDER
    
    async def generate_plan(
        self,
        prompt: str,
        context: List[Dict[str, str]] = None,
        tools: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a plan using the LLM
        
        Args:
            prompt: User prompt/transcript
            context: Conversation context
            tools: Available tool schemas
            
        Returns:
            Dictionary with intent, confidence, tool_calls, etc.
        """
        if self.provider == "krutrim":
            return await self._call_krutrim(prompt, context, tools)
        else:
            return await self._call_local_llm(prompt, context, tools)
    
    async def _call_krutrim(
        self,
        prompt: str,
        context: List[Dict[str, str]],
        tools: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Call Krutrim API
        """
        if not settings.KRUTRIM_API_KEY:
            raise ValueError("KRUTRIM_API_KEY not configured")
        
        # Build messages
        messages = context or []
        messages.append({"role": "user", "content": prompt})
        
        # Add system message with tools
        system_message = self._build_system_prompt(tools)
        messages.insert(0, {"role": "system", "content": system_message})
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.KRUTRIM_API_URL}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.KRUTRIM_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "krutrim-v1",
                        "messages": messages,
                        "temperature": 0.7
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                result = response.json()
                
                # Parse the response
                return self._parse_llm_response(result["choices"][0]["message"]["content"])
                
        except Exception as e:
            # Fallback to simple parsing
            return self._fallback_plan(prompt)
    
    async def _call_local_llm(
        self,
        prompt: str,
        context: List[Dict[str, str]],
        tools: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Call local LLM (Ollama or similar)
        TODO: Integrate with Ollama API at LOCAL_LLM_URL
        Steps needed:
        1. Format messages for Ollama API format
        2. Make HTTP request to {settings.LOCAL_LLM_URL}/api/generate
        3. Parse structured response
        4. Handle errors and timeouts
        See: https://github.com/ollama/ollama/blob/main/docs/api.md
        """
        # For now, return a simple parsed response
        return self._fallback_plan(prompt)
    
    def _build_system_prompt(self, tools: List[Dict[str, Any]]) -> str:
        """Build system prompt with available tools"""
        tools_desc = "\n".join([
            f"- {tool['name']}: {tool['description']}"
            for tool in (tools or [])
        ])
        
        return f"""You are Astra's Planner agent. You analyze user requests and create execution plans.

Available tools:
{tools_desc}

Your response should be a JSON object with:
- intent: the user's intent (string)
- confidence: confidence score 0-1 (float)
- requires_confirmation: whether action needs confirmation (boolean)
- tool_calls: array of tool calls with "tool" and "args" keys
- reasoning: brief explanation of your plan (string)

Example:
{{
  "intent": "send_email",
  "confidence": 0.95,
  "requires_confirmation": true,
  "tool_calls": [
    {{
      "tool": "mail.send",
      "args": {{
        "to": "ravi@example.com",
        "subject": "Meeting update",
        "body": "Hi Ravi, I'll join the meeting tomorrow."
      }}
    }}
  ],
  "reasoning": "User wants to send an email to Ravi about joining tomorrow"
}}"""
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response to extract structured data"""
        try:
            # Try to parse as JSON
            if "{" in response and "}" in response:
                start = response.find("{")
                end = response.rfind("}") + 1
                json_str = response[start:end]
                return json.loads(json_str)
        except Exception:
            pass
        
        return self._fallback_plan(response)
    
    def _fallback_plan(self, prompt: str) -> Dict[str, Any]:
        """
        Create a simple fallback plan when LLM is not available
        This is a basic intent parser
        """
        prompt_lower = prompt.lower()
        
        # Simple keyword-based intent detection
        if any(word in prompt_lower for word in ["send", "mail", "email"]):
            return {
                "intent": "send_email",
                "confidence": 0.7,
                "requires_confirmation": True,
                "tool_calls": [],
                "reasoning": "Detected email-related request. LLM unavailable, manual confirmation needed."
            }
        elif any(word in prompt_lower for word in ["search", "find", "look up"]):
            return {
                "intent": "web_search",
                "confidence": 0.7,
                "requires_confirmation": False,
                "tool_calls": [],
                "reasoning": "Detected search request. LLM unavailable."
            }
        else:
            return {
                "intent": "unknown",
                "confidence": 0.3,
                "requires_confirmation": True,
                "tool_calls": [],
                "reasoning": "Unable to determine intent. LLM unavailable."
            }
