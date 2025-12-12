import asyncio
import os
from dotenv import load_dotenv
from advanced_agent import AdvancedAIAgent


async def example_search_task():
    """Example: Search for information on a website"""
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    agent = AdvancedAIAgent(api_key)
    await agent.initialize()
    
    try:
        task = "Go to python.org and find the latest Python version number"
        result = await agent.execute_task(task)
        print(f"Result: {result}")
    finally:
        await agent.close()


async def example_form_filling():
    """Example: Fill out a form"""
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    agent = AdvancedAIAgent(api_key)
    await agent.initialize()
    
    try:
        task = "Fill out the contact form on the website with example data"
        result = await agent.execute_task(task)
        print(f"Result: {result}")
    finally:
        await agent.close()


async def example_navigation():
    """Example: Navigate and extract information"""
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    agent = AdvancedAIAgent(api_key)
    await agent.initialize()
    
    try:
        task = "Navigate to github.com and find the trending repositories"
        result = await agent.execute_task(task)
        print(f"Result: {result}")
    finally:
        await agent.close()


if __name__ == "__main__":
    print("AI Browser Agent Examples")
    print("=" * 60)
    print("\nAvailable examples:")
    print("1. Search task")
    print("2. Form filling")
    print("3. Navigation")
    
    choice = input("\nSelect example (1-3): ").strip()
    
    if choice == "1":
        asyncio.run(example_search_task())
    elif choice == "2":
        asyncio.run(example_form_filling())
    elif choice == "3":
        asyncio.run(example_navigation())
    else:
        print("Invalid choice")
