#!/usr/bin/env python3
"""
AI Browser Agent - Main entry point
Autonomous AI agent for web browser automation
"""

import asyncio
import sys
import os
from dotenv import load_dotenv
from advanced_agent import AdvancedAIAgent
from cli import AgentCLI


async def run_agent_from_args():
    """Run agent with command line arguments"""
    if len(sys.argv) < 2:
        return False
    
    task = " ".join(sys.argv[1:])
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set in .env file")
        return False
    
    agent = AdvancedAIAgent(api_key)
    await agent.initialize()
    
    try:
        print(f"\n{'='*60}")
        print(f"Task: {task}")
        print(f"{'='*60}\n")
        
        result = await agent.execute_task(task)
        
        print(f"\n{'='*60}")
        print(f"Result:\n{result}")
        print(f"{'='*60}\n")
        
        return True
    
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    finally:
        await agent.close()


async def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("AI Browser Agent")
    print("="*60)
    
    # Check if task provided as argument
    if len(sys.argv) > 1:
        success = await run_agent_from_args()
        sys.exit(0 if success else 1)
    
    # Otherwise run interactive CLI
    cli = AgentCLI()
    
    try:
        await cli.initialize()
        await cli.run_interactive()
    
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        await cli.close()


if __name__ == "__main__":
    asyncio.run(main())
