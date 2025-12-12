import logging
from typing import Dict, List, Any
import json

logger = logging.getLogger(__name__)


class ContextManager:
    def __init__(self, max_tokens: int = 8000):
        self.max_tokens = max_tokens
        self.token_buffer = 500
        self.available_tokens = max_tokens - self.token_buffer

    def estimate_tokens(self, text: str) -> int:
        return len(text.split()) // 4 + 1

    def compress_page_content(self, content: str, max_tokens: int = 2000) -> str:
        estimated = self.estimate_tokens(content)
        
        if estimated <= max_tokens:
            return content
        
        lines = content.split('\n')
        compressed = []
        
        for line in lines:
            stripped = line.strip()
            if stripped and len(stripped) > 3:
                if not any(keyword in stripped.lower() for keyword in ['script', 'style', 'meta', 'link']):
                    compressed.append(stripped)
        
        result = '\n'.join(compressed)
        
        if self.estimate_tokens(result) > max_tokens:
            words = result.split()
            words = words[:max_tokens * 4]
            result = ' '.join(words)
        
        return result

    def format_elements_for_context(self, elements: List[Dict[str, Any]], max_items: int = 15) -> str:
        if not elements:
            return "No interactive elements found"
        
        formatted = []
        for i, elem in enumerate(elements[:max_items]):
            text = elem.get('text', '')[:40]
            selector = elem.get('selector', '')
            elem_type = elem.get('type', '')
            
            formatted.append(f"[{i}] {selector} ({elem_type}) - {text}")
        
        return '\n'.join(formatted)

    def create_page_summary(self, url: str, content: str, elements: List[Dict[str, Any]]) -> str:
        summary = f"""Current Page:
URL: {url}

Content Preview:
{self.compress_page_content(content, 1500)}

Interactive Elements:
{self.format_elements_for_context(elements, 12)}"""
        
        return summary

    def estimate_conversation_tokens(self, messages: List[Dict[str, str]]) -> int:
        total = 0
        for msg in messages:
            total += self.estimate_tokens(msg.get('content', ''))
        return total

    def should_trim_history(self, messages: List[Dict[str, str]]) -> bool:
        return self.estimate_conversation_tokens(messages) > self.available_tokens * 0.8
