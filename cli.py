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
    """Интерфейс командной строки для AI агента"""
    
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY не установлен в .env файле")
        self.agent = None

    async def initialize(self):
        """Инициализировать агента"""
        self.agent = AIAgent(self.api_key)
        await self.agent.initialize()
        logger.info("Агент инициализирован")

    async def close(self):
        """Закрыть агента"""
        if self.agent:
            await self.agent.close()
        logger.info("Агент закрыт")

    async def run_interactive(self):
        """Запустить интерактивный режим"""
        print("\n" + "="*60)
        print("AI Browser Agent - Интерактивный режим")
        print("="*60)
        print("\nКоманды:")
        print("  task <описание>    - Выполнить задачу")
        print("  screenshot <путь>  - Сделать скриншот")
        print("  url                - Получить текущий URL")
        print("  help               - Справка")
        print("  exit               - Выход")
        print("="*60 + "\n")

        while True:
            try:
                user_input = input("\n> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == "exit":
                    print("Выход...")
                    break
                
                elif user_input.lower() == "help":
                    print("\nДоступные команды:")
                    print("  task <описание>    - Выполнить задачу")
                    print("  screenshot <путь>  - Сделать скриншот")
                    print("  url                - Получить текущий URL")
                    print("  exit               - Выход")
                
                elif user_input.lower() == "url":
                    url = await self.agent.browser.get_current_url()
                    print(f"Текущий URL: {url}")
                
                elif user_input.startswith("screenshot"):
                    parts = user_input.split(maxsplit=1)
                    path = parts[1] if len(parts) > 1 else "screenshot.png"
                    await self.agent.browser.take_screenshot(path)
                    print(f"Скриншот сохранен в {path}")
                
                elif user_input.startswith("task"):
                    task = user_input[5:].strip()
                    if not task:
                        print("Пожалуйста, укажите описание задачи")
                        continue
                    
                    print(f"\nВыполнение задачи: {task}")
                    print("-" * 60)
                    result = await self.agent.execute_task(task)
                    print("-" * 60)
                    print(f"\nРезультат:\n{result}\n")
                
                else:
                    print("Неизвестная команда. Введите 'help' для справки.")
            
            except KeyboardInterrupt:
                print("\nПрервано пользователем")
                break
            except Exception as e:
                logger.error(f"Ошибка: {e}")
                print(f"Ошибка: {e}")

    async def run_single_task(self, task: str):
        """Выполнить одну задачу"""
        print(f"\nВыполнение задачи: {task}")
        print("-" * 60)
        result = await self.agent.execute_task(task)
        print("-" * 60)
        print(f"\nРезультат:\n{result}\n")


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
