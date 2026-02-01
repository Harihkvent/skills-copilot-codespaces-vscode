"""
Web search tool
"""
import httpx
from typing import Dict, Any, Tuple
from urllib.parse import quote_plus
import re

from app.tools.base import BaseTool, ToolResult


class WebSearchTool(BaseTool):
    """Tool for searching the web using DuckDuckGo HTML"""
    
    def __init__(self):
        super().__init__()
        self.name = "search.web"
        self.description = "Search the web for information"
        self.requires_confirmation = False
        self.parameters = {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query"
                },
                "num_results": {
                    "type": "integer",
                    "description": "Number of results to return (default: 5)",
                    "default": 5
                }
            },
            "required": ["query"]
        }
    
    def validate(self, args: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate search arguments"""
        if not args.get("query"):
            return False, "Search query is required"
        return True, ""
    
    async def run(self, args: Dict[str, Any], user_context: Dict[str, Any]) -> ToolResult:
        """
        Perform web search using DuckDuckGo HTML
        """
        try:
            query = args["query"]
            num_results = min(args.get("num_results", 5), 10)  # Cap at 10
            
            # Use DuckDuckGo HTML search (no API key needed)
            url = "https://html.duckduckgo.com/html/"
            params = {
                "q": query,
                "kl": "us-en"
            }
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(url, data=params, headers=headers, follow_redirects=True)
                response.raise_for_status()
                
                # Parse HTML results
                results = self._parse_duckduckgo_html(response.text, num_results)
                
                return ToolResult(
                    status="success",
                    result={
                        "query": query,
                        "results": results,
                        "count": len(results)
                    }
                )
                
        except httpx.TimeoutException:
            return ToolResult(
                status="failed",
                error="Search request timed out"
            )
        except httpx.HTTPError as e:
            return ToolResult(
                status="failed",
                error=f"HTTP error: {str(e)}"
            )
        except Exception as e:
            return ToolResult(
                status="failed",
                error=f"Search failed: {str(e)}"
            )
    
    def _parse_duckduckgo_html(self, html: str, max_results: int) -> list:
        """
        Parse DuckDuckGo HTML results
        This is a simple parser - in production, use a proper HTML parser like BeautifulSoup
        """
        results = []
        
        # Simple regex-based extraction (not ideal but works without dependencies)
        # Match result blocks
        result_pattern = r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>([^<]+)</a>'
        snippet_pattern = r'<a[^>]+class="result__snippet"[^>]*>([^<]+)</a>'
        
        links = re.findall(result_pattern, html)
        snippets = re.findall(snippet_pattern, html)
        
        for i, (url, title) in enumerate(links[:max_results]):
            snippet = snippets[i] if i < len(snippets) else ""
            
            # Clean up HTML entities
            title = self._clean_html(title)
            snippet = self._clean_html(snippet)
            
            results.append({
                "title": title,
                "url": url,
                "snippet": snippet
            })
        
        # If parsing fails, return a fallback message
        if not results:
            results.append({
                "title": "Search results",
                "url": f"https://duckduckgo.com/?q={quote_plus(args.get('query', ''))}",
                "snippet": "Click to see search results on DuckDuckGo"
            })
        
        return results
    
    def _clean_html(self, text: str) -> str:
        """Clean HTML entities and tags"""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Decode common HTML entities
        replacements = {
            '&amp;': '&',
            '&lt;': '<',
            '&gt;': '>',
            '&quot;': '"',
            '&#39;': "'",
            '&nbsp;': ' '
        }
        for entity, char in replacements.items():
            text = text.replace(entity, char)
        return text.strip()
