import asyncio
import json
import logging
from typing import Optional, Dict, Any, List
from anthropic import Anthropic
from browser_controller import BrowserController
from context_manager import ContextManager
from error_handler import ErrorHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AdvancedAIAgent:
    """Продвинутый AI агент с улучшенной обработкой ошибок и контекста"""
    
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        self.browser = BrowserController()
        self.context_manager = ContextManager()
        self.error_handler = ErrorHandler()
        self.conversation_history = []
        self.max_iterations = 20
        self.destructive_actions = {"submit", "delete", "remove", "pay", "checkout", "purchase", "confirm"}
        self.task_state = {
            "started_at": None,
            "iterations": 0,
            "last_url": None,
            "actions_taken": []
        }

    async def initialize(self):
        """Инициализировать продвинутого агента"""
        await self.browser.launch()
        logger.info("Продвинутый агент инициализирован")

    async def close(self):
        """Закрыть продвинутого агента"""
        await self.browser.close()

    async def _get_page_state(self) -> Dict[str, Any]:
        url = await self.browser.get_current_url()
        text_content = await self.browser.extract_text_content()
        interactive_elements = await self.browser.get_interactive_elements()
        
        return {
            "url": url,
            "page_content": text_content,
            "interactive_elements": interactive_elements
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
                url = tool_input["url"]
                await self.browser.navigate(url)
                self.task_state["last_url"] = url
                await asyncio.sleep(1.5)
                return f"Successfully navigated to {url}"
            
            elif tool_name == "click":
                selector = tool_input["selector"]
                try:
                    await self.browser.click(selector)
                    self.task_state["actions_taken"].append(f"click:{selector}")
                    return f"Successfully clicked: {selector}"
                except Exception as e:
                    if await self.error_handler.handle_click_error(selector, self.browser):
                        await asyncio.sleep(1)
                        await self.browser.click(selector)
                        return f"Clicked after retry: {selector}"
                    raise
            
            elif tool_name == "type":
                selector = tool_input["selector"]
                text = tool_input["text"]
                await self.browser.type_text(selector, text)
                self.task_state["actions_taken"].append(f"type:{selector}")
                return f"Typed in {selector}: {text[:50]}"
            
            elif tool_name == "scroll":
                direction = tool_input.get("direction", "down")
                amount = tool_input.get("amount", 3)
                await self.browser.scroll(direction, amount)
                return f"Scrolled {direction} by {amount} steps"
            
            elif tool_name == "wait":
                seconds = tool_input.get("seconds", 1)
                await asyncio.sleep(seconds)
                return f"Waited {seconds} seconds"
            
            elif tool_name == "extract_text":
                text = await self.browser.extract_text_content()
                compressed = self.context_manager.compress_page_content(text, 2000)
                return compressed
            
            elif tool_name == "get_elements":
                elements = await self.browser.get_interactive_elements()
                formatted = self.context_manager.format_elements_for_context(elements, 15)
                return formatted
            
            elif tool_name == "screenshot":
                path = tool_input.get("path", "screenshot.png")
                await self.browser.take_screenshot(path)
                return f"Screenshot saved to {path}"
            
            elif tool_name == "get_url":
                url = await self.browser.get_current_url()
                return f"Current URL: {url}"
            
            elif tool_name == "wait_for_element":
                selector = tool_input["selector"]
                timeout = tool_input.get("timeout", 5000)
                try:
                    await self.browser.wait_for_element(selector, timeout)
                    return f"Element appeared: {selector}"
                except Exception as e:
                    if await self.error_handler.handle_timeout_error(selector, self.browser):
                        return f"Timeout for element: {selector}, continuing..."
                    raise
            
            else:
                return f"Unknown tool: {tool_name}"
        
        except Exception as e:
            error_msg = f"Error executing {tool_name}: {str(e)}"
            self.error_handler.record_error(tool_name, str(e))
            logger.error(error_msg)
            return error_msg

    async def _check_destructive_action(self, tool_name: str, tool_input: Dict[str, Any]) -> bool:
        if tool_name == "click":
            selector = tool_input.get("selector", "").lower()
            for action in self.destructive_actions:
                if action in selector:
                    return True
        return False

    async def execute_task(self, task: str) -> str:
        logger.info(f"Starting advanced task: {task}")
        self.conversation_history = []
        self.task_state["iterations"] = 0
        
        system_prompt = """You are an advanced AI agent that controls a web browser to complete complex tasks.

Available tools:
- navigate(url): Navigate to a URL
- click(selector): Click an element using CSS selector
- type(selector, text): Type text into an input field
- scroll(direction, amount): Scroll the page
- wait(seconds): Wait for specified seconds
- extract_text(): Get all visible text from the page
- get_elements(): Get list of interactive elements
- screenshot(path): Take a screenshot
- get_url(): Get current URL
- wait_for_element(selector, timeout): Wait for element to appear

Strategy:
1. First, understand the current page state
2. Identify what needs to be done
3. Find the right elements to interact with
4. Execute actions step by step
5. Verify results and adapt if needed
6. Report progress and findings

Be thorough but efficient. If something fails, try alternative approaches."""

        while self.task_state["iterations"] < self.max_iterations:
            self.task_state["iterations"] += 1
            logger.info(f"Iteration {self.task_state['iterations']}/{self.max_iterations}")
            
            page_state = await self._get_page_state()
            
            summary = self.context_manager.create_page_summary(
                page_state["url"],
                page_state["page_content"],
                page_state["interactive_elements"]
            )
            
            user_message = f"""{summary}

Task: {task}

Actions taken so far: {', '.join(self.task_state['actions_taken'][-5:]) if self.task_state['actions_taken'] else 'None'}

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
            
            logger.info(f"Agent: {assistant_message[:300]}")
            
            tool_calls = await self._parse_tool_calls(assistant_message)
            
            if not tool_calls:
                if any(phrase in assistant_message.lower() for phrase in ["task completed", "done", "finished", "successfully"]):
                    logger.info("Task completed")
                    return assistant_message
                elif self.task_state["iterations"] >= self.max_iterations:
                    return f"Max iterations reached. Summary: {assistant_message}"
                else:
                    await asyncio.sleep(1)
                    continue
            
            for tool_call in tool_calls:
                tool_name = tool_call["name"]
                tool_input = tool_call["input"]
                
                is_destructive = await self._check_destructive_action(tool_name, tool_input)
                if is_destructive:
                    logger.warning(f"Destructive action: {tool_name}({tool_input})")
                    user_input = input(f"\n⚠️  Agent wants to: {tool_name}({json.dumps(tool_input)})\nAllow? (y/n): ")
                    if user_input.lower() != 'y':
                        self.conversation_history.append({
                            "role": "user",
                            "content": "User rejected this action. Try a different approach."
                        })
                        continue
                
                result = await self._execute_tool(tool_name, tool_input)
                logger.info(f"Result: {result[:200]}")
                
                self.conversation_history.append({
                    "role": "user",
                    "content": f"Tool result: {result}"
                })
            
            await asyncio.sleep(0.3)
        
        return f"Max iterations ({self.max_iterations}) reached without completing task"


async def main():
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set")
        return
    
    agent = AdvancedAIAgent(api_key)
    await agent.initialize()
    
    try:
        task = input("Enter task: ")
        result = await agent.execute_task(task)
        print(f"\n{'='*60}")
        print(f"Result:\n{result}")
        print(f"{'='*60}")
    finally:
        await agent.close()


if __name__ == "__main__":
    asyncio.run(main())
