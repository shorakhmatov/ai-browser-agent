import asyncio
import json
import logging
from typing import Optional, Dict, Any, List
from anthropic import Anthropic
from browser_controller import BrowserController

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIAgent:
    """Базовый AI агент для управления браузером"""
    
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        self.browser = BrowserController()
        self.conversation_history = []
        self.max_retries = 3
        self.destructive_actions = {"submit", "delete", "remove", "pay", "checkout", "purchase"}

    async def initialize(self):
        """Инициализировать агента"""
        await self.browser.launch()

    async def close(self):
        """Закрыть агента"""
        await self.browser.close()

    def _compress_content(self, content: str, max_length: int = 3000) -> str:
        if len(content) <= max_length:
            return content
        
        lines = content.split('\n')
        compressed = []
        for line in lines:
            stripped = line.strip()
            if stripped and len(stripped) > 3:
                compressed.append(stripped)
        
        result = '\n'.join(compressed[:100])
        if len(result) > max_length:
            result = result[:max_length] + "..."
        return result

    async def _get_page_state(self) -> Dict[str, Any]:
        url = await self.browser.get_current_url()
        text_content = await self.browser.extract_text_content()
        interactive_elements = await self.browser.get_interactive_elements()
        
        compressed_content = self._compress_content(text_content)
        
        return {
            "url": url,
            "page_content": compressed_content,
            "interactive_elements": interactive_elements[:20]
        }

    async def _parse_tool_calls(self, response_text: str) -> List[Dict[str, Any]]:
        tool_calls = []
        
        if "<tool_use" in response_text:
            import re
            pattern = r'<tool_use id="([^"]+)" name="([^"]+)">(.*?)</tool_use>'
            matches = re.findall(pattern, response_text, re.DOTALL)
            
            for tool_id, tool_name, tool_input in matches:
                try:
                    input_data = json.loads(tool_input.strip())
                    tool_calls.append({
                        "id": tool_id,
                        "name": tool_name,
                        "input": input_data
                    })
                except json.JSONDecodeError:
                    logger.error(f"Failed to parse tool input: {tool_input}")
        
        return tool_calls

    async def _execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
        try:
            if tool_name == "navigate":
                await self.browser.navigate(tool_input["url"])
                await asyncio.sleep(1)
                return "Navigation successful"
            
            elif tool_name == "click":
                selector = tool_input["selector"]
                await self.browser.click(selector)
                return f"Clicked element: {selector}"
            
            elif tool_name == "type":
                selector = tool_input["selector"]
                text = tool_input["text"]
                await self.browser.type_text(selector, text)
                return f"Typed text in {selector}"
            
            elif tool_name == "scroll":
                direction = tool_input.get("direction", "down")
                amount = tool_input.get("amount", 3)
                await self.browser.scroll(direction, amount)
                return f"Scrolled {direction}"
            
            elif tool_name == "wait":
                seconds = tool_input.get("seconds", 1)
                await asyncio.sleep(seconds)
                return f"Waited {seconds} seconds"
            
            elif tool_name == "extract_text":
                text = await self.browser.extract_text_content()
                return self._compress_content(text, 2000)
            
            elif tool_name == "get_elements":
                elements = await self.browser.get_interactive_elements()
                return json.dumps(elements[:15], indent=2)
            
            elif tool_name == "screenshot":
                path = tool_input.get("path", "screenshot.png")
                await self.browser.take_screenshot(path)
                return f"Screenshot saved to {path}"
            
            elif tool_name == "get_url":
                url = await self.browser.get_current_url()
                return f"Current URL: {url}"
            
            else:
                return f"Unknown tool: {tool_name}"
        
        except Exception as e:
            logger.error(f"Tool execution error: {e}")
            return f"Error executing {tool_name}: {str(e)}"

    async def _check_destructive_action(self, tool_name: str, tool_input: Dict[str, Any]) -> bool:
        if tool_name == "click":
            selector = tool_input.get("selector", "").lower()
            for action in self.destructive_actions:
                if action in selector:
                    return True
        return False

    async def execute_task(self, task: str) -> str:
        logger.info(f"Starting task: {task}")
        
        self.conversation_history = []
        
        system_prompt = """You are an AI agent that controls a web browser to complete tasks. 
You have access to tools to interact with the browser.

Available tools:
- navigate(url): Navigate to a URL
- click(selector): Click an element using CSS selector
- type(selector, text): Type text into an input field
- scroll(direction, amount): Scroll the page (direction: 'up' or 'down', amount: number of scrolls)
- wait(seconds): Wait for specified seconds
- extract_text(): Get all visible text from the page
- get_elements(): Get list of interactive elements
- screenshot(path): Take a screenshot
- get_url(): Get current URL

When you need to use a tool, format it like this:
<tool_use id="unique_id" name="tool_name">
{"param1": "value1", "param2": "value2"}
</tool_use>

Rules:
1. Always check the current page state before taking action
2. Use get_elements() to find the right selector to click
3. Be specific with selectors - use IDs or unique classes when possible
4. If an action fails, try alternative approaches
5. Report your progress and findings
6. When task is complete, summarize what was accomplished"""

        max_iterations = 15
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            logger.info(f"Iteration {iteration}/{max_iterations}")
            
            page_state = await self._get_page_state()
            
            user_message = f"""Current page state:
URL: {page_state['url']}
Page content (first 2000 chars):
{page_state['page_content']}

Interactive elements:
{json.dumps(page_state['interactive_elements'], indent=2)}

Task: {task}

What should I do next?"""
            
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })
            
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1500,
                system=system_prompt,
                messages=self.conversation_history
            )
            
            assistant_message = response.content[0].text
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            logger.info(f"Agent response: {assistant_message[:500]}")
            
            tool_calls = await self._parse_tool_calls(assistant_message)
            
            if not tool_calls:
                if "task completed" in assistant_message.lower() or "done" in assistant_message.lower():
                    logger.info("Task completed by agent")
                    return assistant_message
                elif iteration >= max_iterations:
                    return f"Max iterations reached. Last response: {assistant_message}"
                else:
                    await asyncio.sleep(1)
                    continue
            
            for tool_call in tool_calls:
                tool_name = tool_call["name"]
                tool_input = tool_call["input"]
                
                is_destructive = await self._check_destructive_action(tool_name, tool_input)
                if is_destructive:
                    logger.warning(f"Destructive action detected: {tool_name} with {tool_input}")
                    user_input = input(f"Agent wants to execute: {tool_name}({tool_input}). Allow? (y/n): ")
                    if user_input.lower() != 'y':
                        logger.info("User rejected destructive action")
                        self.conversation_history.append({
                            "role": "user",
                            "content": "User rejected this action. Try a different approach."
                        })
                        continue
                
                result = await self._execute_tool(tool_name, tool_input)
                logger.info(f"Tool result: {result}")
                
                self.conversation_history.append({
                    "role": "user",
                    "content": f"Tool execution result: {result}"
                })
            
            await asyncio.sleep(0.5)
        
        return "Max iterations reached without completing task"


async def main():
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set in .env file")
        return
    
    agent = AIAgent(api_key)
    await agent.initialize()
    
    try:
        task = input("Enter task for the agent: ")
        result = await agent.execute_task(task)
        print(f"\nTask result:\n{result}")
    finally:
        await agent.close()


if __name__ == "__main__":
    asyncio.run(main())
