#!/usr/bin/env python3
"""
AI Browser Agent - Главная точка входа
Автономный AI-агент для автоматизации веб-браузера
"""

import asyncio
import sys
import os
from dotenv import load_dotenv
from advanced_agent import AdvancedAIAgent
from cli import AgentCLI


async def run_agent_from_args():
    """Запустить агента с аргументами командной строки"""
    if len(sys.argv) < 2:
        return False
    
    task = " ".join(sys.argv[1:])
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("Ошибка: ANTHROPIC_API_KEY не установлен в .env файле")
        return False
    
    agent = AdvancedAIAgent(api_key)
    await agent.initialize()
    
    try:
        print(f"\n{'='*60}")
        print(f"Задача: {task}")
        print(f"{'='*60}\n")
        
        result = await agent.execute_task(task)
        
        print(f"\n{'='*60}")
        print(f"Результат:\n{result}")
        print(f"{'='*60}\n")
        
        return True
    
    except Exception as e:
        print(f"Ошибка: {e}")
        return False
    
    finally:
        await agent.close()


async def main():
    """Главная функция"""
    print("\n" + "="*60)
    print("AI Browser Agent")
    print("="*60)
    
    # Проверяем, передана ли задача как аргумент
    if len(sys.argv) > 1:
        success = await run_agent_from_args()
        sys.exit(0 if success else 1)
    
    # Иначе запускаем интерактивный режим
    cli = AgentCLI()
    
    try:
        await cli.initialize()
        await cli.run_interactive()
    
    except KeyboardInterrupt:
        print("\n\nПрервано пользователем")
    
    except Exception as e:
        print(f"Ошибка: {e}")
    
    finally:
        await cli.close()


if __name__ == "__main__":
    asyncio.run(main())
