import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Конфигурация приложения"""
    
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    
    # Конфигурация браузера
    BROWSER_CONFIG = {
        "headless": False,
        "args": ["--no-sandbox", "--disable-setuid-sandbox"]
    }
    
    # Конфигурация агента
    AGENT_CONFIG = {
        "max_iterations": 20,
        "max_retries": 3,
        "timeout": 30000,
        "wait_between_actions": 0.3
    }
    
    # Конфигурация контекста
    CONTEXT_CONFIG = {
        "max_tokens": 8000,
        "token_buffer": 500,
        "max_page_content": 2000,
        "max_elements": 15
    }
    
    # Деструктивные действия, требующие подтверждения
    DESTRUCTIVE_ACTIONS = {
        "submit", "delete", "remove", "pay", 
        "checkout", "purchase", "confirm", "send"
    }
    
    @classmethod
    def validate(cls):
        """Проверить конфигурацию"""
        if not cls.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY не установлен в .env файле")
        return True
