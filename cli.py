import asyncio
import os
import sys
from dotenv import load_dotenv
from ai_agent import AIAgent
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AgentCLI:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not set in .env file")
        self.agent = None

    async def initialize(self):
        self.agent = AIAgent(self.api_key)
        await self.agent.initialize()
        logger.info("Agent initialized")

    async def close(self):
        if self.agent:
            await self.agent.close()
        logger.info("Agent closed")

    async def run_interactive(self):
        print("\n" + "="*60)
        print("AI Browser Agent - Interactive Mode")
        print("="*60)
        print("\nCommands:")
        print("  task <description> - Execute a task")
        print("  screenshot <path>  - Take a screenshot")
        print("  url                - Get current URL")
        print("  help               - Show this help")
        print("  exit               - Exit the agent")
        print("="*60 + "\n")

        while True:
            try:
                user_input = input("\n> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == "exit":
                    print("Exiting...")
                    break
                
                elif user_input.lower() == "help":
                    print("\nAvailable commands:")
                    print("  task <description> - Execute a task")
                    print("  screenshot <path>  - Take a screenshot")
                    print("  url                - Get current URL")
                    print("  exit               - Exit the agent")
                
                elif user_input.lower() == "url":
                    url = await self.agent.browser.get_current_url()
                    print(f"Current URL: {url}")
                
                elif user_input.startswith("screenshot"):
                    parts = user_input.split(maxsplit=1)
                    path = parts[1] if len(parts) > 1 else "screenshot.png"
                    await self.agent.browser.take_screenshot(path)
                    print(f"Screenshot saved to {path}")
                
                elif user_input.startswith("task"):
                    task = user_input[5:].strip()
                    if not task:
                        print("Please provide a task description")
                        continue
                    
                    print(f"\nExecuting task: {task}")
                    print("-" * 60)
                    result = await self.agent.execute_task(task)
                    print("-" * 60)
                    print(f"\nResult:\n{result}\n")
                
                else:
                    print("Unknown command. Type 'help' for available commands.")
            
            except KeyboardInterrupt:
                print("\nInterrupted by user")
                break
            except Exception as e:
                logger.error(f"Error: {e}")
                print(f"Error: {e}")

    async def run_single_task(self, task: str):
        print(f"\nExecuting task: {task}")
        print("-" * 60)
        result = await self.agent.execute_task(task)
        print("-" * 60)
        print(f"\nResult:\n{result}\n")


async def main():
    cli = AgentCLI()
    
    try:
        await cli.initialize()
        
        if len(sys.argv) > 1:
            task = " ".join(sys.argv[1:])
            await cli.run_single_task(task)
        else:
            await cli.run_interactive()
    
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"Fatal error: {e}")
    
    finally:
        await cli.close()


if __name__ == "__main__":
    asyncio.run(main())
